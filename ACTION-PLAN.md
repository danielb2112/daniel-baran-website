# SEO Action Plan: daniel-baran.com

## Implementation Status: 2026-07-17

Implemented safely in the repo:
- Title and meta description generation now uses language-specific page metadata and per-case descriptions.
- JSON-LD now includes `Organization`, `Person`, homepage `WebSite`, page-level schema, `BreadcrumbList` where relevant, `dateModified`, and richer case-study `CreativeWork`.
- Homepage, about pages, projects pages, and all case studies now include crawlable static summary sections in German, English, and Polish.
- The extracted prototype `<helmet>` block is removed from generated public `index.html` files.
- `/llms.txt` has been added for GEO/AI crawler context.
- `Strict-Transport-Security` has been added to `_headers`.
- `.seo-cache/` and Python `__pycache__/` are ignored.

Intentionally not completed in this safe pass:
- Full removal of `{{ ... }}`, `<sc-*>`, and `<x-dc>` runtime markup was deferred because the current site still depends on the custom runtime for the interactive redesign. Removing it wholesale would be a higher-risk frontend refactor and should be handled with browser-based visual regression coverage.
- CSP still allows `'unsafe-inline'` and `'unsafe-eval'` because tightening it before removing the runtime can break page behavior.
- Installed SEO fetch scripts cannot analyze the local build directly because they block `127.0.0.1`; local validation was done with deterministic HTML, JSON-LD, sitemap, and HTTP checks instead.

## Critical

No hard indexing blocker found. The site is reachable, sitemap URLs return 200, robots allows crawling, and generated head canonicals are self-referencing.

## High Priority

### 1. Static pre-render the critical content

Target files:
- [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:1070)
- Generated HTML files such as [index.html](/Users/danielbaran/projekte/daniel-baran-website/index.html:28)

Tasks:
- Remove the extracted prototype `<helmet>` block from body output.
- Replace custom runtime placeholders with actual static text, links, and image paths during build.
- Ensure no public HTML contains `{{ ... }}`, `<sc-for>`, `<sc-if>`, `<x-dc>`, or body-level `<helmet>`.

Acceptance check:

```bash
rg -n "\\{\\{|<helmet>|<sc-|<x-dc" --glob '*.html'
```

Expected result: no matches in generated public HTML.

### 2. Fix title and meta description generation

Target:
- [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:43)
- [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:397)

Tasks:
- Keep titles under about 60 characters.
- Expand meta descriptions to 120-160 characters where possible.
- Add `CASE_DESCRIPTIONS` by slug and language.
- Make homepage titles language-specific rather than identical across DE/EN/PL.

Acceptance check:

```bash
python3 scripts/build_redesign.py
python3 - <<'PY'
from pathlib import Path
import re
for p in sorted(Path('.').rglob('index.html')):
    txt = p.read_text(errors='ignore')
    title = re.search(r'<title>(.*?)</title>', txt, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)">', txt, re.S)
    if title and not 30 <= len(re.sub(r'<.*?>','',title.group(1))) <= 60:
        print('title', p, len(title.group(1)), title.group(1))
    if desc and not 120 <= len(desc.group(1)) <= 160:
        print('desc', p, len(desc.group(1)), desc.group(1))
PY
```

### 3. Add extractable content depth

Targets:
- Homepage, about pages, projects pages, and all case-study pages.

Tasks:
- Homepage: add 500-900 words of static, structured copy.
- About: add credentials, certifications, work style, and proof points.
- Case studies: add 300-600 word summaries per case with challenge, role, approach, result.
- Use real H2/H3 headings and short paragraphs.

Acceptance check:
- Homepage server-visible word count at least 500.
- About pages at least 400.
- Case studies at least 300 each as an interim target.

## Medium Priority

### 4. Expand structured data

Tasks:
- Add `WebSite` on the homepage.
- Add `WebPage` for all pages.
- Add `BreadcrumbList` for `/projekte/` and case-study routes.
- Add `dateModified`.
- Keep `Person` and enrich with truthful credentials and sameAs links.

### 5. Add GEO support

Tasks:
- Add `/llms.txt`.
- Add 134-167 word answer blocks on homepage/about.
- Add question-based headings for core service and expertise questions.

Suggested `/llms.txt` outline:

```text
# Daniel Baran
> Senior IT Project & Product Manager for IT projects, product ownership, AI enablement, streaming infrastructure and cross-functional delivery.

## Key pages
- [Homepage](https://daniel-baran.com/): Service positioning, availability and contact.
- [Projects](https://daniel-baran.com/projekte/): Case studies across media, AI, streaming, startup and automotive.
- [About](https://daniel-baran.com/ueber-mich/): Experience, certifications, working style and toolkit.

## Key facts
- Focus: IT project management, product ownership, AI enablement, streaming infrastructure.
- Languages: German, English, Polish.
- Location: Poland, remote across Europe.
```

### 6. Clean sitemap freshness

Tasks:
- Replace global `LASTMOD` with per-file or per-page modification dates.
- Keep all sitemap URLs canonical and 200-only.

### 7. Improve visual/mobile details

Tasks:
- Make the primary CTA visible above the fold on mobile.
- Increase mobile menu and CTA touch targets to at least 48px height.
- Add width/height to below-fold case-study images.

### 8. Tighten security once rendering is static

Tasks:
- Add `Strict-Transport-Security` after confirming HTTPS-only operation.
- Remove `'unsafe-eval'` and reduce `'unsafe-inline'` where the runtime permits.

### 9. Add backlink data only when needed

Current status:
- Moz API: not configured.
- Bing Webmaster API: not configured.
- Common Crawl: domain not found in `cc-main-2026-jan-feb-mar`.

Tasks:
- Verify the domain in Bing Webmaster Tools.
- Add a free Moz API key if domain authority and spam scoring matter.
- Re-run `/seo backlinks daniel-baran.com` after the site has more external mentions.

## Verification Commands

```bash
rg -n "\\{\\{|<helmet>|<sc-|<x-dc" --glob '*.html'
/Users/danielbaran/.codex/skills/seo/.venv/bin/python /Users/danielbaran/.codex/skills/seo/scripts/analyze_technical.py https://daniel-baran.com --json
/Users/danielbaran/.codex/skills/seo/.venv/bin/python /Users/danielbaran/.codex/skills/seo/scripts/analyze_content.py https://daniel-baran.com --json
/Users/danielbaran/.codex/skills/seo/.venv/bin/python /Users/danielbaran/.codex/skills/seo/scripts/analyze_schema.py https://daniel-baran.com --json
/Users/danielbaran/.codex/skills/seo/.venv/bin/python /Users/danielbaran/.codex/skills/seo/scripts/analyze_geo.py https://daniel-baran.com --json
/Users/danielbaran/.codex/skills/seo/.venv/bin/python /Users/danielbaran/.codex/skills/seo/scripts/commoncrawl_graph.py daniel-baran.com --json
```
