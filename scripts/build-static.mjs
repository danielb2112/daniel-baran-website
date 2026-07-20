#!/usr/bin/env node

import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const DIST = path.join(ROOT, "dist");
const SITE = "https://daniel-baran.com";
const LASTMOD = "2026-07-20";
const VESTIUM_YOUTUBE_ID = "La4rd4JhlFE";

const LANGS = ["de", "en", "pl"];
const OG_LOCALE = { de: "de_DE", en: "en_US", pl: "pl_PL" };
const NAV_LABELS = {
  de: {
    navAbout: "Über mich",
    navServices: "Leistungen",
    navProcess: "Prozess",
    navProjects: "Projekte",
    navContact: "Kontakt",
    navMenuLabel: "Menü",
  },
  en: {
    navAbout: "About",
    navServices: "Services",
    navProcess: "Process",
    navProjects: "Projects",
    navContact: "Contact",
    navMenuLabel: "Menu",
  },
  pl: {
    navAbout: "O mnie",
    navServices: "Usługi",
    navProcess: "Proces",
    navProjects: "Projekty",
    navContact: "Kontakt",
    navMenuLabel: "Menu",
  },
};

const CASE_SLUGS = [
  "swr-ki-empfehlungsengine",
  "swr-ki-testphase",
  "swr-multiplatform-service",
  "swr-ard-transcoding",
  "vestium",
  "infinite-playa",
  "uci-track-champions-league",
  "systemmigration-konzernverbund",
  "fahrzeugumbauten-dokumentation",
];

const ROUTE_GROUPS = [
  { kind: "home", routes: { de: "/", en: "/en/", pl: "/pl/" } },
  { kind: "about", routes: { de: "/ueber-mich/", en: "/en/about/", pl: "/pl/o-mnie/" } },
  { kind: "projects", routes: { de: "/projekte/", en: "/en/projects/", pl: "/pl/projekty/" } },
  { kind: "imprint", routes: { de: "/impressum/", en: "/en/imprint/", pl: "/pl/nota-prawna/" } },
  { kind: "privacy", routes: { de: "/datenschutz/", en: "/en/privacy/", pl: "/pl/prywatnosc/" } },
  ...CASE_SLUGS.map((slug) => ({
    kind: "case",
    slug,
    routes: {
      de: `/projekte/${slug}/`,
      en: `/en/projects/${slug}/`,
      pl: `/pl/projekty/${slug}/`,
    },
  })),
];

function routeFor(page, lang) {
  return page.routes[lang];
}

function fileForRoute(base, route) {
  const rel = route === "/" ? "index.html" : path.join(route.slice(1), "index.html");
  return path.join(base, rel);
}

function sourcePath(page, lang) {
  return fileForRoute(ROOT, routeFor(page, lang));
}

function outputPath(page, lang) {
  return fileForRoute(DIST, routeFor(page, lang));
}

