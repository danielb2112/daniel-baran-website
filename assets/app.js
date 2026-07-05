// Edit these placeholders before launch.
const AVAILABLE_FROM = "[DATUM]";
const LINKEDIN_URL = "[LINKEDIN_URL]";
const EMAIL = "kontakt@daniel-baran.com";
const PHONE = "[+48 ...]";

const BRANDS = ["ARD", "SWR", "Warner Bros. Discovery Sports", "Vestium", "Adastra Studios", "Volkswagen Group", "UCI Track Champions League"];
const TOOL_CHIPS = {
  project: ["Jira", "Confluence", "Scrum", "Kanban", "OKR", "Roadmapping"],
  cloud: ["AWS Serverless", "HLS/DASH", "Transcoding", "GitLab CI/CD"],
  ai: ["Generative AI", "LangGraph", "RAG", "LLM-Routing (Ollama/API)", "Prompt Engineering", "Recommendation Engines", "KI-Tool-Evaluation"],
  collab: ["Miro", "Figma", "Microsoft 365", "Slack", "Teams"]
};

const COPY = {
  de: {
    nav: { profile: "Profil", services: "Leistungen", projects: "Stationen & Projekte", contact: "Kontakt" },
    hero: {
      eyebrow: "Freelance · IT- & Product-Delivery · KI-Enablement",
      h1a: "Ich bringe komplexe",
      h1b: "IT-Projekte",
      h1c: "und die Menschen dahinter",
      h1d: "in Einklang.",
      sub: "Senior-Freelancer für IT-Projektmanagement und Product Ownership — von Enterprise-IT über Public Broadcasting bis zum Startup. Am stärksten dort, wo mehrere Systeme, Teams und Interessen zusammenfinden müssen.",
      statusPrefix: "Verfügbar ab",
      location: "Poznań, PL · Remote in Europa",
      ctaPrimary: "Projekt besprechen",
      ctaSecondary: "Projekte ansehen",
      scroll: "Scrollen"
    },
    portrait: { alt: "Porträt von Daniel Baran", caption: "IT-Projekte · Produkte · KI · Menschen" },
    marquee: {
      label: "Projekte & Marken",
      roles: "IT-Projektmanagement — Product Ownership — KI-Enablement — Cloud & Streaming —"
    },
    stats: {
      s1: "Jahre Projektverantwortung",
      s2: "Branchen",
      s2sub: "Automotive · Medien · Entertainment · Fashion-Tech",
      s3: "Sprachen",
      s4val: "Konzern bis Startup",
      s4: "Beide Welten aus erster Hand"
    },
    sections: { profile: "Profil", services: "Leistungen", projects: "Stationen & Projekte", toolkit: "Toolkit & Methoden", contact: "Kontakt" },
    profile: {
      lead: "Seit über vier Jahren verbinde ich Technik, Produkt und Business — und übersetze zwischen Engineering und Fachbereich, zwischen Konzern und Startup, zwischen Disziplinen.",
      body: "Ob serverlose Streaming-Infrastruktur für Millionen Nutzer:innen, eine KI-Empfehlungsengine in Produktion oder das erste Web3-Metaverse-Event für Warner Bros. Discovery Sports — meine Rolle ist es, viele bewegliche Teile in eine Richtung zu bringen und Projekte verlässlich in Produktion zu führen. Über Abteilungs- und Unternehmensgrenzen hinweg.",
      principle: "Mein Arbeitsprinzip: lieber richtig bauen, auch wenn es länger dauert."
    },
    services: {
      title: "Wobei ich Teams am meisten helfe.",
      items: [
        ["Technisches Projekt- & Programm-Management", "Von der Bedarfsaufnahme bis zum Rollout: Ich steuere Projekte über Abteilungs- und Unternehmensgrenzen hinweg, richte Stakeholder aus und schaffe Prozesse, die auch einer Revision standhalten.", ["Stakeholder", "Rollout", "Governance"]],
        ["Product Ownership", "Ich verantworte digitale Produkte end-to-end — von cloud-nativer, serverloser Architektur bis zum Backlog, der Wert liefert und in Produktion geht.", ["Backlog", "Discovery", "Delivery"]],
        ["KI-Enablement & Generative AI", "Ich bringe KI vom Prototyp in den Produktivbetrieb und befähige Teams, Generative AI in Produkt, Strategie und Betrieb sinnvoll einzusetzen.", ["GenAI", "Prototyping", "Enablement"]],
        ["Cloud- & Streaming-Delivery", "Serverlose AWS-Services, HLS/DASH-Streaming und Transcoding-Pipelines — skalierbar, beobachtbar und produktionsreif aufgesetzt.", ["AWS Serverless", "HLS/DASH", "Transcoding"]]
      ]
    },
    projects: {
      title: "Ausgewählte Projekte.",
      items: [
        ["A", "", "", "Streaming-Infrastruktur im Millionenmaßstab", "Cloud-nativer, serverloser AWS-Service zur HLS/DASH-Manifest-Modifikation — im Live-Betrieb der ARD-Mediathek. Dazu ein zentrales Transcoding-System für VOD und Live.", "Im Live-Betrieb der ARD-Mediathek"],
        ["B", "", "", "KI-Empfehlungsengine in Produktion", "Ein 9-köpfiges Team von manueller redaktioneller Kuration zu einer KI-gestützten Empfehlungsengine geführt — live in Produktion, im Rahmen des SWR AI Hub.", "9-Personen-Team"],
        ["C", "", "", "Erstes Web3-Metaverse-Event", "Umsetzung des ersten Web3-Metaverse-Events der UCI Track Champions League. Zuvor die Burning-Man-VR-Experience mit einem interdisziplinären Team von bis zu 30 Personen.", "Internationale Teams"],
        ["D", "", "", "Fashion-Tech mit 3D-Avataren", "Fashion-Tech-Startup für virtuelle Anprobe per 3D-Scan-Avataren mitgegründet. Als Co-Founder ein 8-köpfiges Team für 3D-Rendering und Echtzeit-Visualisierung aufgebaut und geführt.", "8-köpfiges Team"],
        ["E", "", "", "Konzern-Schnittstelle MAN ↔ Volkswagen", "Steuerung der Schnittstelle zwischen MAN und Volkswagen für das weltweite MAN-TGE-After-Sales-Programm — inkl. Aufbau einer globalen Support-Funktion und Integration von Fahrzeugdaten aus Konzernsystemen.", "Weltweiter Rollout"],
        ["F", "EIGENPROJEKT", "Architekt & Entwickler", "Multi-Agent-KI-System in Eigenentwicklung", "Produktionsreifes Multi-Agent-System selbst gebaut: LangGraph-Orchestrierung, hybrides LLM-Routing (lokal + Cloud), RAG-Memory und Freigabe-Workflows per Telegram. Weil ich KI-Projekte besser steuere, wenn ich sie auch selbst bauen kann.", "LangGraph · RAG · HITL"]
      ]
    },
    toolkit: {
      title: "Womit ich arbeite.",
      groups: ["Projekt & Produkt", "Cloud-Architektur", "Künstliche Intelligenz", "Collaboration & Design"],
      languagesLabel: "Sprachen",
      languages: "Deutsch (Muttersprache) · Polnisch (C1, fließend) · Englisch (fließend)",
      certLabel: "Zertifizierungen",
      certifications: "Certified Product Management Expert (XDi) · Generative AI & GPAI (Bitkom) · AI for Business (Wharton Online) · Google Project Management (Coursera) · Technischer Fachwirt (IHK, Abschluss 12/2026)"
    },
    contact: {
      lead: "Ein Projekt, das viele Systeme und Stakeholder verbindet?",
      accent: "Sprechen wir darüber.",
      statusPrefix: "Verfügbar für neue Projekte ab",
      phoneLabel: "Telefon",
      locationLabel: "Standort",
      location: "Poznań, Polen · Remote in Europa",
      languagesLabel: "Sprachen",
      linkedin: "Profil öffnen ↗"
    },
    footer: { role: "Freelance IT- & Product-Delivery", legal: "Impressum", privacy: "Datenschutz" }
  },
  pl: {
    nav: { profile: "Profil", services: "Usługi", projects: "Doświadczenie i projekty", contact: "Kontakt" },
    hero: {
      eyebrow: "Freelance · IT i Product Delivery · Wdrażanie AI",
      h1a: "Łączę złożone",
      h1b: "projekty IT",
      h1c: "i stojących za nimi ludzi",
      h1d: "w jedną całość.",
      sub: "Senior freelancer w obszarze zarządzania projektami IT i product ownership — od IT w korporacjach, przez media publiczne, po startupy. Najskuteczniejszy tam, gdzie wiele systemów, zespołów i interesów musi się spotkać.",
      statusPrefix: "Dostępny od",
      location: "Poznań, PL · Zdalnie w Europie",
      ctaPrimary: "Omówmy projekt",
      ctaSecondary: "Zobacz projekty",
      scroll: "Przewiń"
    },
    portrait: { alt: "Portret Daniela Barana", caption: "Projekty IT · Produkty · AI · Ludzie" },
    marquee: { label: "Projekty i marki", roles: "Zarządzanie projektami IT — Product Ownership — Wdrażanie AI — Cloud i Streaming —" },
    stats: { s1: "Lata odpowiedzialności za projekty", s2: "Branże", s2sub: "Automotive · Media · Entertainment · Fashion-tech", s3: "Języki", s4val: "Od korporacji po startup", s4: "Oba światy z pierwszej ręki" },
    sections: { profile: "Profil", services: "Usługi", projects: "Doświadczenie i projekty", toolkit: "Narzędzia i metody", contact: "Kontakt" },
    profile: {
      lead: "Od ponad czterech lat łączę technologię, produkt i biznes — tłumacząc między inżynierią a biznesem, między korporacją a startupem, między dyscyplinami.",
      body: "Czy to bezserwerowa infrastruktura streamingowa dla milionów użytkowników, silnik rekomendacji AI w produkcji, czy pierwsze wydarzenie w metaverse Web3 dla Warner Bros. Discovery Sports — moją rolą jest ustawić wiele ruchomych elementów w jednym kierunku i niezawodnie doprowadzić projekty do produkcji. Ponad granicami działów i firm.",
      principle: "Moja zasada pracy: lepiej budować porządnie, nawet jeśli trwa to dłużej."
    },
    services: {
      title: "W czym najbardziej pomagam zespołom.",
      items: [
        ["Techniczne zarządzanie projektami i programami", "Od zbierania wymagań po wdrożenie: prowadzę projekty ponad granicami działów i firm, koordynuję interesariuszy i tworzę procesy, które wytrzymają każdą kontrolę.", ["Stakeholder", "Rollout", "Governance"]],
        ["Product ownership", "Odpowiadam za produkty cyfrowe end-to-end — od chmurowej, bezserwerowej architektury po backlog, który dostarcza wartość i trafia na produkcję.", ["Backlog", "Discovery", "Delivery"]],
        ["Wdrażanie AI i generatywna AI", "Przeprowadzam AI od prototypu do produkcji i wspieram zespoły we wdrażaniu generatywnej AI w produkcie, strategii i operacjach.", ["GenAI", "Prototyping", "Enablement"]],
        ["Cloud i streaming delivery", "Bezserwerowe usługi AWS, streaming HLS/DASH i pipeline'y transkodowania — skalowalne, obserwowalne i gotowe na produkcję.", ["AWS Serverless", "HLS/DASH", "Transcoding"]]
      ]
    },
    projects: {
      title: "Wybrane projekty.",
      items: [
        ["A", "", "", "Infrastruktura streamingowa w skali milionów", "Chmurowa, bezserwerowa usługa AWS do modyfikacji manifestów HLS/DASH — działająca na żywo w ARD Mediathek. Do tego centralny system transkodowania dla VOD i live.", "Na żywo w ARD Mediathek"],
        ["B", "", "", "Silnik rekomendacji AI na produkcji", "Poprowadziłem 9-osobowy zespół od ręcznej kuracji redakcyjnej do silnika rekomendacji opartego na AI — na żywo na produkcji, w ramach SWR AI Hub.", "9-osobowy zespół"],
        ["C", "", "", "Pierwsze wydarzenie w metaverse Web3", "Realizacja pierwszego wydarzenia w metaverse Web3 dla UCI Track Champions League. Wcześniej Burning Man VR z interdyscyplinarnym zespołem do 30 osób.", "Zespoły międzynarodowe"],
        ["D", "", "", "Fashion-tech z awatarami 3D", "Współzałożyciel startupu fashion-tech do wirtualnej przymiarki z awatarami ze skanów 3D. Zbudowałem i poprowadziłem 8-osobowy zespół ds. renderingu 3D i wizualizacji w czasie rzeczywistym.", "8-osobowy zespół"],
        ["E", "", "", "Interfejs korporacyjny MAN ↔ Volkswagen", "Zarządzanie interfejsem między MAN a Volkswagenem dla globalnego programu posprzedażowego MAN TGE — w tym budowa globalnej funkcji wsparcia i integracja danych pojazdów z systemów koncernu.", "Globalny rollout"],
        ["F", "PROJEKT WŁASNY", "Architekt i deweloper", "Autorski system multi-agentowy AI", "Samodzielnie zbudowany, gotowy na produkcję system multi-agentowy: orkiestracja LangGraph, hybrydowy routing LLM (lokalnie + chmura), pamięć RAG i workflow zatwierdzeń przez Telegram. Bo lepiej prowadzę projekty AI, kiedy potrafię je też sam zbudować.", "LangGraph · RAG · HITL"]
      ]
    },
    toolkit: {
      title: "Z czego korzystam.",
      groups: ["Projekt i produkt", "Architektura chmury", "Sztuczna inteligencja", "Współpraca i design"],
      languagesLabel: "Języki",
      languages: "Niemiecki (ojczysty) · Polski (C1, biegły) · Angielski (biegły)",
      certLabel: "Certyfikaty",
      certifications: "Certified Product Management Expert (XDi) · Generative AI & GPAI (Bitkom) · AI for Business (Wharton Online) · Google Project Management (Coursera) · Technischer Fachwirt (IHK, ukończenie 12/2026)"
    },
    contact: { lead: "Projekt, który łączy wiele systemów i interesariuszy?", accent: "Porozmawiajmy.", statusPrefix: "Dostępny dla nowych projektów od", phoneLabel: "Telefon", locationLabel: "Lokalizacja", location: "Poznań, Polska · Zdalnie w Europie", languagesLabel: "Języki", linkedin: "Otwórz profil ↗" },
    footer: { role: "Freelance IT i product delivery", legal: "Nota prawna", privacy: "Polityka prywatności" }
  },
  en: {
    nav: { profile: "Profile", services: "Services", projects: "Roles & projects", contact: "Contact" },
    hero: {
      eyebrow: "Freelance · IT & Product Delivery · AI Enablement",
      h1a: "I bring complex",
      h1b: "IT projects",
      h1c: "and the people behind them",
      h1d: "into alignment.",
      sub: "Senior freelancer for IT project management and product ownership — from enterprise IT through public broadcasting to startups. Strongest where multiple systems, teams and interests have to come together.",
      statusPrefix: "Available from",
      location: "Poznań, PL · Remote across Europe",
      ctaPrimary: "Discuss a project",
      ctaSecondary: "See the work",
      scroll: "Scroll"
    },
    portrait: { alt: "Portrait of Daniel Baran", caption: "IT projects · Products · AI · People" },
    marquee: { label: "Projects & brands", roles: "IT project management — Product ownership — AI enablement — Cloud & streaming —" },
    stats: { s1: "Years of project responsibility", s2: "Industries", s2sub: "Automotive · Media · Entertainment · Fashion tech", s3: "Languages", s4val: "Corporate to startup", s4: "Both worlds first-hand" },
    sections: { profile: "Profile", services: "Services", projects: "Roles & projects", toolkit: "Toolkit & methods", contact: "Contact" },
    profile: {
      lead: "For over four years I've been connecting technology, product and business — translating between engineering and the business side, between corporations and startups, between disciplines.",
      body: "Whether serverless streaming infrastructure for millions of users, an AI recommendation engine in production, or the first Web3 metaverse event for Warner Bros. Discovery Sports — my role is to move many moving parts in one direction and take projects reliably into production. Across department and company boundaries.",
      principle: "My working principle: build it right, even if it takes longer."
    },
    services: {
      title: "Where I help teams most.",
      items: [
        ["Technical project & programme management", "From demand intake to rollout: I steer projects across department and company boundaries, align stakeholders and establish processes that hold up under review.", ["Stakeholder", "Rollout", "Governance"]],
        ["Product ownership", "I own digital products end-to-end — from cloud-native, serverless architecture to a backlog that delivers value and ships to production.", ["Backlog", "Discovery", "Delivery"]],
        ["AI enablement & generative AI", "I take AI from prototype into production and enable teams to use generative AI meaningfully across product, strategy and operations.", ["GenAI", "Prototyping", "Enablement"]],
        ["Cloud & streaming delivery", "Serverless AWS services, HLS/DASH streaming and transcoding pipelines — set up to be scalable, observable and production-ready.", ["AWS Serverless", "HLS/DASH", "Transcoding"]]
      ]
    },
    projects: {
      title: "Selected projects.",
      items: [
        ["A", "", "", "Streaming infrastructure at millions scale", "Cloud-native, serverless AWS service for HLS/DASH manifest modification — running live in the ARD Mediathek. Plus a central transcoding system for VOD and live.", "Live in the ARD Mediathek"],
        ["B", "", "", "AI recommendation engine in production", "Led a 9-person team from manual editorial curation to an AI-powered recommendation engine — live in production, as part of the SWR AI Hub.", "9-person team"],
        ["C", "", "", "First Web3 metaverse event", "Delivery of the first Web3 metaverse event for the UCI Track Champions League. Previously the Burning Man VR experience with an interdisciplinary team of up to 30.", "International teams"],
        ["D", "", "", "Fashion-tech with 3D avatars", "Co-founded a fashion-tech startup for virtual try-on using 3D-scan avatars. Built and led an 8-person team for 3D rendering and real-time visualisation.", "8-person team"],
        ["E", "", "", "Enterprise interface MAN ↔ Volkswagen", "Steering the interface between MAN and Volkswagen for the worldwide MAN TGE after-sales programme — including building a global support function and integrating vehicle data from group systems.", "Worldwide rollout"],
        ["F", "OWN PROJECT", "Architect & developer", "Self-built multi-agent AI system", "Built a production-ready multi-agent system myself: LangGraph orchestration, hybrid LLM routing (local + cloud), RAG memory and approval workflows via Telegram. Because I steer AI projects better when I can also build them myself.", "LangGraph · RAG · HITL"]
      ]
    },
    toolkit: {
      title: "What I work with.",
      groups: ["Project & product", "Cloud architecture", "Artificial intelligence", "Collaboration & design"],
      languagesLabel: "Languages",
      languages: "German (native) · Polish (C1, fluent) · English (fluent)",
      certLabel: "Certifications",
      certifications: "Certified Product Management Expert (XDi) · Generative AI & GPAI (Bitkom) · AI for Business (Wharton Online) · Google Project Management (Coursera) · Technischer Fachwirt (IHK, completing 12/2026)"
    },
    contact: { lead: "A project that connects many systems and stakeholders?", accent: "Let's talk.", statusPrefix: "Available for new projects from", phoneLabel: "Phone", locationLabel: "Location", location: "Poznań, Poland · Remote across Europe", languagesLabel: "Languages", linkedin: "Open profile ↗" },
    footer: { role: "Freelance IT & product delivery", legal: "Legal notice", privacy: "Privacy" }
  }
};

