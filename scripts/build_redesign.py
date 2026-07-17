#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = Path("/private/tmp/dbredesign.8WlWOo/design_handoff_daniel_baran_website")
RUNTIME = "/assets/bundle/98fbe8e7-3e34-4182-88f6-79233bad489b.js"
SITE = "https://daniel-baran.com"
LINKEDIN = "https://www.linkedin.com/in/daniel-baran-5b14b2269"
LASTMOD = "2026-07-17"
VESTIUM_YOUTUBE_ID = "La4rd4JhlFE"

LANGS = ("de", "en", "pl")

CASE_FILES = {
    "Redesign Case SWR-Empfehlungen.dc.html": "swr-ki-empfehlungsengine",
    "Redesign Case SWR-KI-Testphase.dc.html": "swr-ki-testphase",
    "Redesign Case ARD-Multiplattform.dc.html": "swr-multiplatform-service",
    "Redesign Case ARD-Transcoding.dc.html": "swr-ard-transcoding",
    "Redesign Case Vestium.dc.html": "vestium",
    "Redesign Case Infinite Playa.dc.html": "infinite-playa",
    "Redesign Case UCI-Metaverse.dc.html": "uci-track-champions-league",
    "Redesign Case Systemmigration.dc.html": "systemmigration-konzernverbund",
    "Redesign Case Umbaudokumentation.dc.html": "fahrzeugumbauten-dokumentation",
}

CASE_ORDER = list(CASE_FILES.values())
CASE_SOURCE_BY_SLUG = {slug: source for source, slug in CASE_FILES.items()}

PAGE_SOURCES = {
    "home": "Redesign Startseite v2.dc.html",
    "about": "Redesign Profilseite.dc.html",
    "projects": "Redesign Projekte.dc.html",
}

TITLES = {
    "home": {
        "de": "Daniel Baran - Senior IT Project & Product Manager",
        "en": "Daniel Baran - Senior IT Project & Product Manager",
        "pl": "Daniel Baran - Senior IT Project & Product Manager",
    },
    "about": {
        "de": "Über mich - Daniel Baran",
        "en": "About - Daniel Baran",
        "pl": "O mnie - Daniel Baran",
    },
    "projects": {
        "de": "Projekte - Daniel Baran",
        "en": "Projects - Daniel Baran",
        "pl": "Projekty - Daniel Baran",
    },
}

DESCRIPTIONS = {
    "home": {
        "de": "Senior IT Project & Product Manager für IT-Projekte, digitale Produkte und KI-Enablement im DACH-Raum.",
        "en": "Senior IT Project & Product Manager for IT projects, digital products and AI enablement across DACH.",
        "pl": "Senior IT Project & Product Manager wspierający projekty IT, produkty cyfrowe i wdrażanie AI w regionie DACH.",
    },
    "about": {
        "de": "Profil, Arbeitsweise, Karriere und Toolkit von Daniel Baran.",
        "en": "Profile, working style, career and toolkit of Daniel Baran.",
        "pl": "Profil, sposób pracy, kariera i toolkit Daniela Barana.",
    },
    "projects": {
        "de": "Neun Case Studies aus Medien, KI, Streaming, Startup und Automotive.",
        "en": "Nine case studies from media, AI, streaming, startup and automotive.",
        "pl": "Dziewięć case studies z mediów, AI, streamingu, startupów i motoryzacji.",
    },
}

CASE_TITLES = {
    "swr-ki-empfehlungsengine": "Personalisierte Empfehlungen für die SWR-Website",
    "swr-ki-testphase": "KI-Testphase beim SWR",
    "swr-multiplatform-service": "ARD-Multiplattformservice",
    "swr-ard-transcoding": "Zentrales ARD-Transcoding",
    "vestium": "Vestium",
    "infinite-playa": "The Infinite Playa",
    "uci-track-champions-league": "UCI Track Champions League",
    "systemmigration-konzernverbund": "Systemmigration im Konzernverbund",
    "fahrzeugumbauten-dokumentation": "Dokumentation für Fahrzeugumbauten",
}

FONT_CSS = """    @font-face { font-family:'Space Grotesk'; font-style:normal; font-weight:400; font-display:swap; src:url('/assets/fonts/space-grotesk-400.woff2') format('woff2'); }
    @font-face { font-family:'Space Grotesk'; font-style:normal; font-weight:500; font-display:swap; src:url('/assets/fonts/space-grotesk-500.woff2') format('woff2'); }
"""