function htmlEscape(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function extractHead(source) {
  const match = source.match(/<head>[\s\S]*?<\/head>/);
  if (!match) throw new Error("No <head> found");
  return match[0];
}

function extractXdc(source) {
  const match = source.match(/<x-dc>([\s\S]*?)<\/x-dc>/);
  if (!match) return null;
  return match[1];
}

function extractHelmetStyle(xdc) {
  const match = xdc.match(/<helmet>[\s\S]*?<style>([\s\S]*?)<\/style>[\s\S]*?<\/helmet>/);
  return match ? match[1].trim() : "";
}

function extractDataScript(source) {
  const match = source.match(/<script type="text\/x-dc"[^>]*>([\s\S]*?)<\/script>/);
  if (!match) return "";
  return match[1];
}

function extractConstExpression(source, name) {
  const marker = `const ${name} =`;
  const markerIndex = source.indexOf(marker);
  if (markerIndex < 0) return null;

  let index = markerIndex + marker.length;
  while (/\s/.test(source[index])) index += 1;

  const open = source[index];
  const close = open === "{" ? "}" : open === "[" ? "]" : null;
  if (!close) throw new Error(`Unsupported ${name} initializer`);

  let depth = 0;
  let quote = "";
  let escaped = false;

  for (let i = index; i < source.length; i += 1) {
    const ch = source[i];

    if (quote) {
      if (escaped) {
        escaped = false;
      } else if (ch === "\\") {
        escaped = true;
      } else if (ch === quote) {
        quote = "";
      }
      continue;
    }

    if (ch === "\"" || ch === "'" || ch === "`") {
      quote = ch;
      continue;
    }

    if (ch === open) depth += 1;
    if (ch === close) depth -= 1;
    if (depth === 0) return source.slice(index, i + 1);
  }

  throw new Error(`Could not parse ${name}`);
}

function evaluateLiteral(source, name) {
  const expression = extractConstExpression(source, name);
  if (!expression) return null;
  return vm.runInNewContext(`(${expression})`, Object.create(null), { timeout: 1000 });
}

function words(text) {
  let i = 0;
  return String(text).split(" ").map((word) => ({
    letters: word.split("").map((char) => ({ char, delay: `${150 + i++ * 28}ms` })),
  }));
}

function languageLinks(lang) {
  return [
    { code: "de", label: "DE" },
    { code: "pl", label: "PL" },
    { code: "en", label: "EN" },
  ].map((item) => ({
    ...item,
    current: lang === item.code ? "true" : "false",
    color: lang === item.code ? "#0D0D0C" : "#4A4945",
    underline: lang === item.code ? "#0D0D0C" : "transparent",
    select: "",
  }));
}

function accordionRows(items, withAccent = false) {
  return items.map((item) => ({
    ...item,
    open: "false",
    rows: "0fr",
    rot: "rotate(0deg)",
    toggle: "",
    ...(withAccent
      ? {
          color: item.accent ? "#2A2AE5" : "#0D0D0C",
          trans: item.accent ? "none" : "grid-template-rows 0.7s cubic-bezier(0.62,0.05,0.01,0.99)",
        }
      : {}),
  }));
}

function initialValues(page, lang, data, meta) {
  const t = data[lang];
  if (!t) throw new Error(`Missing DATA.${lang}`);

  if (page.kind === "home") {
    return {
      t,
      langs: languageLinks(lang),
      h1Words: words("PROJECT & PRODUCT DELIVERY"),
      nameWords: words("DANIEL BARAN"),
      services: accordionRows(t.services),
      processSteps: accordionRows(t.processSteps),
      cases: t.cases,
      topics: t.topics.map((topic) => ({
        ...topic,
        selected: "false",
        mark: "+",
        color: "#4A4945",
        weight: 400,
        underline: "transparent",
        toggle: "",
      })),
      budgets: t.budgets.map((budget) => ({
        ...budget,
        selected: "false",
        color: "#4A4945",
        weight: 400,
        underline: "transparent",
        select: "",
      })),
      portraitFilter: "grayscale(1) contrast(1.05)",
      formMsg: "",
      formMsgColor: "#4A4945",
      submitForm: "",
    };
  }

  if (page.kind === "about") {
    return {
      t,
      langs: languageLinks(lang),
      headlineWords: words("PASSIONATE PROJECT MANAGER"),
      facts: t.facts,
      skills: accordionRows(t.skills, true),
      timeline: t.timeline,
      toolkit: accordionRows(t.toolkit, true),
    };
  }

  if (page.kind === "projects") {
    if (!meta) throw new Error("Projects page is missing META");
    return {
      t,
      langs: languageLinks(lang),
      headlineWords: words(t.h1),
      cases: meta.map((item, index) => ({
        ...item,
        ...t.cases[index],
        hasImg: item.img ? "true" : "",
        noImg: item.img ? "" : "true",
        img: item.img || "",
      })),
    };
  }

  if (page.kind === "case") {
    const mergedText = { ...NAV_LABELS[lang], ...t };
    const hasVestiumVideo = page.slug === "vestium" && Boolean(VESTIUM_YOUTUBE_ID);
    return {
      t: mergedText,
      langs: languageLinks(lang),
      hasVestiumVideo: hasVestiumVideo ? "true" : "",
      noVestiumVideo: hasVestiumVideo ? "" : "true",
      vestiumVideoSrc: hasVestiumVideo
        ? `https://www.youtube-nocookie.com/embed/${encodeURIComponent(VESTIUM_YOUTUBE_ID)}?rel=0&modestbranding=1`
        : "",
      prev: "",
      next: "",
    };
  }

  throw new Error(`Unsupported template page kind ${page.kind}`);
}

function readPath(scope, expression) {
  const parts = expression.trim().split(".");
  let value = scope;
  for (const part of parts) {
    if (part === "true") return true;
    if (part === "false") return false;
    if (part === "null") return null;
    if (value == null || !(part in Object(value))) return "";
    value = value[part];
  }
  return value;
}

function truthy(value) {
  return value === true || value === "true" || (Boolean(value) && value !== "false");
}

function parseAttr(tag, name) {
  const match = tag.match(new RegExp(`${name}="([^"]*)"`));
  return match ? match[1] : "";
}

function findMatchingTag(template, start, tagName) {
  const re = new RegExp(`<\\/?${tagName}\\b[^>]*>`, "g");
  re.lastIndex = start;
  let depth = 0;
  let openEnd = -1;

  while (true) {
    const match = re.exec(template);
    if (!match) throw new Error(`No closing </${tagName}> found`);
    const isClosing = match[0].startsWith(`</${tagName}`);
    if (!isClosing) {
      depth += 1;
      if (depth === 1) openEnd = re.lastIndex;
    } else {
      depth -= 1;
      if (depth === 0) {
        return {
          openTag: template.slice(start, openEnd),
          openEnd,
          closeStart: match.index,
          closeEnd: re.lastIndex,
        };
      }
    }
  }
}

function interpolate(template, scope) {
  return template.replace(/\{\{\s*([^}]+?)\s*\}\}/g, (_match, expression) => {
    const value = readPath(scope, expression);
    if (typeof value === "function") return "";
    return htmlEscape(value);
  });
}