function text(path, lang) {
  return path.split(".").reduce((obj, key) => obj && obj[key], COPY[lang]) || "";
}

function setText(node, value) {
  node.textContent = value;
}

function renderMarquee(selector, items) {
  const host = document.querySelector(selector);
  if (!host) return;
  const track = document.createElement("div");
  track.className = "marquee-track";
  const doubled = [...items, ...items];
  doubled.forEach((item) => {
    const span = document.createElement("span");
    span.textContent = item;
    const dot = document.createElement("i");
    dot.textContent = "·";
    track.append(span, dot);
  });
  host.replaceChildren(track);
}

function chipRow(chips) {
  const row = document.createElement("div");
  row.className = "chip-row";
  chips.forEach((chip) => {
    const el = document.createElement("span");
    el.className = "chip";
    el.textContent = chip;
    row.append(el);
  });
  return row;
}

function renderServices(lang) {
  const host = document.querySelector("[data-services]");
  if (!host) return;
  host.replaceChildren();
  COPY[lang].services.items.forEach(([title, description, chips], index) => {
    const article = document.createElement("article");
    const num = String(index + 1).padStart(2, "0");
    article.className = "service-item reveal";
    article.dataset.big = num;
    const heading = document.createElement("div");
    heading.className = "service-heading";
    const number = document.createElement("span");
    number.textContent = num;
    const h3 = document.createElement("h3");
    h3.textContent = title;
    heading.append(number, h3);
    const body = document.createElement("div");
    const p = document.createElement("p");
    p.textContent = description;
    body.append(p, chipRow(chips));
    article.append(heading, body);
    host.append(article);
  });
}

