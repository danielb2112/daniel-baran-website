# SEO Full Audit: daniel-baran.com

Analyzed: 2026-07-17T11:00:29Z  
Scope: local Git repository plus live checks for `https://daniel-baran.com/`, `robots.txt`, `sitemap.xml`, and installed codex-seo scripts.  
Business type: personal portfolio / freelance IT project and product management.

## Executive Summary

SEO Health Score: **58/100** directional.

The site is technically reachable, HTTPS-only, indexed, multilingual, and has a clean 42-URL sitemap. The strongest SEO risk is not infrastructure; it is that much of the meaningful content is still template/JavaScript dependent in the initial HTML. Installed SEO scripts see the homepage as only 144 words, and local parsing sees most core pages and case studies as very thin. Titles and meta descriptions are also generated centrally with many overlong titles and generic duplicated descriptions.

Key tool scores:

| Category | Score | Notes |
|---|---:|---|
| Technical SEO | 87 | Good crawlability/security; JS rendering risk; no IndexNow |
| Content quality | 23 | Homepage below content floor; weak E-E-A-T extraction |
| On-page SEO | 42 | Titles too long, descriptions short/duplicated, thin pages |
| Schema | 76 | Person/ProfilePage present; WebSite/WebPage/Organization/Breadcrumb gaps |
| Performance | 91 | Heuristic only; no PageSpeed/CrUX credentials configured |
| AI/GEO readiness | 44 | AI crawlers allowed, but no `llms.txt` and weak extractable passages |
| Images | 82 | Alt text mostly ok; hero just over warning threshold; templated unresolved image |
| Backlinks | insufficient data | Moz/Bing missing; Common Crawl did not find the domain |

## What Is Working

- Live homepage returns HTTP/2 200 through Cloudflare.
- `robots.txt` allows crawling and references `https://daniel-baran.com/sitemap.xml`.
- Sitemap contains 42 URLs; all 42 live URLs returned 200 in the installed sitemap analyzer.
- Local sitemap coverage matches the Git repo: 42 public `index.html` routes, 0 missing local files, 0 local public routes missing from sitemap.
- Canonicals in the generated head are self-referencing in the repo.
- Hreflang is present for `de`, `en`, `pl`, and `x-default`.
- JSON-LD exists on all analyzed page types.
- Hero image uses WebP, dimensions, eager loading, and `fetchpriority="high"`.
- Security headers include CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.

## High Priority Findings

### 1. Initial HTML still contains template markup and a second body-level `<helmet>`

Evidence:
- Generated homepage head is valid at [index.html](/Users/danielbaran/projekte/daniel-baran-website/index.html:1), but the body immediately contains `<x-dc>` and `<helmet>` at [index.html](/Users/danielbaran/projekte/daniel-baran-website/index.html:28).
- The generator appends the extracted prototype body directly after the generated head in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:1088).
- Homepage case-list images still appear as `src="{{ c.img }}"` and `alt="{{ c.title }}"` in [index.html](/Users/danielbaran/projekte/daniel-baran-website/index.html:278).

Impact:
- Google can render JavaScript, but AI crawlers and simpler SEO tools do not reliably execute the runtime.
- The installed content script counted only 144 homepage words and the images script detected an unresolved `https://daniel-baran.com/{{ c.img }}` image.
- The sitemap script reported false canonical mismatches because the unusual markup confuses its simple parser. Manual source review shows self-canonical tags, so this is a parser/markup robustness issue, not a confirmed canonical defect.

Recommendation:
- Pre-render the dynamic custom-element output into static HTML during `scripts/build_redesign.py`.
- Strip the prototype `<helmet>...</helmet>` block from the body after extracting the body.
- Ensure generated HTML contains real page copy and real image `src`/`alt` values without relying on runtime substitution for critical content.

### 2. Content is too thin for the site intent

Evidence:
- Installed content script: homepage word count 144; recommended homepage floor 500.
- Local parser: homepage 141 words, about pages about 100 words, projects pages about 62 words, case studies about 123-172 words.
- Key metadata source is centralized in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:71).

Impact:
- The site undersells the expertise it is trying to rank for: IT project management, product ownership, AI enablement, streaming infrastructure, and case-study proof.
- E-E-A-T signals are present in concept but not strongly extractable in server-visible content.

Recommendation:
- Homepage: add 500-900 words of static, structured content covering who Daniel is, service fit, proof points, industries, and project outcomes.
- About: add credential and process detail, certifications, working model, and specific experience signals.
- Each case study: add a 300-600 word static summary with challenge, role, approach, constraints, outcome, and relevant technology/business terms.

### 3. Titles and meta descriptions need systematic cleanup

Evidence:
- Titles are generated in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:43) and case titles in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:111).
- Case descriptions are generic and duplicated by language in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:397).
- Local audit found many titles over 60 chars and descriptions below 120 chars.

