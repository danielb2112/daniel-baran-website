# daniel-baran-website

Statische Website für `daniel-baran.com`: dreisprachig vorgerendertes HTML, lokale Assets und schlankes Vanilla-JS für Interaktivität.

## Build

Der Build läuft vollständig im Repo und verwendet Node, weil die vorhandenen Inhalte als JavaScript-`DATA`/`META`-Objekte in den bestehenden Templates liegen. Es gibt keine externe Handoff- oder `/private/tmp`-Abhängigkeit.

```bash
npm run build
```

Der Build schreibt das vollständige Deploy-Artefakt nach `dist/`. Production enthält kein React, kein Babel und kein altes DC-Runtime-Bundle.

Lokale Vorschau mit Live-Reload:

```bash
npm run dev
```

## Cloudflare Deploy

Die Website wird als Cloudflare Worker mit statischen Assets deployed. Der Worker liefert die Dateien aus `dist/` aus und verarbeitet zusätzlich `POST /api/contact`.

Lokaler manueller Deploy:

```bash
npm run deploy
```

## Cloudflare Workers Builds

Cloudflare Workers Builds läuft aus einem frischen Git-Checkout. `dist/` ist bewusst nicht im Repo und muss vor `wrangler deploy` erzeugt werden. Deshalb darf die Workers-Build-Konfiguration nicht nur `npx wrangler deploy` ausführen.

Empfohlene Einstellung in **Worker > Settings > Build**:

- **Root directory:** leer lassen, wenn das Repository direkt `daniel-baran-website` ist; sonst auf den Projektordner setzen.
- **Install command:** `npm ci`
- **Build command:** `npm run build`
- **Deploy command:** `npm run deploy:worker`

Alternative, falls Cloudflare nur ein kombiniertes Deploy-Feld nutzt:

```bash
npm run deploy
```

`wrangler` ist als Dev-Dependency in `package.json` gepinnt. Workers Builds verwendet dadurch die im Repo definierte Wrangler-Version. Der Build selbst ist Node-only und ruft kein Python-Script auf.

Der Worker macht keine nutzerabhängigen Sprach-Redirects auf `/`. Sprachwechsel passieren über feste Links (`/`, `/en/`, `/pl/`) und der Sprachumschalter speichert optional `db-lang` in Cookie/localStorage.

## Kontaktformular

Das Formular sendet an `/api/contact`. Der Worker validiert Pflichtfelder, Budget, Themenauswahl, E-Mail-Adresse, Honeypot und ein einfaches IP-Rate-Limit. Der Mailversand läuft über Resend.

Erforderliche Cloudflare Secrets/Variables:

- `RESEND_API_KEY` als Secret
- `CONTACT_FROM_EMAIL` als Variable oder Secret, z. B. `Daniel Baran <kontakt@daniel-baran.com>` nach Domain-Verifizierung bei Resend
- `CONTACT_TO_EMAIL` optional, Standard ist `kontakt@daniel-baran.com`
- `CONTACT_SUBJECT_PREFIX` optional, Standard ist `Website-Anfrage`

Resend-Voraussetzung:

1. Domain bei Resend verifizieren.
2. Absenderadresse in `CONTACT_FROM_EMAIL` auf eine verifizierte Domain setzen.
3. `RESEND_API_KEY` in Cloudflare für den Worker hinterlegen.

## Static Renderer

Die statischen Sprachseiten werden aus den vorhandenen HTML-Templates und deren eingebetteten `DATA`/`META`-Objekten erzeugt:

```bash
node scripts/build-static.mjs
```

Der alte `scripts/build_redesign.py` bleibt nur als historische Referenz im Repo. Für Deployments ist `npm run build` maßgeblich.

## Vestium-Video

Case 5 nutzt einen privacy-freundlichen YouTube-Embed. Die Video-ID steht in `VESTIUM_YOUTUBE_ID` in `scripts/build-static.mjs`. Das MP4 bleibt bewusst außerhalb des Repos.