function renderTemplate(template, scope) {
  let output = "";
  let cursor = 0;

  while (cursor < template.length) {
    const nextFor = template.indexOf("<sc-for", cursor);
    const nextIf = template.indexOf("<sc-if", cursor);
    const candidates = [nextFor, nextIf].filter((index) => index >= 0);

    if (candidates.length === 0) {
      output += interpolate(template.slice(cursor), scope);
      break;
    }

    const next = Math.min(...candidates);
    output += interpolate(template.slice(cursor, next), scope);

    const tagName = template.startsWith("<sc-for", next) ? "sc-for" : "sc-if";
    const match = findMatchingTag(template, next, tagName);
    const inner = template.slice(match.openEnd, match.closeStart);

    if (tagName === "sc-for") {
      const listExpr = parseAttr(match.openTag, "list").replace(/^\{\{\s*|\s*\}\}$/g, "");
      const asName = parseAttr(match.openTag, "as");
      const list = readPath(scope, listExpr);
      if (!Array.isArray(list)) throw new Error(`Expected array for ${listExpr}`);
      output += list
        .map((item, index) => renderTemplate(inner, { ...scope, [asName]: item, [`${asName}Index`]: index }))
        .join("");
    } else {
      const valueExpr = parseAttr(match.openTag, "value").replace(/^\{\{\s*|\s*\}\}$/g, "");
      if (truthy(readPath(scope, valueExpr))) output += renderTemplate(inner, scope);
    }

    cursor = match.closeEnd;
  }

  return output;
}

function prepareTemplate(xdc, page) {
  let template = xdc.replace(/<helmet>[\s\S]*?<\/helmet>/, "").trim();

  if (page.kind === "home") {
    template = template
      .replace('onSubmit="{{ submitForm }}"', "data-contact-form")
      .replace('onClick="{{ tp.toggle }}" aria-pressed="{{ tp.selected }}"', 'data-topic="{{ tp.id }}" aria-pressed="{{ tp.selected }}"')
      .replace('onClick="{{ b.select }}" aria-pressed="{{ b.selected }}"', 'data-budget="{{ b.id }}" aria-pressed="{{ b.selected }}"')
      .replace("<p aria-live=\"polite\" style=\"margin:14px 0 0;", "<p data-form-message aria-live=\"polite\" style=\"margin:14px 0 0;");
  }

  return template;
}

