# daniel-baran-website

Statische Website für `daniel-baran.com`: HTML, CSS und JavaScript ohne Build-Step und ohne externe Requests zur Laufzeit.

## Cloudflare Deploy

Die Website wird als Cloudflare Worker mit statischen Assets deployed. Der Worker liefert die Dateien aus `.` aus und verarbeitet zusätzlich `POST /api/contact`.

Build/Deploy command in Cloudflare:

```bash
npx wrangler deploy
```

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
