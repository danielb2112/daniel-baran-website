# daniel-baran-website

Statische Website für `daniel-baran.com`: HTML, CSS und JavaScript ohne Build-Step und ohne externe Requests zur Laufzeit.

## Cloudflare Pages Deploy

1. Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git → dieses Repo wählen.
2. Build-Einstellungen: **Framework preset: None**, **Build command: leer lassen**, **Build output directory: `/`** (Root).
3. Deploy. Danach unter Custom Domains `daniel-baran.com` (und `www`) hinzufügen — da die Domain bereits über Cloudflare Registrar läuft, DNS automatisch.
4. Vor Go-live in `assets/app.js` die vier Platzhalter (AVAILABLE_FROM, LINKEDIN_URL, PHONE, EMAIL) füllen, `portrait.jpg` ersetzen, interne Hinweisblöcke in impressum/datenschutz löschen.