function replaceLanguageButtons(markup, page) {
  return markup.replace(
    /<button type="button" onClick="" aria-current="(true|false)"([^>]*)>(DE|PL|EN)<\/button>/g,
    (_match, current, attrs, label) => {
      const code = label.toLowerCase();
      const currentAttr = current === "true" ? ' aria-current="page"' : "";
      return `<a href="${routeFor(page, code)}" data-lang-link="${code}"${currentAttr}${attrs}>${label}</a>`;
    },
  );
}

function postprocessBody(markup, page, lang) {
  let body = replaceLanguageButtons(markup, page);

  body = body
    .replace(/\s+onClick=""/g, "")
    .replace(/\s+onSubmit=""/g, "")
    .replace(/\s+onclick="this\.closest\('details'\)\.removeAttribute\('open'\)"/g, " data-close-menu")
    .replace(/\s+onclick="document\.cookie='db-lang=([a-z]+); Path=\/; Max-Age=31536000; SameSite=Lax; Secure';"/g, ' data-lang-link="$1"');

  if (page.kind === "case") {
    body = body.replace('class="case-root"', 'class="case-root no-track"');
  }

  if (page.kind === "home" && lang !== "de") {
    body = body.replace('href="/datenschutz/"', `href="${ROUTE_GROUPS.find((group) => group.kind === "privacy").routes[lang]}"`);
  }

  return body;
}

function patchPrivacyCopy(html, lang) {
  const replacements = {
    de: [
      "Die Website stellt feste Sprachversionen unter /, /pl/ und /en/ bereit. Beim Aufruf der Startseite kann der Browser-Header Accept-Language technisch ausgewertet werden, um Besucher auf die passende Sprachversion zu leiten. Wenn Sie eine Sprache wählen oder eine Sprache automatisch erkannt wurde, kann das technisch notwendige Cookie db-lang mit dem Sprachcode de, en oder pl gesetzt werden. Zweck ist ausschließlich die Speicherung der Sprachwahl und die korrekte Navigation auf dieser Website. Die Speicherdauer beträgt 12 Monate. Rechtsgrundlage für das Setzen des Cookies ist § 25 Abs. 2 TTDSG; die weitere Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Zusätzlich kann derselbe Sprachcode lokal im Browser als localStorage-Eintrag db-lang gespeichert werden. Es findet kein Tracking statt und die Sprachwahl wird nicht an Dritte weitergegeben.",
      "Die Website stellt feste Sprachversionen unter /, /pl/ und /en/ bereit. Wenn Sie den Sprachumschalter nutzen, kann das technisch notwendige Cookie db-lang mit dem Sprachcode de, en oder pl gesetzt werden. Zweck ist ausschließlich die Speicherung der Sprachwahl und die korrekte Navigation auf dieser Website. Die Speicherdauer beträgt 12 Monate. Rechtsgrundlage für das Setzen des Cookies ist § 25 Abs. 2 TTDSG; die weitere Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Zusätzlich kann derselbe Sprachcode lokal im Browser als localStorage-Eintrag db-lang gespeichert werden. Es findet kein Tracking statt und die Sprachwahl wird nicht an Dritte weitergegeben.",
    ],
    en: [
      "The website provides fixed language versions at /, /pl/ and /en/. When the homepage is accessed, the browser header Accept-Language may be technically evaluated to direct visitors to the appropriate language version. When you choose a language or a language is detected automatically, the technically necessary cookie db-lang may be set with the language code de, en or pl. Its sole purpose is to store the language choice and support correct navigation on this website. The storage period is 12 months. The legal basis for setting the cookie is Section 25(2) TTDSG; further processing is based on Art. 6(1)(f) GDPR. In addition, the same language code may be stored locally in your browser as the localStorage entry db-lang. No tracking takes place and the language choice is not shared with third parties.",
      "The website provides fixed language versions at /, /pl/ and /en/. When you use the language switcher, the technically necessary cookie db-lang may be set with the language code de, en or pl. Its sole purpose is to store the language choice and support correct navigation on this website. The storage period is 12 months. The legal basis for setting the cookie is Section 25(2) TTDSG; further processing is based on Art. 6(1)(f) GDPR. In addition, the same language code may be stored locally in your browser as the localStorage entry db-lang. No tracking takes place and the language choice is not shared with third parties.",
    ],
    pl: [
      "Strona udostępnia stałe wersje językowe pod adresami /, /pl/ i /en/. Przy wejściu na stronę główną nagłówek przeglądarki Accept-Language może zostać technicznie oceniony, aby skierować odwiedzających do odpowiedniej wersji językowej. Po wyborze języka albo po automatycznym rozpoznaniu języka może zostać ustawiony technicznie niezbędny plik cookie db-lang z kodem języka de, en albo pl. Służy on wyłącznie do zapisania wyboru języka i prawidłowej nawigacji na tej stronie. Okres przechowywania wynosi 12 miesięcy. Podstawą prawną ustawienia cookie jest § 25 ust. 2 TTDSG; dalsze przetwarzanie odbywa się na podstawie art. 6 ust. 1 lit. f RODO. Dodatkowo ten sam kod języka może zostać zapisany lokalnie w przeglądarce jako wpis localStorage db-lang. Nie odbywa się śledzenie, a wybór języka nie jest przekazywany osobom trzecim.",
      "Strona udostępnia stałe wersje językowe pod adresami /, /pl/ i /en/. Po użyciu przełącznika języka może zostać ustawiony technicznie niezbędny plik cookie db-lang z kodem języka de, en albo pl. Służy on wyłącznie do zapisania wyboru języka i prawidłowej nawigacji na tej stronie. Okres przechowywania wynosi 12 miesięcy. Podstawą prawną ustawienia cookie jest § 25 ust. 2 TTDSG; dalsze przetwarzanie odbywa się na podstawie art. 6 ust. 1 lit. f RODO. Dodatkowo ten sam kod języka może zostać zapisany lokalnie w przeglądarce jako wpis localStorage db-lang. Nie odbywa się śledzenie, a wybór języka nie jest przekazywany osobom trzecim.",
    ],
  };
  const [before, after] = replacements[lang] || [];
  return before ? html.replace(before, after) : html;
}