def route(kind: str, lang: str, slug: str | None = None) -> str:
    if kind == "home":
        return {"de": "/", "en": "/en/", "pl": "/pl/"}[lang]
    if kind == "about":
        return {"de": "/ueber-mich/", "en": "/en/about/", "pl": "/pl/o-mnie/"}[lang]
    if kind == "projects":
        return {"de": "/projekte/", "en": "/en/projects/", "pl": "/pl/projekty/"}[lang]
    if kind == "imprint":
        return {"de": "/impressum/", "en": "/en/imprint/", "pl": "/pl/nota-prawna/"}[lang]
    if kind == "privacy":
        return {"de": "/datenschutz/", "en": "/en/privacy/", "pl": "/pl/prywatnosc/"}[lang]
    if kind == "case":
        assert slug
        prefix = {"de": "/projekte", "en": "/en/projects", "pl": "/pl/projekty"}[lang]
        return f"{prefix}/{slug}/"
    raise ValueError(kind)


def out_path(kind: str, lang: str, slug: str | None = None) -> Path:
    rel = route(kind, lang, slug).strip("/")
    if not rel:
        return ROOT / "index.html"
    return ROOT / rel / "index.html"


def alt_routes(kind: str, slug: str | None = None) -> dict[str, str]:
    return {lang: route(kind, lang, slug) for lang in LANGS}


def case_next(slug: str) -> str:
    idx = CASE_ORDER.index(slug)
    return CASE_ORDER[(idx + 1) % len(CASE_ORDER)]


def extract_body(source: str) -> str:
    match = re.search(r"<body>(.*)</body>", source, flags=re.S)
    if not match:
        raise ValueError("No body found")
    return match.group(1).strip()


def js_config(lang: str, kind: str, slug: str | None = None) -> str:
    config = {
        "defaultLang": lang,
        "altRoutes": alt_routes(kind, slug),
        "vestiumYouTubeId": VESTIUM_YOUTUBE_ID,
    }
    return (
        "<script>"
        f"window.__DB_DEFAULT_LANG={json.dumps(config['defaultLang'])};"
        f"window.__DB_ALT_ROUTES={json.dumps(config['altRoutes'], ensure_ascii=False)};"
        f"window.__VESTIUM_YOUTUBE_ID={json.dumps(config['vestiumYouTubeId'])};"
        "</script>"
    )


def metadata(kind: str, lang: str, slug: str | None = None) -> tuple[str, str]:
    if kind == "case":
        title = f"{CASE_TITLES[slug]} - Case Study - Daniel Baran"
        desc = "Case Study von Daniel Baran zu Projekt- und Produktarbeit in Medien, Startup, Streaming, KI oder Automotive."
        if lang == "en":
            desc = "Daniel Baran case study covering project and product work in media, startup, streaming, AI or automotive."
        elif lang == "pl":
            desc = "Case study Daniela Barana o pracy projektowej i produktowej w mediach, startupach, streamingu, AI lub motoryzacji."
        return title, desc
    return TITLES[kind][lang], DESCRIPTIONS[kind][lang]


