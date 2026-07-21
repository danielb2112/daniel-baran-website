(() => {
  const LANGUAGE_COOKIE_MAX_AGE = 31536000;
  const FORM_MESSAGES = {
    de: {
      required: "Bitte füllen Sie alle Pflichtfelder aus und wählen Sie mindestens ein Thema.",
      sending: "Sende Anfrage ...",
      success: "Danke. Ihre Anfrage wurde gesendet. Ich melde mich innerhalb von zwei Werktagen.",
      server: "Die Anfrage konnte nicht gesendet werden. Bitte versuchen Sie es später erneut oder schreiben Sie direkt per E-Mail.",
    },
    en: {
      required: "Please fill in all required fields and select at least one topic.",
      sending: "Sending inquiry ...",
      success: "Thank you. Your inquiry has been sent. I'll get back to you within two working days.",
      server: "The inquiry could not be sent. Please try again later or email me directly.",
    },
    pl: {
      required: "Proszę wypełnić wszystkie pola obowiązkowe i wybrać co najmniej jeden temat.",
      sending: "Wysyłam zapytanie ...",
      success: "Dziękuję. Zapytanie zostało wysłane. Odezwę się w ciągu dwóch dni roboczych.",
      server: "Nie udało się wysłać zapytania. Proszę spróbować później albo napisać bezpośrednio e-mailem.",
    },
  };

  const lang = () => document.documentElement.lang || "de";
  const messages = () => FORM_MESSAGES[lang()] || FORM_MESSAGES.de;

  function setLanguageChoice(code) {
    if (!/^(de|en|pl)$/.test(code)) return;
    try {
      localStorage.setItem("db-lang", code);
    } catch {
      // localStorage can be disabled; links still navigate normally.
    }
    document.cookie = `db-lang=${code}; Path=/; Max-Age=${LANGUAGE_COOKIE_MAX_AGE}; SameSite=Lax; Secure`;
  }

  function closeMobileMenu(link) {
    const menu = link.closest("details");
    if (menu) menu.removeAttribute("open");
  }

  function initGlobalClicks() {
    document.addEventListener("click", (event) => {
      const languageLink = event.target.closest("[data-lang-link]");
      if (languageLink) setLanguageChoice(languageLink.dataset.langLink);

      const closeLink = event.target.closest("[data-close-menu]");
      if (closeLink) closeMobileMenu(closeLink);
    });
  }

  function initAccordions() {
    document.querySelectorAll(".acc-button").forEach((button) => {
      const heading = button.closest("h1, h2, h3, h4, h5, h6");
      const panel = button.nextElementSibling || heading?.nextElementSibling;
      const icon = button.lastElementChild;
      if (!panel) return;

      button.addEventListener("click", () => {
        const isOpen = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", String(!isOpen));
        panel.style.gridTemplateRows = isOpen ? "0fr" : "1fr";
        if (icon) icon.style.transform = isOpen ? "rotate(0deg)" : "rotate(45deg)";
      });
    });
  }

  function updateTopicButton(button, selected) {
    button.setAttribute("aria-pressed", String(selected));
    button.style.color = selected ? "#0D0D0C" : "#4A4945";
    button.style.fontWeight = selected ? "500" : "400";
    const mark = button.querySelector("span:first-child");
    const label = button.querySelector("span:last-child");
    if (mark) mark.textContent = selected ? "×" : "+";
    if (label) label.style.borderBottomColor = selected ? "#0D0D0C" : "transparent";
  }

  function updateBudgetButton(button, selected) {
    button.setAttribute("aria-pressed", String(selected));
    button.style.color = selected ? "#0D0D0C" : "#4A4945";
    button.style.fontWeight = selected ? "500" : "400";
    button.style.borderBottomColor = selected ? "#0D0D0C" : "transparent";
  }

  function initContactForm() {
    const form = document.querySelector("form[data-contact-form]");
    if (!form) return;

    const selectedTopics = new Set();
    let selectedBudget = null;
    const topicButtons = Array.from(form.querySelectorAll("[data-topic]"));
    const budgetButtons = Array.from(form.querySelectorAll("[data-budget]"));
    const message = form.querySelector("[data-form-message]");
    const submit = form.querySelector('button[type="submit"]');

    function setMessage(text, ok = false) {
      if (!message) return;
      message.textContent = text;
      message.style.color = ok ? "#0D0D0C" : "#4A4945";
    }

    topicButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const id = button.dataset.topic;
        if (selectedTopics.has(id)) selectedTopics.delete(id);
        else selectedTopics.add(id);
        updateTopicButton(button, selectedTopics.has(id));
        setMessage("");
      });
    });

    budgetButtons.forEach((button) => {
      button.addEventListener("click", () => {
        selectedBudget = button.dataset.budget;
        budgetButtons.forEach((candidate) => updateBudgetButton(candidate, candidate === button));
        setMessage("");
      });
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const m = messages();
      const who = form.elements.who.value.trim();
      const email = form.elements.email.value.trim();
      const context = form.elements.context.value.trim();
      const privacy = form.elements.privacy.checked;
      const website = form.elements.website ? form.elements.website.value : "";
      const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      if (!who || !validEmail || !context || !selectedBudget || selectedTopics.size === 0 || !privacy) {
        setMessage(m.required);
        return;
      }

      if (submit) submit.disabled = true;
      setMessage(m.sending);

      try {
        const response = await fetch("/api/contact", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            who,
            email,
            context,
            budget: selectedBudget,
            topics: [...selectedTopics],
            privacy,
            website,
          }),
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.ok) throw new Error(data.error || "Request failed");

        form.reset();
        selectedTopics.clear();
        selectedBudget = null;
        topicButtons.forEach((button) => updateTopicButton(button, false));
        budgetButtons.forEach((button) => updateBudgetButton(button, false));
        setMessage(m.success, true);
      } catch {
        setMessage(m.server);
      } finally {
        if (submit) submit.disabled = false;
      }
    });
  }

  function scrollToHash() {
    if (!window.location.hash) return;
    let id = window.location.hash.slice(1);
    try {
      id = decodeURIComponent(id);
    } catch {
      // Keep the raw hash if decoding fails.
    }
    const target = document.getElementById(id);
    if (target) target.scrollIntoView({ block: "start" });
  }

  function initReveal() {
    const elements = document.querySelectorAll("[data-reveal]");
    if (!elements.length) return;

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce || !("IntersectionObserver" in window)) {
      elements.forEach((element) => {
        element.style.opacity = "1";
      });
      return;
    }

    const ease = "cubic-bezier(0.62,0.05,0.01,0.99)";
    elements.forEach((element) => {
      element.style.clipPath = "inset(8% 0 8% 0)";
      element.style.transform = "scale(1.06)";
      element.style.opacity = "0.001";
      element.style.transition = `clip-path 1s ${ease}, transform 1s ${ease}, opacity 0.6s ${ease}`;
    });

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.style.clipPath = "inset(0 0 0 0)";
          entry.target.style.transform = "scale(1)";
          entry.target.style.opacity = "1";
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.08 },
    );

    elements.forEach((element) => observer.observe(element));
  }

  function initCaseTrack() {
    const root = document.querySelector(".case-root");
    const track = document.querySelector(".case-track");
    const panels = document.querySelector(".panels");
    const wraps = Array.from(document.querySelectorAll(".panel-wrap"));
    if (!root || !track || !panels || wraps.length < 2) return;

    const counter = document.querySelector(".case-counter");
    const buttons = Array.from(document.querySelectorAll(".case-hud button"));
    const mobile = window.matchMedia("(max-width: 767px)");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
    const count = wraps.length;
    let noTrack = true;
    let progress = 0;
    let painted = false;

    function applyMode() {
      noTrack = mobile.matches || reduce.matches;
      root.classList.toggle("no-track", noTrack);
      track.style.height = noTrack ? "auto" : `${count * 100}vh`;
      if (noTrack) {
        panels.style.transform = "none";
        wraps.forEach((wrap) => wrap.classList.add("in-view"));
      }
    }

    function currentPanel() {
      return Math.round(progress * (count - 1));
    }

    function goTo(index) {
      if (noTrack) return;
      const next = Math.max(0, Math.min(count - 1, index));
      const scrollable = track.offsetHeight - window.innerHeight;
      const top = track.offsetTop + next * (scrollable / (count - 1));
      window.scrollTo({ top, behavior: "smooth" });
    }

    function tick() {
      if (!noTrack) {
        const scrollable = track.offsetHeight - window.innerHeight;
        const nextProgress = scrollable > 0
          ? Math.max(0, Math.min(1, (window.scrollY - track.offsetTop) / scrollable))
          : 0;

        if (nextProgress !== progress || !painted) {
          painted = true;
          progress = nextProgress;
          const introFrac = Math.max(0, 1 - (progress * (count - 1)) / 0.4);
          const pctVal = introFrac * 48 - progress * (count - 1) * 100;
          panels.style.transform = `translateX(calc(${pctVal}% - ${progress * (count - 1) * 6}vw))`;
          const position = progress * (count - 1);
          wraps.forEach((wrap, index) => {
            if (!wrap.classList.contains("in-view") && position > index - 0.5) wrap.classList.add("in-view");
          });
          if (counter) counter.textContent = `${Math.round(position) + 1} / ${count}`;
        }
      }
      window.requestAnimationFrame(tick);
    }

    buttons[0]?.addEventListener("click", () => goTo(currentPanel() - 1));
    buttons[1]?.addEventListener("click", () => goTo(currentPanel() + 1));

    window.addEventListener("keydown", (event) => {
      if (noTrack) return;
      const rect = track.getBoundingClientRect();
      if (!(rect.top < window.innerHeight && rect.bottom > 0)) return;
      if (event.key === "ArrowRight") {
        event.preventDefault();
        goTo(currentPanel() + 1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        goTo(currentPanel() - 1);
      }
    });

    mobile.addEventListener("change", applyMode);
    reduce.addEventListener("change", applyMode);
    applyMode();
    window.requestAnimationFrame(tick);
  }

  document.addEventListener("DOMContentLoaded", () => {
    initGlobalClicks();
    initAccordions();
    initContactForm();
    initReveal();
    initCaseTrack();
    window.setTimeout(scrollToHash, 0);
    window.setTimeout(scrollToHash, 250);
  });
})();