function renderProjects(lang) {
  const host = document.querySelector("[data-projects]");
  if (!host) return;
  host.replaceChildren();
  COPY[lang].projects.items.forEach(([letter, label, role, title, description, chip], index) => {
    const article = document.createElement("article");
    article.className = `project-card reveal${index === 5 ? " featured" : ""}`;
    const visual = document.createElement("div");
    visual.className = "project-visual";
    visual.dataset.number = String(index + 1).padStart(2, "0");
    const letterEl = document.createElement("span");
    letterEl.className = "project-letter";
    letterEl.textContent = letter;
    visual.append(letterEl);
    const content = document.createElement("div");
    content.className = "project-content";
    const meta = document.createElement("div");
    meta.className = "project-meta";
    [label, role].filter(Boolean).forEach((item) => {
      const span = document.createElement("span");
      span.textContent = item;
      meta.append(span);
    });
    const h3 = document.createElement("h3");
    h3.textContent = title;
    const p = document.createElement("p");
    p.textContent = description;
    const chipEl = document.createElement("span");
    chipEl.className = "project-chip";
    chipEl.textContent = chip;
    content.append(meta, h3, p, chipEl);
    article.append(visual, content);
    host.append(article);
  });
}

function renderToolkit(lang) {
  const host = document.querySelector("[data-toolkit]");
  if (!host) return;
  host.replaceChildren();
  const groups = [
    [COPY[lang].toolkit.groups[0], TOOL_CHIPS.project],
    [COPY[lang].toolkit.groups[1], TOOL_CHIPS.cloud],
    [COPY[lang].toolkit.groups[2], TOOL_CHIPS.ai],
    [COPY[lang].toolkit.groups[3], TOOL_CHIPS.collab]
  ];
  groups.forEach(([title, chips]) => {
    const group = document.createElement("article");
    group.className = "tool-group reveal";
    const h3 = document.createElement("h3");
    h3.textContent = title;
    group.append(h3, chipRow(chips));
    host.append(group);
  });
}