Impact:
- Google may rewrite snippets heavily.
- Duplicate case descriptions reduce topical clarity and click-through relevance.
- Overlong titles hide the distinguishing part of the page in SERPs.

Recommendation:
- Keep titles roughly 35-60 chars.
- Expand descriptions to roughly 120-160 chars.
- Create per-case descriptions, not one generic case description for all nine projects.

### 4. Schema is present but incomplete for entity and page discovery

Evidence:
- JSON-LD is generated in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:409).
- Installed schema script detected `Person` and `ProfilePage`, score 76, and recommended `WebPage`, `WebSite`, and `Organization`.

Impact:
- The Person entity is a good start, but the site lacks a stronger site/entity graph.
- Breadcrumbs are missing for project detail pages.
- Case studies do not expose dateModified, breadcrumb position, or richer work metadata.

Recommendation:
- Add `WebSite` on the homepage.
- Add explicit `WebPage` per page, even when also using `ProfilePage` or `CollectionPage`.
- Consider `ProfessionalService` or `Organization` only if it truthfully represents the freelance business entity.
- Add `BreadcrumbList` on projects and case studies.
- Add `dateModified` from the actual generated lastmod value.

### 5. AI search readiness is weak

Evidence:
- Installed GEO score: 44.
- `/llms.txt` returned 404.
- No 134-167 word self-contained answer block found.
- Question-based headings and answer-first sections are limited.

Impact:
- ChatGPT Search, Perplexity, and AI Overview-style systems have limited clean passages to cite.
- The site has strong underlying experience but does not package it into extractable claims.

Recommendation:
- Add `/llms.txt` with key pages, service summary, case-study links, and authority/contact signals.
- Add answer-first H2/H3 sections such as "What does Daniel Baran do?", "When should teams bring Daniel in?", and "Which project types has Daniel delivered?".
- Add concise proof blocks with specific outcomes, team sizes, domains, and technologies.

## Medium Priority Findings

### Sitemap lastmod values are all identical

The sitemap is valid and complete, but every `<lastmod>` is `2026-07-17`. This is not a blocking issue, but it is less useful than page-specific modification dates. The sitemap writer is in [scripts/build_redesign.py](/Users/danielbaran/projekte/daniel-baran-website/scripts/build_redesign.py:1175).

### Visual/mobile checks need small fixes

Installed visual script found:
- H1 visible above fold.
- CTA not visible above fold.
- No horizontal mobile scroll.
- Some touch targets below the 48px recommendation, including the mobile menu summary and CTA links.

Recommendation: make the primary CTA visible earlier on mobile and increase interactive target height/padding.

### Image optimization is mostly fine but not complete

Installed images score: 82.

Issues:
- Hero WebP is about 217 KB, slightly above the 200 KB warning threshold.
- One templated image is unresolved in the initial HTML.
- Some below-fold images lack intrinsic width/height attributes.

Recommendation: fix static rendering first, then add dimensions and consider AVIF/WebP responsive variants for larger case images.

### Security headers are good, with two caveats

Security headers are present in [_headers](/Users/danielbaran/projekte/daniel-baran-website/_headers:1). Caveats:
- No `Strict-Transport-Security` header is configured.
- CSP currently allows `'unsafe-inline'` and `'unsafe-eval'`, likely because of the runtime/prototype architecture.

Recommendation: after static pre-rendering, tighten CSP and add HSTS if HTTPS is stable.

### Backlink data is insufficient

Moz and Bing Webmaster API credentials are not configured. Common Crawl Web Graph release `cc-main-2026-jan-feb-mar` did not find `daniel-baran.com`, which usually means the domain is too new, too small, or not prominent enough in that crawl.

Recommendation: configure Moz or Bing Webmaster data if backlink health becomes important, then rerun the backlink subskill.

## Limitations

- Google Search Console, PageSpeed Insights, CrUX, Indexing API, and GA4 credentials are not configured.
- Performance score is heuristic, not field data.
- Playwright Chromium is not installed in the SEO skill venv, so no screenshot artifacts were generated.
- DataForSEO/Firecrawl MCP enrichment was not used.
- Backlink analysis is limited to Common Crawl because Moz/Bing/DataForSEO are not configured.
- SXO SERP-backwards analysis was not run for a specific keyword because no target keyword was provided; strategic SXO should be run per keyword.

## Priority Order

1. Pre-render real static HTML and remove body `<helmet>`.
2. Rewrite title/meta description maps in `scripts/build_redesign.py`.
3. Add substantial static homepage/about/case-study copy.
4. Expand schema graph with WebSite/WebPage/BreadcrumbList and richer case metadata.
5. Add `/llms.txt` and answer-first sections.
6. Add page-specific sitemap lastmod and tighten security/performance details.