def head(lang: str, kind: str, slug: str | None = None) -> str:
    title, desc = metadata(kind, lang, slug)
    canonical = route(kind, lang, slug)
    alts = alt_routes(kind, slug)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{code}" href="{SITE}{href}">'
        for code, href in alts.items()
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{canonical}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{SITE}{alts['de']}">
<link rel="icon" href="/favicon.ico">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-image.png">
{js_config(lang, kind, slug)}
<script src="{RUNTIME}"></script>
</head>"""


def normalize_fonts(body: str) -> str:
    body = re.sub(r"\s*<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">\n?", "\n", body)
    body = re.sub(r"\s*<link rel=\"preconnect\" href=\"https://fonts\.gstatic\.com\" crossorigin>\n?", "\n", body)
    body = re.sub(r"\s*<link href=\"https://fonts\.googleapis\.com[^\"]+\" rel=\"stylesheet\">\n?", "\n", body)
    body = body.replace("'Archivo'", "'Space Grotesk'")
    body = body.replace("font-family:'Space Grotesk', sans-serif", "font-family:'Space Grotesk', 'Helvetica Neue', Arial, sans-serif")
    body = body.replace("<style>\n", "<style>\n" + FONT_CSS, 1)
    body = re.sub(r"letter-spacing:-0\.[0-9]+em", "letter-spacing:0", body)
    return body


def normalize_assets(body: str) -> str:
    body = body.replace('src="uploads/DSCF5508.jpg"', 'src="/assets/redesign/DSCF5508.jpg"')
    body = body.replace('src="assets/', 'src="/assets/redesign/')
    body = body.replace('img: "assets/', 'img: "/assets/redesign/')
    return body


def replace_links(body: str, lang: str, kind: str, slug: str | None = None) -> str:
    anchors = {
        "Redesign Startseite v2.dc.html#leistungen": route("home", lang) + "#leistungen",
        "Redesign Startseite v2.dc.html#prozess": route("home", lang) + "#prozess",
        "Redesign Startseite v2.dc.html#projekte": route("home", lang) + "#projekte",
        "Redesign Startseite v2.dc.html#kontakt": route("home", lang) + "#kontakt",
        "Redesign Startseite v2.dc.html": route("home", lang),
        "Redesign Profilseite.dc.html": route("about", lang),
        "Redesign Projekte.dc.html": route("projects", lang),
    }
    for file_name, case_slug in CASE_FILES.items():
        anchors[file_name] = route("case", lang, case_slug)

    for old, new in sorted(anchors.items(), key=lambda item: -len(item[0])):
        body = body.replace(f'href="{old}"', f'href="{new}"')
        body = body.replace(f'"{old}"', f'"{new}"')

    if kind in {"about", "projects"}:
        body = body.replace('href="#" aria-current="page"', f'href="{route(kind, lang)}" aria-current="page"')

    body = re.sub(
        r'<a href="#"([^>]*>\{\{ t\.footerLinkedin \}\}</a>)',
        rf'<a href="{LINKEDIN}" target="_blank" rel="noopener"\1',
        body,
    )
    body = re.sub(
        r'<a href="#"([^>]*>\{\{ t\.footerImprint \}\}</a>)',
        rf'<a href="{route("imprint", lang)}"\1',
        body,
    )
    body = re.sub(
        r'<a href="#"([^>]*>\{\{ t\.footerPrivacy \}\}</a>)',
        rf'<a href="{route("privacy", lang)}"\1',
        body,
    )
    body = re.sub(
        r'<a href="#"([^>]*>\{\{ t\.privacyLink \}\}</a>)',
        rf'<a href="{route("privacy", lang)}"\1',
        body,
    )
    return body


def replace_language_state(body: str) -> str:
    old = 'lang: (() => { try { const l = localStorage.getItem("db-lang"); return (l && DATA[l]) ? l : "de"; } catch (e) { return "de"; } })(),'
    new = 'lang: (() => { const d = window.__DB_DEFAULT_LANG; if (d && DATA[d]) return d; try { const l = localStorage.getItem("db-lang"); return (l && DATA[l]) ? l : "de"; } catch (e) { return "de"; } })(),'
    body = body.replace(old, new)

    def set_lang_repl(match: re.Match[str]) -> str:
        state_line = match.group("state")
        return f"""  setLang(code) {{
    if (!DATA[code]) return;
    try {{ localStorage.setItem("db-lang", code); }} catch (e) {{}}
    const target = window.__DB_ALT_ROUTES && window.__DB_ALT_ROUTES[code];
    const current = window.location.pathname.endsWith("/") ? window.location.pathname : window.location.pathname + "/";
    if (target && target !== current) {{
      window.location.href = target;
      return;
    }}
    {state_line}
  }}"""

    body = re.sub(
        r"  setLang\(code\) \{\n    if \(!DATA\[code\]\) return;\n    try \{ localStorage\.setItem\(\"db-lang\", code\); \} catch \(e\) \{\}\n    (?P<state>this\.setState\(\{ lang: code(?:, formMsg: \"\")? \}\);)\n  \}",
        set_lang_repl,
        body,
    )
    return body


def update_home_form(body: str) -> str:
    body = body.replace(
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); display:grid;',
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); position:relative; display:grid;',
    )
    body = body.replace(
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); position:relative; display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr)); gap:clamp(32px,5vw,80px); align-items:start; border-top:1.5px solid #0D0D0C; padding-top:clamp(24px,4vh,40px);">',
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); position:relative; display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr)); gap:clamp(32px,5vw,80px); align-items:start; border-top:1.5px solid #0D0D0C; padding-top:clamp(24px,4vh,40px);">\n'
        '      <input type="text" name="website" autocomplete="off" tabindex="-1" aria-hidden="true" style="position:absolute; left:-10000px; width:1px; height:1px; opacity:0;">',
    )
    body = body.replace(
        '<p style="margin:14px 0 0; font-size:0.85rem; line-height:1.4; color:{{ formMsgColor }}; min-height:1.2em;">{{ formMsg }}</p>',
        '<p aria-live="polite" style="margin:14px 0 0; font-size:0.85rem; line-height:1.4; color:{{ formMsgColor }}; min-height:1.2em;">{{ formMsg }}</p>',
    )
    body = body.replace(
        'openS: [], openP: [], topics: [], budget: null, formMsg: "", formOk: false,',
        'openS: [], openP: [], topics: [], budget: null, formMsg: "", formOk: false, sending: false,',
    )
    old_submit = """submitForm: (e) => {
        e.preventDefault();
        const f = e.target;
        const who = f.who.value.trim(), email = f.email.value.trim(), ctx = f.context.value.trim();
        const ok = who && email && /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email) && ctx && this.state.budget && this.state.topics.length > 0 && f.privacy.checked;
        this.setState({ formOk: ok, formMsg: ok ? L.okMsg : L.errMsg });
      },"""
    new_submit = """submitForm: async (e) => {
        e.preventDefault();
        if (this.state.sending) return;
        const f = e.target;
        const who = f.who.value.trim(), email = f.email.value.trim(), ctx = f.context.value.trim();
        const ok = who && email && /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email) && ctx && this.state.budget && this.state.topics.length > 0 && f.privacy.checked;
        if (!ok) {
          this.setState({ formOk: false, formMsg: L.errMsg });
          return;
        }
        const sendingMsg = { de: "Sende Anfrage ...", en: "Sending inquiry ...", pl: "Wysyłam zapytanie ..." }[lang] || "Sending ...";
        const serverErrMsg = {
          de: "Die Anfrage konnte nicht gesendet werden. Bitte versuchen Sie es später erneut oder schreiben Sie direkt per E-Mail.",
          en: "The inquiry could not be sent. Please try again later or email me directly.",
          pl: "Nie udało się wysłać zapytania. Proszę spróbować później albo napisać bezpośrednio e-mailem.",
        }[lang] || L.errMsg;
        this.setState({ sending: true, formOk: false, formMsg: sendingMsg });
        try {
          const response = await fetch("/api/contact", {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({
              who,
              email,
              context: ctx,
              budget: this.state.budget,
              topics: this.state.topics,
              privacy: f.privacy.checked,
              website: f.website ? f.website.value : "",
            }),
          });
          const data = await response.json().catch(() => ({}));
          if (!response.ok || !data.ok) throw new Error(data.error || "Request failed");
          f.reset();
          this.setState({ topics: [], budget: null, formOk: true, sending: false, formMsg: L.okMsg });
        } catch (err) {
          this.setState({ formOk: false, sending: false, formMsg: serverErrMsg });
        }
      },"""
    if old_submit not in body:
        raise RuntimeError("Home submit handler pattern not found")
    return body.replace(old_submit, new_submit)


def update_vestium_video(body: str) -> str:
    body = body.replace(
        '<x-import component-from-global-scope="image-slot" from="./image-slot.js" id="case05-prototype" shape="rect" radius="0" placeholder="{{ t.shotPlaceholder }}" hint-size="100%,360px" style="width:100%; height:100%; display:block;"></x-import>',
        '<sc-if value="{{ hasVestiumVideo }}" hint-placeholder-val="{{ false }}">\n'
        '                  <iframe src="{{ vestiumVideoSrc }}" title="Vestium prototype video" loading="lazy" allow="fullscreen; encrypted-media; picture-in-picture" allowfullscreen style="width:100%; height:100%; border:0; display:block; background:#0D0D0C;"></iframe>\n'
        '                </sc-if>\n'
        '                <sc-if value="{{ noVestiumVideo }}" hint-placeholder-val="{{ true }}">\n'
        '                  <div style="width:100%; height:100%; min-height:320px; display:flex; align-items:center; justify-content:center; text-align:center; padding:clamp(20px,3vw,40px); box-sizing:border-box; background:linear-gradient(135deg,#181817,#0D0D0C); color:#F2EFEA;">\n'
        '                    <p style="margin:0; max-width:34ch; font-size:0.82rem; line-height:1.5; letter-spacing:0.08em; text-transform:uppercase; color:#E7188C;">{{ t.shotPlaceholder }}</p>\n'
        '                  </div>\n'
        '                </sc-if>',
    )
    old_return = """return {
      t: DATA[lang], langs,
      prev: () => this.goTo(this.current() - 1),
      next: () => this.goTo(this.current() + 1),
    };"""
    new_return = """const videoId = (window.__VESTIUM_YOUTUBE_ID || "").trim();
    return {
      t: DATA[lang], langs,
      hasVestiumVideo: !!videoId,
      noVestiumVideo: !videoId,
      vestiumVideoSrc: videoId ? "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(videoId) + "?rel=0&modestbranding=1" : "",
      prev: () => this.goTo(this.current() - 1),
      next: () => this.goTo(this.current() + 1),
    };"""
    if old_return not in body:
        raise RuntimeError("Vestium render return pattern not found")
    return body.replace(old_return, new_return)


def transform(source_name: str, lang: str, kind: str, slug: str | None = None) -> str:
    source = (HANDOFF / source_name).read_text(encoding="utf-8")
    body = extract_body(source)
    title, _ = metadata(kind, lang, slug)
    body = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)}</title>", body, count=1, flags=re.S)
    body = normalize_fonts(body)
    body = normalize_assets(body)
    body = replace_links(body, lang, kind, slug)
    body = replace_language_state(body)
    if kind == "home":
        body = update_home_form(body)
    if slug == "vestium":
        body = update_vestium_video(body)
    body = body.replace("./image-slot.js", "")
    page = f"{head(lang, kind, slug)}\n<body>\n{body}\n</body>\n</html>\n"
    checks = ["support.js", "fonts.googleapis", "fonts.gstatic", "image-slot.js"]
    leftovers = [needle for needle in checks if needle in page]
    if leftovers:
        raise RuntimeError(f"{source_name}: leftover prototype references: {leftovers}")
    return page


def copy_assets() -> None:
    target = ROOT / "assets" / "redesign"
    target.mkdir(parents=True, exist_ok=True)
    for asset in (HANDOFF / "assets").iterdir():
        if asset.is_file():
            shutil.copy2(asset, target / asset.name)
    shutil.copy2(HANDOFF / "uploads" / "DSCF5508.jpg", target / "DSCF5508.jpg")


def write_pages() -> None:
    for kind, source_name in PAGE_SOURCES.items():
        for lang in LANGS:
            output = out_path(kind, lang)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(transform(source_name, lang, kind), encoding="utf-8")

    for slug in CASE_ORDER:
        source_name = CASE_SOURCE_BY_SLUG[slug]
        for lang in LANGS:
            output = out_path("case", lang, slug)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(transform(source_name, lang, "case", slug), encoding="utf-8")


def sitemap_url_group(kind: str, slug: str | None = None) -> str:
    locs = alt_routes(kind, slug)
    items = []
    for lang in LANGS:
        items.append(
            "  <url>\n"
            f"    <loc>{SITE}{locs[lang]}</loc>\n"
            f"    <lastmod>{LASTMOD}</lastmod>\n"
            f"    <xhtml:link rel=\"alternate\" hreflang=\"de\" href=\"{SITE}{locs['de']}\" />\n"
            f"    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"{SITE}{locs['en']}\" />\n"
            f"    <xhtml:link rel=\"alternate\" hreflang=\"pl\" href=\"{SITE}{locs['pl']}\" />\n"
            f"    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{SITE}{locs['de']}\" />\n"
            "  </url>"
        )
    return "\n".join(items)


def write_sitemap() -> None:
    groups = [
        sitemap_url_group("home"),
        sitemap_url_group("about"),
        sitemap_url_group("projects"),
        sitemap_url_group("imprint"),
        sitemap_url_group("privacy"),
    ]
    groups.extend(sitemap_url_group("case", slug) for slug in CASE_ORDER)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(groups)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")


def main() -> None:
    if not HANDOFF.exists():
        raise SystemExit(f"Handoff not found: {HANDOFF}")
    copy_assets()
    write_pages()
    write_sitemap()
    print("Redesign pages, assets and sitemap written.")


if __name__ == "__main__":
    main()
