const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "no-store",
};

const TOPICS = new Set(["po", "sprint", "ai", "other"]);
const BUDGETS = new Set(["under-10", "10-25", "25-60", "over-60", "unclear"]);
const RATE_LIMIT = new Map();

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: JSON_HEADERS });
}

function clean(value, maxLength) {
  return String(value || "").trim().slice(0, maxLength);
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function getClientIp(request) {
  return request.headers.get("cf-connecting-ip") || "unknown";
}

function rateLimited(ip) {
  const now = Date.now();
  const windowMs = 10 * 60 * 1000;
  const maxRequests = 5;
  const entry = RATE_LIMIT.get(ip) || { count: 0, resetAt: now + windowMs };
  if (now > entry.resetAt) {
    entry.count = 0;
    entry.resetAt = now + windowMs;
  }
  entry.count += 1;
  RATE_LIMIT.set(ip, entry);
  return entry.count > maxRequests;
}

function validate(payload) {
  const who = clean(payload.who, 100);
  const email = clean(payload.email, 180);
  const context = clean(payload.context, 300);
  const budget = clean(payload.budget, 40);
  const topics = Array.isArray(payload.topics) ? payload.topics.map((topic) => clean(topic, 40)) : [];
  const privacy = payload.privacy === true;
  const website = clean(payload.website, 200);

  if (website) return { ok: false, status: 400, error: "Spam check failed." };
  if (!who || !email || !context || !budget || !privacy || topics.length === 0) {
    return { ok: false, status: 400, error: "Required fields are missing." };
  }
  if (!isEmail(email)) return { ok: false, status: 400, error: "Invalid email address." };
  if (!BUDGETS.has(budget) || topics.some((topic) => !TOPICS.has(topic))) {
    return { ok: false, status: 400, error: "Invalid form value." };
  }

  return { ok: true, data: { who, email, context, budget, topics, privacy } };
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function buildEmail({ who, email, context, budget, topics }) {
  const topicText = topics.join(", ");
  const text = [
    "Neue Anfrage über daniel-baran.com",
    "",
    `Wer: ${who}`,
    `E-Mail: ${email}`,
    `Themen: ${topicText}`,
    `Budget: ${budget}`,
    "",
    "Kontext:",
    context,
  ].join("\n");

  const html = `
    <h2>Neue Anfrage über daniel-baran.com</h2>
    <p><strong>Wer:</strong> ${escapeHtml(who)}</p>
    <p><strong>E-Mail:</strong> ${escapeHtml(email)}</p>
    <p><strong>Themen:</strong> ${escapeHtml(topicText)}</p>
    <p><strong>Budget:</strong> ${escapeHtml(budget)}</p>
    <p><strong>Kontext:</strong></p>
    <p>${escapeHtml(context).replace(/\n/g, "<br>")}</p>
  `;

  return { text, html };
}

async function handleContact(request, env) {
  if (request.method === "OPTIONS") return new Response(null, { status: 204 });
  if (request.method !== "POST") return json({ ok: false, error: "Method not allowed." }, 405);

  const ip = getClientIp(request);
  if (rateLimited(ip)) return json({ ok: false, error: "Too many requests." }, 429);

  let payload;
  try {
    payload = await request.json();
  } catch {
    return json({ ok: false, error: "Invalid JSON." }, 400);
  }

  const result = validate(payload);
  if (!result.ok) return json({ ok: false, error: result.error }, result.status);

  const apiKey = env.RESEND_API_KEY;
  const from = env.CONTACT_FROM_EMAIL;
  const to = env.CONTACT_TO_EMAIL || "kontakt@daniel-baran.com";

  if (!apiKey || !from) {
    return json({ ok: false, error: "Contact service is not configured." }, 503);
  }

  const email = buildEmail(result.data);
  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      authorization: `Bearer ${apiKey}`,
      "content-type": "application/json",
    },
    body: JSON.stringify({
      from,
      to,
      reply_to: result.data.email,
      subject: `${env.CONTACT_SUBJECT_PREFIX || "Website-Anfrage"}: ${result.data.who}`,
      text: email.text,
      html: email.html,
    }),
  });

  if (!response.ok) {
    return json({ ok: false, error: "Email delivery failed." }, 502);
  }

  return json({ ok: true });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/contact") {
      return handleContact(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};