function applyContactLinks() {
  document.querySelectorAll("[data-email-link]").forEach((link) => {
    link.href = `mailto:${EMAIL}`;
    if (link.textContent.includes("@")) link.textContent = EMAIL;
  });
  document.querySelectorAll("[data-phone-link]").forEach((link) => {
    link.textContent = PHONE;
    link.href = `tel:${PHONE.replace(/[^+0-9]/g, "")}`;
  });
  document.querySelectorAll("[data-linkedin]").forEach((link) => {
    const disabled = LINKEDIN_URL === "[LINKEDIN_URL]" || !LINKEDIN_URL;
    link.href = disabled ? "#" : LINKEDIN_URL;
    link.classList.toggle("is-disabled", disabled);
    link.setAttribute("aria-disabled", disabled ? "true" : "false");
  });
}

function applyLanguage(lang) {
  const safeLang = COPY[lang] ? lang : "de";
  document.documentElement.lang = safeLang;
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = text(node.dataset.i18n, safeLang);
    if (value) setText(node, value);
  });
  document.querySelectorAll("[data-i18n-alt]").forEach((node) => {
    const value = text(node.dataset.i18nAlt, safeLang);
    if (value) node.alt = value;
  });
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.setAttribute("aria-pressed", button.dataset.lang === safeLang ? "true" : "false");
  });
  setText(document.querySelector("[data-i18n='hero.status']"), `${COPY[safeLang].hero.statusPrefix} ${AVAILABLE_FROM}`);
  setText(document.querySelector("[data-i18n='contact.status']"), `${COPY[safeLang].contact.statusPrefix} ${AVAILABLE_FROM}`);
  renderServices(safeLang);
  renderProjects(safeLang);
  renderToolkit(safeLang);
  renderMarquee("[data-marquee='roles']", [COPY[safeLang].marquee.roles]);
  applyContactLinks();
  initReveal();
  localStorage.setItem("lang", safeLang);
}

function initReveal() {
  const items = document.querySelectorAll(".reveal");
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    items.forEach((item) => item.classList.add("is-visible"));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  items.forEach((item) => observer.observe(item));
}

function initProgress() {
  const bar = document.querySelector("[data-progress]");
  if (!bar) return;
  const update = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    const progress = max > 0 ? (window.scrollY / max) * 100 : 0;
    bar.style.width = `${progress}%`;
  };
  update();
  window.addEventListener("scroll", update, { passive: true });
}

document.addEventListener("DOMContentLoaded", () => {
  renderMarquee("[data-marquee='brands']", BRANDS);
  document.querySelectorAll("[data-lang]").forEach((button) => {
    button.addEventListener("click", () => applyLanguage(button.dataset.lang));
  });
  document.querySelector("[data-year]").textContent = new Date().getFullYear();
  const stored = localStorage.getItem("lang");
  applyLanguage(COPY[stored] ? stored : "de");
  initProgress();
});