function patchHead(head, lang, style = "") {
  let next = head
    .replace(/\n?<script>window\.__DB_DEFAULT_LANG=[\s\S]*?<\/script>/g, "")
    .replace(/\n?<script src="\/assets\/bundle\/[^"]+"><\/script>/g, "")
    .replace(/\n?<meta property="og:locale" content="[^"]+">/g, "")
    .replace(/\n?<script src="\/assets\/site\.js" defer><\/script>/g, "");

  next = next.replace(
    /(<meta property="og:type" content="website">)/,
    `$1\n<meta property="og:locale" content="${OG_LOCALE[lang]}">`,
  );

  const styleTag = style ? `\n<style>\n${style}\n</style>` : "";
  return next.replace("</head>", `${styleTag}\n<script src="/assets/site.js" defer></script>\n</head>`);
}

async function renderDynamicPage(page, lang, source) {
  const xdc = extractXdc(source);
  if (!xdc) throw new Error(`No <x-dc> template in ${sourcePath(page, lang)}`);

  const dataScript = extractDataScript(source);
  const data = evaluateLiteral(dataScript, "DATA");
  const meta = evaluateLiteral(dataScript, "META");
  const values = initialValues(page, lang, data, meta);

  const style = extractHelmetStyle(xdc);
  const head = patchHead(extractHead(source), lang, style);
  const template = prepareTemplate(xdc, page);
  const rendered = postprocessBody(renderTemplate(template, values), page, lang);
  const html = `${source.slice(0, source.indexOf("<head>"))}${head}\n<body>\n${rendered}\n</body>\n</html>\n`;
  return html;
}

async function renderStaticPage(page, lang, source) {
  let html = source
    .replace(/\s+onclick="document\.cookie='db-lang=([a-z]+); Path=\/; Max-Age=31536000; SameSite=Lax; Secure';"/g, ' data-lang-link="$1"')
    .replace(/\s+onclick="this\.closest\('details'\)\.removeAttribute\('open'\)"/g, " data-close-menu");

  if (page.kind === "privacy") html = patchPrivacyCopy(html, lang);

  const beforeHead = html.slice(0, html.indexOf("<head>"));
  const afterHead = html.slice(html.indexOf("</head>") + "</head>".length);
  const head = patchHead(extractHead(html), lang);
  return `${beforeHead}${head}${afterHead}`;
}

function validateRendered(html, page, lang) {
  const needles = ["{{", "<x-dc", "</x-dc", "<sc-for", "<sc-if", "data-dc-script", "/assets/bundle/"];
  const found = needles.filter((needle) => html.includes(needle));
  if (found.length) {
    throw new Error(`${routeFor(page, lang)} still contains ${found.join(", ")}`);
  }
}

async function copyIfExists(from, to) {
  if (!fs.existsSync(from)) return;
  await fsp.mkdir(path.dirname(to), { recursive: true });
  const stat = await fsp.stat(from);
  if (stat.isDirectory()) {
    await fsp.cp(from, to, { recursive: true });
  } else {
    await fsp.copyFile(from, to);
  }
}

async function copyAssets() {
  await copyIfExists(path.join(ROOT, "_headers"), path.join(DIST, "_headers"));
  await copyIfExists(path.join(ROOT, "favicon.ico"), path.join(DIST, "favicon.ico"));
  await copyIfExists(path.join(ROOT, "assets", "fonts"), path.join(DIST, "assets", "fonts"));
  await copyIfExists(path.join(ROOT, "assets", "redesign"), path.join(DIST, "assets", "redesign"));
  await copyIfExists(path.join(ROOT, "assets", "brand-icon.svg"), path.join(DIST, "assets", "brand-icon.svg"));
  await copyIfExists(path.join(ROOT, "assets", "og-image.png"), path.join(DIST, "assets", "og-image.png"));
  await copyIfExists(path.join(ROOT, "assets", "og-image.svg"), path.join(DIST, "assets", "og-image.svg"));
  await copyIfExists(path.join(ROOT, "assets", "site.js"), path.join(DIST, "assets", "site.js"));
}

function sitemap() {
  const urls = [];
  for (const page of ROUTE_GROUPS) {
    for (const lang of LANGS) {
      const alternates = LANGS.map(
        (code) => `    <xhtml:link rel="alternate" hreflang="${code}" href="${SITE}${routeFor(page, code)}" />`,
      ).join("\n");
      urls.push(`  <url>
    <loc>${SITE}${routeFor(page, lang)}</loc>
    <lastmod>${LASTMOD}</lastmod>
${alternates}
    <xhtml:link rel="alternate" hreflang="x-default" href="${SITE}${routeFor(page, "de")}" />
  </url>`);
    }
  }

  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urls.join("\n")}
</urlset>
`;
}

async function writeSupportFiles() {
  await fsp.writeFile(path.join(DIST, "robots.txt"), `User-agent: *\nAllow: /\n\nSitemap: ${SITE}/sitemap.xml\n`, "utf8");
  await fsp.writeFile(path.join(DIST, "sitemap.xml"), sitemap(), "utf8");
}

async function writePages() {
  const missingImages = new Set();

  for (const page of ROUTE_GROUPS) {
    for (const lang of LANGS) {
      const sourceFile = sourcePath(page, lang);
      const source = await fsp.readFile(sourceFile, "utf8");
      const html = extractXdc(source)
        ? await renderDynamicPage(page, lang, source)
        : await renderStaticPage(page, lang, source);

      validateRendered(html, page, lang);

      if (page.kind === "projects") {
        const meta = evaluateLiteral(extractDataScript(source), "META") || [];
        meta.filter((item) => !item.img).forEach((item) => missingImages.add(item.num));
      }

      const output = outputPath(page, lang);
      await fsp.mkdir(path.dirname(output), { recursive: true });
      await fsp.writeFile(output, html, "utf8");
    }
  }

  if (missingImages.size) {
    console.warn(`[build] Case cards without final image: ${[...missingImages].sort().join(", ")}`);
  } else {
    console.log("[build] Case cards without final image: none");
  }
}

async function main() {
  await fsp.rm(DIST, { recursive: true, force: true });
  await fsp.mkdir(DIST, { recursive: true });
  await copyAssets();
  await writePages();
  await writeSupportFiles();
  console.log(`[build] Static site written to ${path.relative(ROOT, DIST)}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
