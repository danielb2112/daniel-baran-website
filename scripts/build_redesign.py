#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
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
        "de": "Über mich - Daniel Baran, IT Project & Product Manager",
        "en": "About Daniel Baran - IT Project & Product Manager",
        "pl": "O Danielu Baranie - IT Project & Product Manager",
    },
    "projects": {
        "de": "Projekte - Case Studies von Daniel Baran",
        "en": "Projects - Daniel Baran Case Studies",
        "pl": "Projekty - case studies Daniela Barana",
    },
    "imprint": {
        "de": "Impressum - Daniel Baran",
        "en": "Legal Notice - Daniel Baran",
        "pl": "Nota prawna - Daniel Baran",
    },
    "privacy": {
        "de": "Datenschutz - Daniel Baran",
        "en": "Privacy Policy - Daniel Baran",
        "pl": "Polityka prywatności - Daniel Baran",
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
    "imprint": {
        "de": "Impressum und Anbieterkennzeichnung von Daniel Baran.",
        "en": "Legal notice and provider information for Daniel Baran.",
        "pl": "Nota prawna i dane identyfikacyjne Daniela Barana.",
    },
    "privacy": {
        "de": "Datenschutzerklärung für daniel-baran.com.",
        "en": "Privacy policy for daniel-baran.com.",
        "pl": "Polityka prywatności dla daniel-baran.com.",
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

CASE_SEO_TITLES = {
    "swr-ki-empfehlungsengine": {
        "de": "SWR KI-Empfehlungen - Product Owner Case Study - Daniel Baran",
        "en": "SWR AI Recommendations - Product Owner Case Study - Daniel Baran",
        "pl": "Rekomendacje AI dla SWR - Product Owner Case Study - Daniel Baran",
    },
    "swr-ki-testphase": {
        "de": "SWR KI-Testphase - KI-Enablement Case Study - Daniel Baran",
        "en": "SWR AI Pilot Phase - AI Enablement Case Study - Daniel Baran",
        "pl": "Faza testów AI w SWR - AI Enablement Case Study - Daniel Baran",
    },
    "swr-multiplatform-service": {
        "de": "ARD-Multiplattformservice - Product Owner Case Study - Daniel Baran",
        "en": "ARD Multiplatform Service - Product Owner Case Study - Daniel Baran",
        "pl": "Serwis multiplatformowy ARD - Product Owner Case Study - Daniel Baran",
    },
    "swr-ard-transcoding": {
        "de": "ARD-Transcoding - Projektleitung Case Study - Daniel Baran",
        "en": "ARD Transcoding - Project Lead Case Study - Daniel Baran",
        "pl": "Transcoding ARD - Project Lead Case Study - Daniel Baran",
    },
    "vestium": {
        "de": "Vestium Fashion-Tech Startup - Case Study - Daniel Baran",
        "en": "Vestium Fashion-Tech Startup - Case Study - Daniel Baran",
        "pl": "Vestium Fashion-Tech Startup - Case Study - Daniel Baran",
    },
    "infinite-playa": {
        "de": "The Infinite Playa Metaverse - Case Study - Daniel Baran",
        "en": "The Infinite Playa Metaverse - Case Study - Daniel Baran",
        "pl": "The Infinite Playa Metaverse - Case Study - Daniel Baran",
    },
    "uci-track-champions-league": {
        "de": "UCI Track Champions League Metaverse - Case Study - Daniel Baran",
        "en": "UCI Track Champions League Metaverse - Case Study - Daniel Baran",
        "pl": "UCI Track Champions League Metaverse - Case Study - Daniel Baran",
    },
    "systemmigration-konzernverbund": {
        "de": "Systemmigration bei MAN/VW - IT-Projekt Case Study - Daniel Baran",
        "en": "MAN/VW System Migration - IT Project Case Study - Daniel Baran",
        "pl": "Migracja systemu MAN/VW - IT Project Case Study - Daniel Baran",
    },
    "fahrzeugumbauten-dokumentation": {
        "de": "Fahrzeugumbauten-Dokumentation - IT-Projekt Case Study - Daniel Baran",
        "en": "Vehicle Conversion Documentation - IT Project Case Study - Daniel Baran",
        "pl": "Dokumentacja przebudów pojazdów - IT Project Case Study - Daniel Baran",
    },
}

CASE_DESCRIPTIONS = {
    "swr-ki-empfehlungsengine": {
        "de": "Case Study: KI-Empfehlungssystem für die SWR-Website von Konzept bis Produktion, mit Feedback-Tool und messbar besseren Empfehlungen.",
        "en": "Case study on an AI recommendation system for the SWR website, from concept to production with a feedback tool and measurable improvements.",
        "pl": "Case study systemu rekomendacji AI dla strony SWR: od koncepcji do produkcji, z narzędziem feedbacku i mierzalną poprawą.",
    },
    "swr-ki-testphase": {
        "de": "Case Study zur SWR-KI-Testphase: Teams, Workflows und klare Leitplanken für sinnvolle KI-Nutzung im redaktionellen Alltag.",
        "en": "Case study on the SWR AI pilot phase: enabling teams, workflows and practical guardrails for responsible AI use in editorial work.",
        "pl": "Case study fazy testów AI w SWR: zespoły, workflow i praktyczne zasady odpowiedzialnego użycia AI w redakcji.",
    },
    "swr-multiplatform-service": {
        "de": "Case Study zum ARD-Multiplattformservice: Produktarbeit für zentrale Ausspielung, Betrieb und Weiterentwicklung digitaler Medienangebote.",
        "en": "Case study on the ARD multiplatform service: product work for central publishing, operations and digital media delivery.",
        "pl": "Case study serwisu multiplatformowego ARD: praca produktowa nad centralną dystrybucją, operacjami i cyfrowymi mediami.",
    },
    "swr-ard-transcoding": {
        "de": "Case Study: Zentrales ARD-Transcoding mit Projektleitung, Abstimmung zwischen Partnern und belastbarer Streaming-Infrastruktur.",
        "en": "Case study on central ARD transcoding: project leadership, partner alignment and reliable streaming infrastructure.",
        "pl": "Case study centralnego transkodowania ARD: prowadzenie projektu, koordynacja partnerów i stabilna infrastruktura streamingu.",
    },
    "vestium": {
        "de": "Case Study zu Vestium: Fashion-Tech-Startup von 3D-Scanning und digitalem Kleiderschrank bis zum funktionierenden Prototyp.",
        "en": "Case study on Vestium: building a fashion-tech startup from 3D scanning and digital wardrobe concepts to a working prototype.",
        "pl": "Case study Vestium: fashion-tech startup od skanowania 3D i cyfrowej garderoby do działającego prototypu.",
    },
    "infinite-playa": {
        "de": "Case Study zu The Infinite Playa: Metaverse-Erlebnis für Burning-Man-Kultur, virtuelle Räume und Community-Formate.",
        "en": "Case study on The Infinite Playa: a metaverse experience for Burning Man culture, virtual spaces and community formats.",
        "pl": "Case study The Infinite Playa: doświadczenie metaverse dla kultury Burning Man, wirtualnych przestrzeni i społeczności.",
    },
    "uci-track-champions-league": {
        "de": "Case Study zur UCI Track Champions League: Metaverse-Konzept für Live-Sport, digitale Fan-Erlebnisse und virtuelle Aktivierung.",
        "en": "Case study on the UCI Track Champions League: a metaverse concept for live sports, digital fan experiences and virtual activation.",
        "pl": "Case study UCI Track Champions League: koncepcja metaverse dla sportu na żywo, cyfrowych doświadczeń fanów i aktywacji.",
    },
    "systemmigration-konzernverbund": {
        "de": "Case Study zur MAN/VW-Systemmigration: Wechsel eines zentralen Werkstatt-Systems ohne Bruch für Nutzer, Prozesse und Support.",
        "en": "Case study on a MAN/VW system migration: switching a central workshop system without disrupting users, processes or support.",
        "pl": "Case study migracji systemu MAN/VW: zmiana centralnego systemu warsztatowego bez przerwy dla użytkowników, procesów i wsparcia.",
    },
    "fahrzeugumbauten-dokumentation": {
        "de": "Case Study zur Dokumentation für Fahrzeugumbauten: Service-Wissen weltweit auffindbar machen und technische Informationen strukturieren.",
        "en": "Case study on vehicle conversion documentation: making global service knowledge searchable and structuring technical information.",
        "pl": "Case study dokumentacji przebudów pojazdów: globalna wiedza serwisowa staje się łatwa do znalezienia i uporządkowana.",
    },
}

CASE_IMAGE_BY_SLUG = {
    "swr-ki-empfehlungsengine": "case-01-swr.webp",
    "swr-ki-testphase": "case-02-swr-ki.webp",
    "swr-multiplatform-service": "case-03-ard-multiplattform.webp",
    "swr-ard-transcoding": "case-04-ard-transcoding.webp",
    "vestium": "case-05-vestium.webp",
    "infinite-playa": "case-06-playa.webp",
    "uci-track-champions-league": "case-07-uci.webp",
    "systemmigration-konzernverbund": "case-08-systemmigration.webp",
    "fahrzeugumbauten-dokumentation": "case-09-fahrzeugumbauten.webp",
}

LEGAL_COPY = {
    "imprint": {
        "de": {
            "eyebrow": "Rechtliches",
            "h1": "Impressum",
            "side": "Anbieterkennzeichnung",
            "back": "Zurück zur Startseite",
            "sections": [
                ("Angaben gemäß § 5 DDG", "Daniel Baran<br>Jasionka 33<br>28-300 Jędrzejów<br>Polen"),
                ("Kontakt", "Telefon: +49 172 7539490 (DE) · +48 780 680 329 (PL)<br>E-Mail: kontakt@daniel-baran.com"),
                ("Tätigkeit", "Freiberufliche Dienstleistungen: IT-Projektmanagement, Product Ownership und KI-Beratung."),
                ("Verantwortlich für den Inhalt", "Daniel Baran (Anschrift wie oben)"),
                ("Streitbeilegung", 'Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: <a href="https://ec.europa.eu/consumers/odr" rel="noopener">https://ec.europa.eu/consumers/odr</a>. Ich bin nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.'),
                ("Haftung für Links", "Diese Website enthält Links zu externen Websites Dritter, auf deren Inhalte ich keinen Einfluss habe. Für diese fremden Inhalte übernehme ich keine Gewähr; verantwortlich ist stets der jeweilige Anbieter oder Betreiber der Seiten."),
            ],
        },
        "en": {
            "eyebrow": "Legal",
            "h1": "Legal Notice",
            "side": "Provider information",
            "back": "Back to home",
            "sections": [
                ("Information according to § 5 DDG", "Daniel Baran<br>Jasionka 33<br>28-300 Jędrzejów<br>Poland"),
                ("Contact", "Phone: +49 172 7539490 (DE) · +48 780 680 329 (PL)<br>Email: kontakt@daniel-baran.com"),
                ("Activity", "Freelance services: IT project management, product ownership and AI consulting."),
                ("Responsible for content", "Daniel Baran (address as above)"),
                ("Dispute resolution", 'The European Commission provides a platform for online dispute resolution (ODR): <a href="https://ec.europa.eu/consumers/odr" rel="noopener">https://ec.europa.eu/consumers/odr</a>. I am not obliged and not willing to participate in dispute resolution proceedings before a consumer arbitration board.'),
                ("Liability for links", "This website contains links to external third-party websites over whose content I have no influence. I assume no liability for this external content; the respective provider or operator of the linked pages is always responsible for their content."),
            ],
        },
        "pl": {
            "eyebrow": "Nota prawna",
            "h1": "Nota prawna",
            "side": "Dane identyfikacyjne",
            "back": "Powrót do strony głównej",
            "sections": [
                ("Informacje zgodnie z § 5 DDG", "Daniel Baran<br>Jasionka 33<br>28-300 Jędrzejów<br>Polska"),
                ("Kontakt", "Telefon: +49 172 7539490 (DE) · +48 780 680 329 (PL)<br>E-mail: kontakt@daniel-baran.com"),
                ("Działalność", "Usługi freelancerskie: zarządzanie projektami IT, product ownership oraz doradztwo w zakresie AI."),
                ("Odpowiedzialny za treść", "Daniel Baran (adres jak powyżej)"),
                ("Rozstrzyganie sporów", 'Komisja Europejska udostępnia platformę internetowego rozstrzygania sporów (ODR): <a href="https://ec.europa.eu/consumers/odr" rel="noopener">https://ec.europa.eu/consumers/odr</a>. Nie jestem zobowiązany ani gotowy do udziału w postępowaniach przed konsumencką komisją arbitrażową.'),
                ("Odpowiedzialność za linki", "Ta strona internetowa zawiera linki do zewnętrznych stron internetowych osób trzecich, na których treść nie mam wpływu. Nie ponoszę odpowiedzialności za te zewnętrzne treści; odpowiedzialny jest zawsze odpowiedni dostawca lub operator tych stron."),
            ],
        },
    },
    "privacy": {
        "de": {
            "eyebrow": "Rechtliches",
            "h1": "Datenschutz",
            "side": "Datenschutzerklärung",
            "back": "Zurück zur Startseite",
            "sections": [
                ("1. Verantwortlicher", "Daniel Baran<br>Jasionka 33, 28-300 Jędrzejów, Polen<br>E-Mail: kontakt@daniel-baran.com"),
                ("2. Allgemeines", "Diese Website ist ein rein informatives Angebot. Es werden keine Tracking- oder Analyse-Dienste eingesetzt und keine personenbezogenen Daten zu Werbezwecken verarbeitet. Schriftarten werden lokal von dieser Website geladen; es findet keine Verbindung zu Google Fonts oder ähnlichen Diensten statt."),
                ("3. Hosting (Cloudflare)", 'Diese Website wird bei Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA, gehostet. Beim Aufruf der Website verarbeitet Cloudflare technisch notwendige Daten wie IP-Adresse, Datum und Uhrzeit des Zugriffs, aufgerufene Seite, Browsertyp und Betriebssystem (Server-Logfiles). Diese Verarbeitung ist für den sicheren und stabilen Betrieb der Website erforderlich (Art. 6 Abs. 1 lit. f DSGVO – berechtigtes Interesse). Cloudflare ist unter dem EU-U.S. Data Privacy Framework zertifiziert; zudem bestehen Standardvertragsklauseln. Weitere Informationen: <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">https://www.cloudflare.com/privacypolicy/</a>'),
                ("4. Sprachwahl und lokale Speicherung", "Die Website stellt feste Sprachversionen unter /, /pl/ und /en/ bereit. Beim Aufruf der Startseite kann der Browser-Header Accept-Language technisch ausgewertet werden, um Besucher auf die passende Sprachversion zu leiten. Wenn Sie eine Sprache wählen oder eine Sprache automatisch erkannt wurde, kann das technisch notwendige Cookie db-lang mit dem Sprachcode de, en oder pl gesetzt werden. Zweck ist ausschließlich die Speicherung der Sprachwahl und die korrekte Navigation auf dieser Website. Die Speicherdauer beträgt 12 Monate. Rechtsgrundlage für das Setzen des Cookies ist § 25 Abs. 2 TTDSG; die weitere Verarbeitung erfolgt auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Zusätzlich kann derselbe Sprachcode lokal im Browser als localStorage-Eintrag db-lang gespeichert werden. Es findet kein Tracking statt und die Sprachwahl wird nicht an Dritte weitergegeben."),
                ("5. Kontaktaufnahme", "Wenn Sie mich per Kontaktformular, E-Mail oder Telefon kontaktieren, verarbeite ich die von Ihnen mitgeteilten Daten (Name, Kontaktdaten, Inhalt der Anfrage, ausgewählte Themen und Budgetrahmen) zur Bearbeitung Ihrer Anfrage und für Anschlussfragen. Das Kontaktformular wird technisch über Cloudflare Workers verarbeitet und per E-Mail über den Dienst Resend, Resend, Inc., 2261 Market Street #5039, San Francisco, CA 94114, USA, an mich zugestellt. Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO bzw. Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden gelöscht, sobald sie für die Bearbeitung nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten entgegenstehen."),
                ("6. Externe Links", "Diese Website verlinkt auf externe Angebote, zum Beispiel LinkedIn und YouTube. Beim Anklicken oder Abspielen verlassen Sie diese Website bzw. rufen Inhalte des jeweiligen Anbieters ab; es gilt die Datenschutzerklärung des jeweiligen Anbieters. Es sind keine Social-Media-Plugins eingebunden, die bereits beim Seitenaufruf Daten übertragen."),
                ("7. Ihre Rechte", "Sie haben nach der DSGVO das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit sowie Widerspruch gegen Verarbeitungen auf Grundlage von Art. 6 Abs. 1 lit. f DSGVO. Wenden Sie sich dazu an die oben genannten Kontaktdaten."),
                ("8. Beschwerderecht", 'Sie haben das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Zuständig für mich als Verantwortlichen ist die polnische Aufsichtsbehörde: Urząd Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Warszawa, <a href="https://uodo.gov.pl" rel="noopener">https://uodo.gov.pl</a>. Sie können sich auch an die Aufsichtsbehörde Ihres gewöhnlichen Aufenthaltsorts wenden.'),
                ("Stand", "Juli 2026"),
            ],
        },
        "en": {
            "eyebrow": "Legal",
            "h1": "Privacy Policy",
            "side": "Privacy",
            "back": "Back to home",
            "sections": [
                ("1. Controller", "Daniel Baran<br>Jasionka 33, 28-300 Jędrzejów, Poland<br>Email: kontakt@daniel-baran.com"),
                ("2. General information", "This website is purely informational. No tracking or analytics services are used, and no personal data is processed for advertising purposes. Fonts are loaded locally from this website; no connection is made to Google Fonts or similar services."),
                ("3. Hosting (Cloudflare)", 'This website is hosted by Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA. When the website is accessed, Cloudflare processes technically necessary data such as IP address, date and time of access, page requested, browser type and operating system (server log files). This processing is necessary for the secure and stable operation of the website (Art. 6(1)(f) GDPR – legitimate interest). Cloudflare is certified under the EU-U.S. Data Privacy Framework; standard contractual clauses are also in place. Further information: <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">https://www.cloudflare.com/privacypolicy/</a>'),
                ("4. Language choice and local storage", "The website provides fixed language versions at /, /pl/ and /en/. When the homepage is accessed, the browser header Accept-Language may be technically evaluated to direct visitors to the appropriate language version. When you choose a language or a language is detected automatically, the technically necessary cookie db-lang may be set with the language code de, en or pl. Its sole purpose is to store the language choice and support correct navigation on this website. The storage period is 12 months. The legal basis for setting the cookie is Section 25(2) TTDSG; further processing is based on Art. 6(1)(f) GDPR. In addition, the same language code may be stored locally in your browser as the localStorage entry db-lang. No tracking takes place and the language choice is not shared with third parties."),
                ("5. Contact", "If you contact me via the contact form, email or phone, I process the data you provide to handle your enquiry and any follow-up questions. The contact form is technically processed via Cloudflare Workers and delivered to me by email through Resend, Resend, Inc., 2261 Market Street #5039, San Francisco, CA 94114, USA. The legal basis is Art. 6(1)(b) GDPR or Art. 6(1)(f) GDPR. The data will be deleted once it is no longer required for handling the enquiry and no statutory retention obligations apply."),
                ("6. External links", "This website links to external services, for example LinkedIn and YouTube. When you click such a link or play embedded content, you leave this website or request content from the respective provider; the privacy policy of that provider applies. No social media plugins are embedded that transmit data when the page is loaded."),
                ("7. Your rights", "Under the GDPR, you have the right of access, rectification, erasure, restriction of processing, data portability, and the right to object to processing based on Art. 6(1)(f) GDPR. To exercise these rights, please use the contact details above."),
                ("8. Right to lodge a complaint", 'You have the right to lodge a complaint with a data protection supervisory authority. The authority responsible for me as controller is the Polish supervisory authority: Urząd Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Warszawa, <a href="https://uodo.gov.pl" rel="noopener">https://uodo.gov.pl</a>. You may also contact the supervisory authority of your usual place of residence.'),
                ("Last updated", "July 2026"),
            ],
        },
        "pl": {
            "eyebrow": "Prywatność",
            "h1": "Polityka prywatności",
            "side": "Ochrona danych",
            "back": "Powrót do strony głównej",
            "sections": [
                ("1. Administrator danych", "Daniel Baran<br>Jasionka 33, 28-300 Jędrzejów, Polska<br>E-mail: kontakt@daniel-baran.com"),
                ("2. Informacje ogólne", "Ta strona internetowa ma wyłącznie charakter informacyjny. Nie są wykorzystywane żadne usługi śledzenia ani analityki i żadne dane osobowe nie są przetwarzane do celów reklamowych. Czcionki są ładowane lokalnie z tej strony; nie następuje połączenie z Google Fonts ani podobnymi usługami."),
                ("3. Hosting (Cloudflare)", 'Ta strona jest hostowana przez Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA. Podczas korzystania ze strony Cloudflare przetwarza technicznie niezbędne dane, takie jak adres IP, data i godzina dostępu, wywołana strona, typ przeglądarki i system operacyjny. Przetwarzanie to jest niezbędne do bezpiecznego i stabilnego działania strony (art. 6 ust. 1 lit. f RODO – prawnie uzasadniony interes). Cloudflare posiada certyfikację w ramach EU-U.S. Data Privacy Framework; stosowane są również standardowe klauzule umowne. Więcej informacji: <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">https://www.cloudflare.com/privacypolicy/</a>'),
                ("4. Wybór języka i lokalne przechowywanie", "Strona udostępnia stałe wersje językowe pod adresami /, /pl/ i /en/. Przy wejściu na stronę główną nagłówek przeglądarki Accept-Language może zostać technicznie oceniony, aby skierować odwiedzających do odpowiedniej wersji językowej. Po wyborze języka albo po automatycznym rozpoznaniu języka może zostać ustawiony technicznie niezbędny plik cookie db-lang z kodem języka de, en albo pl. Służy on wyłącznie do zapisania wyboru języka i prawidłowej nawigacji na tej stronie. Okres przechowywania wynosi 12 miesięcy. Podstawą prawną ustawienia cookie jest § 25 ust. 2 TTDSG; dalsze przetwarzanie odbywa się na podstawie art. 6 ust. 1 lit. f RODO. Dodatkowo ten sam kod języka może zostać zapisany lokalnie w przeglądarce jako wpis localStorage db-lang. Nie odbywa się śledzenie, a wybór języka nie jest przekazywany osobom trzecim."),
                ("5. Kontakt", "W przypadku kontaktu przez formularz kontaktowy, e-mail lub telefon przetwarzam przekazane dane w celu obsługi zapytania i ewentualnych pytań uzupełniających. Formularz kontaktowy jest technicznie przetwarzany przez Cloudflare Workers i dostarczany do mnie e-mailem za pośrednictwem usługi Resend, Resend, Inc., 2261 Market Street #5039, San Francisco, CA 94114, USA. Podstawą prawną jest art. 6 ust. 1 lit. b RODO albo art. 6 ust. 1 lit. f RODO. Dane zostaną usunięte, gdy nie będą już potrzebne do obsługi zapytania i nie będą istnieć ustawowe obowiązki ich przechowywania."),
                ("6. Linki zewnętrzne", "Ta strona zawiera linki do zewnętrznych usług, na przykład LinkedIn i YouTube. Po kliknięciu takiego linku lub odtworzeniu osadzonego materiału opuszczają Państwo tę stronę albo pobierają treści danego dostawcy; zastosowanie ma polityka prywatności tego dostawcy. Nie są osadzone żadne wtyczki mediów społecznościowych, które przekazywałyby dane już przy wczytaniu strony."),
                ("7. Państwa prawa", "Zgodnie z RODO przysługuje Państwu prawo dostępu do danych, sprostowania, usunięcia, ograniczenia przetwarzania, przenoszenia danych oraz sprzeciwu wobec przetwarzania na podstawie art. 6 ust. 1 lit. f RODO. W tym celu proszę skorzystać z danych kontaktowych podanych powyżej."),
                ("8. Prawo wniesienia skargi", 'Mają Państwo prawo wnieść skargę do organu nadzorczego ds. ochrony danych. Organem właściwym dla mnie jako administratora jest polski organ nadzorczy: Urząd Ochrony Danych Osobowych (UODO), ul. Stawki 2, 00-193 Warszawa, <a href="https://uodo.gov.pl" rel="noopener">https://uodo.gov.pl</a>. Mogą Państwo również zwrócić się do organu nadzorczego właściwego dla swojego zwykłego miejsca pobytu.'),
                ("Stan", "lipiec 2026"),
            ],
        },
    },
}

FONT_CSS = """    @font-face { font-family:'Space Grotesk'; font-style:normal; font-weight:400; font-display:swap; src:url('/assets/fonts/space-grotesk-400.woff2') format('woff2'); }
    @font-face { font-family:'Space Grotesk'; font-style:normal; font-weight:500; font-display:swap; src:url('/assets/fonts/space-grotesk-500.woff2') format('woff2'); }
"""

SITE_CSS = """    .site-header { box-sizing:border-box; grid-template-columns:auto minmax(0,1fr) auto !important; }
    .site-header > * { min-width:0; }
    .mobile-nav { display:none; }
    .mobile-menu summary::-webkit-details-marker { display:none; }
    .mobile-menu:not([open]) .mobile-menu-panel { display:none !important; }
    .mobile-menu[open] .mobile-menu-panel { display:grid !important; }
    .menu-icon { display:grid; gap:5px; width:20px; }
    .menu-icon span { display:block; height:1.5px; background:#0D0D0C; }
    [id] { scroll-margin-top:72px; }
    img { max-width:100%; }
    .split-grid, .career-row, .acc-button, .acc-content-grid { min-width:0; }
    .split-grid > *, .career-row > *, .acc-button > *, .acc-content-grid > * { min-width:0; }
    .case-row { position:relative; isolation:isolate; text-decoration:none; overflow:visible; }
    .case-row > * { min-width:0; }
    .case-row::before { content:""; position:absolute; inset:0; background:#DAD7CF; opacity:0; transform:scaleX(0.985); transform-origin:left center; transition:opacity 0.35s cubic-bezier(0.62,0.05,0.01,0.99), transform 0.35s cubic-bezier(0.62,0.05,0.01,0.99); z-index:-1; pointer-events:none; }
    .case-row::after { content:""; position:absolute; top:0; bottom:0; left:0; width:0; background:#0D0D0C; transition:width 0.35s cubic-bezier(0.62,0.05,0.01,0.99); pointer-events:none; }
    .case-thumb { transition:background 0.35s cubic-bezier(0.62,0.05,0.01,0.99); }
    .case-thumb img { transition:transform 0.55s cubic-bezier(0.62,0.05,0.01,0.99), filter 0.55s cubic-bezier(0.62,0.05,0.01,0.99); }
    .case-meta, .case-role, .case-arrow { transition:color 0.35s cubic-bezier(0.62,0.05,0.01,0.99), transform 0.35s cubic-bezier(0.62,0.05,0.01,0.99); }
    .case-title { border-bottom-color:transparent !important; overflow-wrap:anywhere; transition:color 0.35s cubic-bezier(0.62,0.05,0.01,0.99); }
    .case-row:hover::before, .case-row:focus-visible::before { opacity:1; transform:scaleX(1); }
    .case-row:hover::after, .case-row:focus-visible::after { width:4px; }
    .case-row:hover .case-thumb, .case-row:focus-visible .case-thumb { background:#CEC9BE !important; }
    .case-row:hover .case-thumb img, .case-row:focus-visible .case-thumb img { transform:scale(1.045); filter:contrast(1.04); }
    .case-row:hover .case-meta, .case-row:hover .case-role, .case-row:focus-visible .case-meta, .case-row:focus-visible .case-role { color:#0D0D0C !important; }
    .case-row:hover .case-arrow, .case-row:focus-visible .case-arrow { transform:translateX(8px); color:#0D0D0C; }
    @media (max-width: 1100px) {
      .site-tagline { display:none !important; }
      .site-header { grid-template-columns:auto 1fr auto !important; }
    }
    @media (max-width: 860px) {
      html, body { max-width:100%; overflow-x:hidden; }
      .site-header { grid-template-columns:1fr auto !important; gap:14px !important; }
      .site-nav { display:none !important; }
      .mobile-nav { display:block !important; justify-self:end; position:relative; }
      .mobile-menu-panel { box-sizing:border-box; }
    }
    @media (max-width: 820px) {
      .case-row { grid-template-columns:1fr !important; gap:18px !important; align-items:start !important; }
      .case-row .case-arrow { display:none !important; }
    }
    @media (max-width: 720px) {
      .split-grid { grid-template-columns:1fr !important; gap:18px !important; }
      .split-grid > span:empty { display:none !important; }
      .career-row { grid-template-columns:1fr !important; gap:10px !important; align-items:start !important; }
      .career-row h3, .career-row p { max-width:100% !important; }
      .acc-button { grid-template-columns:1fr auto !important; gap:14px !important; align-items:start !important; }
      .acc-button > span:first-child { grid-column:1 / -1; }
      .acc-button > span:nth-child(2) { overflow-wrap:anywhere; }
      .acc-button > span:last-child { justify-self:end; }
      .acc-content-grid { grid-template-columns:1fr !important; gap:16px !important; }
      .acc-content-grid > span:first-child { display:none !important; }
      [style*="grid-template-columns:minmax(160px,220px) 1fr"] { grid-template-columns:1fr !important; gap:18px !important; }
    }
    @media (max-width: 520px) {
      .site-header { grid-template-columns:1fr auto !important; gap:14px !important; padding:12px 16px !important; }
      .hero-media { align-items:stretch !important; margin-right:0 !important; }
      .hero-media img { width:100% !important; max-width:calc(100vw - 32px) !important; min-width:0 !important; }
      [data-screen-label="Profil Inhalt"] h2 { font-size:3rem !important; line-height:0.9 !important; }
    }
    @media (max-width: 380px) {
      [data-screen-label="Profil Inhalt"] h2 { font-size:2.65rem !important; }
    }
"""

CASE_MOBILE_CSS = """    @media (max-width: 767px) {
      .case-root .site-header { grid-template-columns:minmax(0,1fr) auto !important; gap:10px 12px !important; padding:12px 16px !important; }
      .case-root .site-header > span:first-child { display:none !important; }
      .case-root .site-header > span:nth-child(2) { min-width:0; overflow:hidden; text-overflow:ellipsis; }
      .case-root .site-header nav { display:flex !important; justify-content:flex-end !important; align-items:center !important; gap:12px !important; min-width:0 !important; }
      .case-root .site-header nav span { gap:8px !important; }
      .case-root .mobile-nav { display:none !important; }
      .no-track .case-sticky { padding-top:88px; }
      .no-track .case-aside { padding:0 20px 28px; box-sizing:border-box; }
      .no-track .case-aside h1 { max-width:100% !important; font-size:clamp(1.75rem,8vw,2.35rem) !important; line-height:0.98 !important; overflow-wrap:anywhere; }
      .no-track .case-aside p, .no-track .case-aside dd { max-width:100% !important; overflow-wrap:anywhere; }
      .no-track .case-aside dl > div { grid-template-columns:minmax(92px,34%) minmax(0,1fr) !important; gap:14px !important; }
      .no-track .slides-col { margin-top:0; }
      .no-track .panels { display:grid !important; grid-template-columns:1fr !important; gap:0 !important; overflow:visible !important; scroll-snap-type:none !important; height:auto !important; align-items:stretch !important; }
      .no-track .panel-wrap { scroll-snap-align:none !important; width:100% !important; height:auto !important; display:block !important; }
      .no-track .panel-wrap .panel { min-height:auto !important; width:100% !important; max-width:none !important; border-left:0 !important; border-right:0 !important; padding:28px 20px !important; overflow:visible !important; }
      .no-track .panel p, .no-track .panel h2, .no-track .panel span, .no-track .panel dd { max-width:100% !important; overflow-wrap:anywhere; }
      .no-track .panel [style*="grid-template-columns:minmax(0,1fr) minmax(0,1fr)"],
      .no-track .panel [style*="grid-template-columns: minmax(0px, 1fr) minmax(0px, 1fr)"],
      .no-track .panel [style*="grid-template-columns:minmax(0,3fr) minmax(0,2fr)"],
      .no-track .panel [style*="grid-template-columns: minmax(0px, 3fr) minmax(0px, 2fr)"],
      .no-track .panel [style*="grid-template-columns:repeat(3,minmax(0,1fr))"],
      .no-track .panel [style*="grid-template-columns: repeat(3, minmax(0px, 1fr))"] { grid-template-columns:1fr !important; gap:22px !important; align-items:start !important; }
      .no-track .panel [style*="display:flex; align-items:flex-start"],
      .no-track .panel [style*="display: flex"][style*="align-items: flex-start"] { display:grid !important; grid-template-columns:1fr !important; gap:18px !important; }
      .no-track .panel span[aria-hidden="true"] { display:none !important; }
      .no-track .case-hud { display:none !important; }
    }
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
        title = CASE_SEO_TITLES[slug][lang]
        return title, CASE_DESCRIPTIONS[slug][lang]
    return TITLES[kind][lang], DESCRIPTIONS[kind][lang]


def structured_data(kind: str, lang: str, slug: str | None = None) -> str:
    title, desc = metadata(kind, lang, slug)
    url = SITE + route(kind, lang, slug)
    person = {
        "@type": "Person",
        "@id": f"{SITE}/#person",
        "name": "Daniel Baran",
        "url": SITE,
        "image": f"{SITE}/assets/redesign/DSCF5508.webp",
        "jobTitle": "Senior IT Project & Product Manager",
        "sameAs": [LINKEDIN],
        "knowsAbout": [
            "IT project management",
            "Product ownership",
            "AI enablement",
            "Streaming infrastructure",
            "Digital products",
        ],
    }
    graph: list[dict[str, object]] = [person]

    if kind == "case":
        graph.append(
            {
                "@type": "CreativeWork",
                "@id": f"{url}#case-study",
                "name": title,
                "description": desc,
                "url": url,
                "inLanguage": lang,
                "author": {"@id": f"{SITE}/#person"},
                "image": f"{SITE}/assets/redesign/{CASE_IMAGE_BY_SLUG[slug]}",
            }
        )
    elif kind == "projects":
        graph.append(
            {
                "@type": "CollectionPage",
                "@id": f"{url}#webpage",
                "name": title,
                "description": desc,
                "url": url,
                "inLanguage": lang,
                "about": {"@id": f"{SITE}/#person"},
                "mainEntity": {
                    "@type": "ItemList",
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": idx + 1,
                            "url": SITE + route("case", lang, case_slug),
                            "name": CASE_SEO_TITLES[case_slug][lang],
                        }
                        for idx, case_slug in enumerate(CASE_ORDER)
                    ],
                },
            }
        )
    elif kind in {"imprint", "privacy"}:
        graph.append(
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "name": title,
                "description": desc,
                "url": url,
                "inLanguage": lang,
                "about": {"@id": f"{SITE}/#person"},
            }
        )
    else:
        graph.append(
            {
                "@type": "ProfilePage",
                "@id": f"{url}#webpage",
                "name": title,
                "description": desc,
                "url": url,
                "inLanguage": lang,
                "mainEntity": {"@id": f"{SITE}/#person"},
            }
        )

    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    safe_data = data.replace("</", "<\\/")
    return f'<script type="application/ld+json">{safe_data}</script>'


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
{structured_data(kind, lang, slug)}
{js_config(lang, kind, slug)}
<script src="{RUNTIME}"></script>
</head>"""


def legal_css() -> str:
    return f"""<style>
{FONT_CSS}{SITE_CSS}
html, body {{ margin:0; padding:0; background:#E7E5E0; }}
body {{ font-family:'Space Grotesk', 'Helvetica Neue', Arial, sans-serif; color:#0D0D0C; -webkit-font-smoothing:antialiased; }}
a {{ color:#0D0D0C; text-decoration:none; }}
:focus-visible {{ outline:2px solid #2A2AE5; outline-offset:3px; }}
::selection {{ background:#2A2AE5; color:#E7E5E0; }}
.legal-shell {{ min-height:100svh; background:#E7E5E0; color:#0D0D0C; overflow-x:hidden; }}
.legal-hero {{ padding:clamp(130px,20vh,220px) clamp(20px,3vw,48px) clamp(48px,7vh,88px); box-sizing:border-box; }}
.legal-eyebrow {{ margin:0 0 18px; font-size:0.78rem; letter-spacing:0.12em; text-transform:uppercase; color:#4A4945; }}
.legal-hero h1 {{ margin:0; font-weight:500; text-transform:uppercase; font-size:clamp(2.6rem,10.5vw,7rem); line-height:0.9; letter-spacing:0; max-width:12ch; overflow-wrap:anywhere; }}
.legal-layout {{ padding:0 clamp(20px,3vw,48px) clamp(56px,9vh,110px); box-sizing:border-box; display:grid; grid-template-columns:minmax(160px,220px) minmax(0,760px); gap:clamp(24px,4vw,64px); }}
.legal-side {{ margin:0; font-size:0.78rem; letter-spacing:0.12em; text-transform:uppercase; color:#4A4945; }}
.legal-content {{ border-top:1.5px solid #0D0D0C; padding-top:clamp(20px,3vh,32px); min-width:0; }}
.legal-content h2 {{ margin:clamp(32px,5vh,52px) 0 12px; font-weight:500; text-transform:uppercase; font-size:clamp(1.25rem,2.2vw,1.9rem); line-height:1.05; letter-spacing:0; }}
.legal-content h2:first-child {{ margin-top:0; }}
.legal-content p {{ margin:0 0 18px; font-size:0.98rem; line-height:1.55; color:#4A4945; max-width:68ch; }}
.legal-content a {{ border-bottom:1.5px solid #4A4945; padding-bottom:1px; color:#4A4945; overflow-wrap:anywhere; }}
.legal-content a:hover {{ border-bottom-color:#2A2AE5; color:#0D0D0C; }}
.legal-back {{ display:inline-block; margin-top:clamp(22px,3.5vh,32px); font-weight:500; font-size:0.95rem; border-bottom:1.5px solid #0D0D0C; padding-bottom:3px; }}
.legal-footer {{ border-top:1.5px solid #0D0D0C; padding:18px clamp(20px,3vw,48px); display:flex; flex-wrap:wrap; justify-content:space-between; gap:12px; font-size:0.78rem; letter-spacing:0.04em; color:#4A4945; }}
.legal-footer a {{ color:#4A4945; border-bottom:1.5px solid transparent; padding-bottom:2px; }}
.legal-footer a:hover {{ border-bottom-color:#2A2AE5; }}
@media (max-width:720px) {{
  .legal-layout {{ grid-template-columns:1fr; gap:18px; }}
}}
@media (max-width:520px) {{
  .legal-hero {{ padding:96px 16px 42px; }}
  .legal-layout {{ padding-left:16px; padding-right:16px; }}
  .legal-hero h1 {{ font-size:clamp(2.25rem,13vw,4.2rem); max-width:100%; }}
}}
</style>"""


def static_nav_labels(lang: str) -> dict[str, str]:
    return {
        "de": {
            "tagline": "Senior IT Project & Product Manager · Remote · DACH",
            "about": "Über mich",
            "services": "Leistungen",
            "process": "Prozess",
            "projects": "Projekte",
            "contact": "Kontakt",
            "menu": "Menü",
            "footer_name": "Daniel Baran · Freelance IT- & Product-Delivery",
            "imprint": "Impressum",
            "privacy": "Datenschutz",
        },
        "en": {
            "tagline": "Senior IT Project & Product Manager · Remote · DACH",
            "about": "About",
            "services": "Services",
            "process": "Process",
            "projects": "Projects",
            "contact": "Contact",
            "menu": "Menu",
            "footer_name": "Daniel Baran · Freelance IT & Product Delivery",
            "imprint": "Legal Notice",
            "privacy": "Privacy",
        },
        "pl": {
            "tagline": "Senior IT Project & Product Manager · Zdalnie · DACH",
            "about": "O mnie",
            "services": "Usługi",
            "process": "Proces",
            "projects": "Projekty",
            "contact": "Kontakt",
            "menu": "Menu",
            "footer_name": "Daniel Baran · Freelance IT & Product Delivery",
            "imprint": "Nota prawna",
            "privacy": "Prywatność",
        },
    }[lang]


def lang_cookie_onclick(code: str) -> str:
    return f"document.cookie='db-lang={code}; Path=/; Max-Age=31536000; SameSite=Lax; Secure';"


def static_mobile_nav(lang: str, current_kind: str) -> str:
    labels = static_nav_labels(lang)
    links = [
        (route("about", lang), labels["about"], False),
        (route("home", lang) + "#leistungen", labels["services"], False),
        (route("home", lang) + "#prozess", labels["process"], False),
        (route("projects", lang), labels["projects"], False),
        (route("home", lang) + "#kontakt", labels["contact"], False),
    ]
    link_html = "\n".join(
        f'        <a href="{href}" style="font-weight:500; text-transform:uppercase; letter-spacing:0.04em; border-bottom:1.5px solid transparent; padding:0 0 4px;">{html.escape(label)}</a>'
        for href, label, _ in links
    )
    lang_links = "\n".join(
        f'          <a href="{href}" onclick="{lang_cookie_onclick(code)}"{" aria-current=\"page\"" if code == lang else ""} style="border-bottom:1.5px solid {"#0D0D0C" if code == lang else "transparent"}; padding-bottom:2px; color:{"#0D0D0C" if code == lang else "#4A4945"};">{code.upper()}</a>'
        for code, href in alt_routes(current_kind).items()
    )
    return f"""    <details class="mobile-nav mobile-menu" style="display:none;">
      <summary aria-label="{html.escape(labels['menu'])}" style="list-style:none; width:36px; height:32px; display:grid; place-items:center; cursor:pointer;">
        <span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span>
      </summary>
      <div class="mobile-menu-panel" style="position:fixed; top:57px; left:0; right:0; z-index:11; display:grid; gap:16px; padding:18px 16px 20px; border-bottom:1.5px solid #0D0D0C; background:#E7E5E0;">
{link_html}
        <span style="display:flex; gap:14px; padding-top:4px; color:#4A4945;">
{lang_links}
        </span>
      </div>
    </details>"""


def static_header(lang: str, current_kind: str) -> str:
    labels = static_nav_labels(lang)
    lang_links = "".join(
        f'<a href="{href}" onclick="{lang_cookie_onclick(code)}"{" aria-current=\"page\"" if code == lang else ""} style="border-bottom:1.5px solid {"#0D0D0C" if code == lang else "transparent"}; padding-bottom:2px; color:{"#0D0D0C" if code == lang else "#4A4945"};">{code.upper()}</a>'
        for code, href in alt_routes(current_kind).items()
    )
    return f"""  <header class="site-header" style="position:fixed; top:0; left:0; right:0; z-index:10; display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:24px; padding:14px clamp(20px,3vw,48px); border-bottom:1.5px solid #0D0D0C; background:#E7E5E0; font-size:0.8rem; letter-spacing:0.02em;">
    <a href="{route('home', lang)}" style="font-weight:500; text-transform:uppercase; letter-spacing:0.04em; white-space:nowrap;">Daniel Baran</a>
    <div class="site-tagline" style="color:#4A4945; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; min-width:0;">{html.escape(labels['tagline'])}</div>
    <nav class="site-nav" aria-label="Navigation" style="display:flex; justify-content:flex-end; align-items:center; gap:22px; white-space:nowrap;">
      <a href="{route('about', lang)}" style="border-bottom:1.5px solid transparent; padding-bottom:2px;">{html.escape(labels['about'])}</a>
      <a href="{route('home', lang)}#leistungen" style="border-bottom:1.5px solid transparent; padding-bottom:2px;">{html.escape(labels['services'])}</a>
      <a href="{route('home', lang)}#prozess" style="border-bottom:1.5px solid transparent; padding-bottom:2px;">{html.escape(labels['process'])}</a>
      <a href="{route('projects', lang)}" style="border-bottom:1.5px solid transparent; padding-bottom:2px;">{html.escape(labels['projects'])}</a>
      <a href="{route('home', lang)}#kontakt" style="border-bottom:1.5px solid transparent; padding-bottom:2px;">{html.escape(labels['contact'])}</a>
      <span style="display:flex; gap:10px; margin-left:14px; color:#4A4945;">{lang_links}</span>
    </nav>
{static_mobile_nav(lang, current_kind)}
  </header>"""


def legal_body(kind: str, lang: str) -> str:
    labels = static_nav_labels(lang)
    copy = LEGAL_COPY[kind][lang]
    sections = "\n".join(
        f'        <h2>{html.escape(title)}</h2>\n        <p>{text}</p>'
        for title, text in copy["sections"]
    )
    return f"""<body>
<div class="legal-shell">
{static_header(lang, kind)}
  <main>
    <section class="legal-hero">
      <p class="legal-eyebrow">{html.escape(copy['eyebrow'])}</p>
      <h1>{html.escape(copy['h1'])}</h1>
      <a class="legal-back" href="{route('home', lang)}">{html.escape(copy['back'])}</a>
    </section>
    <section class="legal-layout" aria-label="{html.escape(copy['h1'])}">
      <p class="legal-side">{html.escape(copy['side'])}</p>
      <article class="legal-content">
{sections}
      </article>
    </section>
  </main>
  <footer class="legal-footer">
    <span>{html.escape(labels['footer_name'])}</span>
    <span style="display:flex; gap:18px;">
      <a href="{route('imprint', lang)}">{html.escape(labels['imprint'])}</a>
      <a href="{route('privacy', lang)}">{html.escape(labels['privacy'])}</a>
    </span>
  </footer>
</div>
</body>"""


def render_legal(kind: str, lang: str) -> str:
    doc_head = head(lang, kind).replace(f'<script src="{RUNTIME}"></script>\n', "")
    doc_head = re.sub(r"<script>window\.__DB_DEFAULT_LANG=.*?</script>\n", "", doc_head)
    return doc_head.replace("</head>", legal_css() + "\n</head>") + "\n" + legal_body(kind, lang) + "\n</html>\n"


def normalize_fonts(body: str) -> str:
    body = re.sub(r"\s*<link rel=\"preconnect\" href=\"https://fonts\.googleapis\.com\">\n?", "\n", body)
    body = re.sub(r"\s*<link rel=\"preconnect\" href=\"https://fonts\.gstatic\.com\" crossorigin>\n?", "\n", body)
    body = re.sub(r"\s*<link href=\"https://fonts\.googleapis\.com[^\"]+\" rel=\"stylesheet\">\n?", "\n", body)
    body = body.replace("'Archivo'", "'Space Grotesk'")
    body = body.replace("font-family:'Space Grotesk', sans-serif", "font-family:'Space Grotesk', 'Helvetica Neue', Arial, sans-serif")
    body = body.replace("<style>\n", "<style>\n" + FONT_CSS + SITE_CSS, 1)
    body = re.sub(r"letter-spacing:-0\.[0-9]+em", "letter-spacing:0", body)
    return body


def update_case_mobile_layout(body: str) -> str:
    if ".case-root .site-header > span:first-child" in body:
        return body
    needle = "    @media (prefers-reduced-motion: reduce) {\n"
    if needle not in body:
        raise RuntimeError("Case mobile CSS insertion point not found")
    return body.replace(needle, CASE_MOBILE_CSS + needle, 1)


def normalize_assets(body: str) -> str:
    body = body.replace('src="uploads/DSCF5508.jpg"', 'src="/assets/redesign/DSCF5508.webp"')
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
        r'<a href="#projekte"([^>]*>\{\{ t\.navProjects \}\}</a>)',
        rf'<a href="{route("projects", lang)}"\1',
        body,
    )

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


def anchor_href(kind: str, lang: str, anchor: str) -> str:
    if kind == "home":
        return f"#{anchor}"
    return route("home", lang) + f"#{anchor}"


def mobile_nav(lang: str, kind: str) -> str:
    links = [
        (route("about", lang), "{{ t.navAbout }}", kind == "about"),
        (anchor_href(kind, lang, "leistungen"), "{{ t.navServices }}", False),
        (anchor_href(kind, lang, "prozess"), "{{ t.navProcess }}", False),
        (route("projects", lang), "{{ t.navProjects }}", kind == "projects"),
        (anchor_href(kind, lang, "kontakt"), "{{ t.navContact }}", False),
    ]
    link_parts = []
    for href, label, current in links:
        current_attr = ' aria-current="page"' if current else ""
        link_parts.append(
            f'        <a href="{href}"{current_attr} onclick="this.closest(\'details\').removeAttribute(\'open\')" style="font-weight:500; text-transform:uppercase; letter-spacing:0.04em; border-bottom:1.5px solid transparent; padding:0 0 4px;" style-hover="border-bottom-color:#2A2AE5;">{label}</a>'
        )
    link_html = "\n".join(link_parts)
    return f"""    <details class="mobile-nav mobile-menu" style="display:none;">
      <summary aria-label="{{{{ t.navMenuLabel }}}}" style="list-style:none; width:36px; height:32px; display:grid; place-items:center; cursor:pointer;">
        <span class="menu-icon" aria-hidden="true"><span></span><span></span><span></span></span>
      </summary>
      <div class="mobile-menu-panel" style="position:fixed; top:57px; left:0; right:0; z-index:11; display:grid; gap:16px; padding:18px 16px 20px; border-bottom:1.5px solid #0D0D0C; background:#E7E5E0;">
{link_html}
        <span style="display:flex; gap:14px; padding-top:4px; color:#4A4945;">
          <sc-for list="{{{{ langs }}}}" as="lg" hint-placeholder-count="3">
            <button type="button" onClick="{{{{ lg.select }}}}" aria-current="{{{{ lg.current }}}}" style="background:none; border:none; padding:0 0 2px; cursor:pointer; font-size:0.8rem; letter-spacing:0.02em; color:{{{{ lg.color }}}}; border-bottom:1.5px solid {{{{ lg.underline }}}};" style-hover="border-bottom-color:#2A2AE5;">{{{{ lg.label }}}}</button>
          </sc-for>
        </span>
      </div>
    </details>"""


def update_responsive_markup(body: str, lang: str, kind: str) -> str:
    body = body.replace('<header style="position:fixed;', '<header class="site-header" style="position:fixed;', 1)
    body = body.replace(
        '<div style="color:#4A4945; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; min-width:0;">{{ t.tagline }}</div>',
        '<div class="site-tagline" style="color:#4A4945; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; min-width:0;">{{ t.tagline }}</div>',
        1,
    )
    body = body.replace(
        '<nav aria-label="Hauptnavigation" style="display:flex;',
        '<nav class="site-nav" aria-label="Hauptnavigation" style="display:flex;',
        1,
    )
    body = body.replace("</nav>\n  </header>", "</nav>\n" + mobile_nav(lang, kind) + "\n  </header>", 1)
    body = body.replace(
        '<div style="display:flex; flex-direction:column; align-items:flex-end; gap:clamp(12px,2svh,18px); margin-top:auto; margin-right:calc(-1 * clamp(20px,3vw,48px)); padding-top:clamp(12px,2svh,24px);">',
        '<div class="hero-media" style="display:flex; flex-direction:column; align-items:flex-end; gap:clamp(12px,2svh,18px); margin-top:auto; margin-right:calc(-1 * clamp(20px,3vw,48px)); padding-top:clamp(12px,2svh,24px);">',
        1,
    )
    body = body.replace('alt="" loading="lazy"', 'alt="{{ c.title }}" loading="lazy"')
    body = body.replace(
        'src="/assets/redesign/DSCF5508.webp" alt="Daniel Baran" width="640" height="274"',
        'src="/assets/redesign/DSCF5508.webp" alt="Daniel Baran" width="640" height="274" loading="eager" decoding="async" fetchpriority="high"',
        1,
    )
    body = body.replace(
        '<button type="button" onClick="{{ sv.toggle }}" aria-expanded="{{ sv.open }}" style="width:100%; display:grid;',
        '<button class="acc-button" type="button" onClick="{{ sv.toggle }}" aria-expanded="{{ sv.open }}" style="width:100%; display:grid;',
    )
    body = body.replace(
        '<button type="button" onClick="{{ p.toggle }}" aria-expanded="{{ p.open }}" style="width:100%; display:grid;',
        '<button class="acc-button" type="button" onClick="{{ p.toggle }}" aria-expanded="{{ p.open }}" style="width:100%; display:grid;',
    )
    body = body.replace(
        '<button type="button" onClick="{{ s.toggle }}" aria-expanded="{{ s.open }}" style="width:100%; display:grid;',
        '<button class="acc-button" type="button" onClick="{{ s.toggle }}" aria-expanded="{{ s.open }}" style="width:100%; display:grid;',
    )
    body = body.replace(
        '<button type="button" onClick="{{ g.toggle }}" aria-expanded="{{ g.open }}" style="width:100%; display:grid;',
        '<button class="acc-button" type="button" onClick="{{ g.toggle }}" aria-expanded="{{ g.open }}" style="width:100%; display:grid;',
    )
    body = body.replace(
        '<div style="display:grid; grid-template-columns:minmax(160px,220px) 1fr; gap:clamp(24px,4vw,64px); padding:0 0',
        '<div class="acc-content-grid" style="display:grid; grid-template-columns:minmax(160px,220px) 1fr; gap:clamp(24px,4vw,64px); padding:0 0',
    )
    body = body.replace(
        '<div data-reveal style="display:grid; grid-template-columns:minmax(160px,220px) 1fr;',
        '<div data-reveal class="split-grid" style="display:grid; grid-template-columns:minmax(160px,220px) 1fr;',
    )
    body = body.replace(
        '<div style="display:grid; grid-template-columns:minmax(160px,220px) 1fr;',
        '<div class="split-grid" style="display:grid; grid-template-columns:minmax(160px,220px) 1fr;',
    )
    body = body.replace(
        '<div data-reveal style="display:grid; grid-template-columns:minmax(160px,220px) minmax(200px,26ch) 1fr;',
        '<div data-reveal class="career-row" style="display:grid; grid-template-columns:minmax(160px,220px) minmax(200px,26ch) 1fr;',
    )
    body = body.replace(
        '<span style="display:block; aspect-ratio:3/2; overflow:hidden; background:#EDEBE5;">',
        '<span class="case-thumb" style="display:block; aspect-ratio:3/2; overflow:hidden; background:#EDEBE5;">',
    )
    body = body.replace(
        '<span style="display:block; aspect-ratio:3/2; overflow:hidden; background:#DEDCD5;">',
        '<span class="case-thumb" style="display:block; aspect-ratio:3/2; overflow:hidden; background:#DEDCD5;">',
    )
    body = body.replace(
        '<span style="display:block; margin:0 0 12px; font-size:0.78rem; letter-spacing:0.04em; color:#4A4945;">{{ c.num }} · {{ c.chips }}</span>',
        '<span class="case-meta" style="display:block; margin:0 0 12px; font-size:0.78rem; letter-spacing:0.04em; color:#4A4945;">{{ c.num }} · {{ c.chips }}</span>',
    )
    body = body.replace(
        '<span style="display:block; margin:0 0 14px; font-size:0.78rem; letter-spacing:0.04em; color:#4A4945;">{{ c.num }} · {{ c.chips }}</span>',
        '<span class="case-meta" style="display:block; margin:0 0 14px; font-size:0.78rem; letter-spacing:0.04em; color:#4A4945;">{{ c.num }} · {{ c.chips }}</span>',
    )
    body = body.replace(
        '<span style="display:inline; font-weight:500; text-transform:uppercase; font-size:clamp(1.3rem,2.6vw,2.2rem); line-height:1.0; letter-spacing:0; border-bottom:1.5px solid transparent; padding-bottom:2px; transition:border-color 0.3s cubic-bezier(0.62,0.05,0.01,0.99);" class="case-title">{{ c.title }}</span>',
        '<span class="case-title" style="display:inline; font-weight:500; text-transform:uppercase; font-size:clamp(1.3rem,2.6vw,2.2rem); line-height:1.0; letter-spacing:0;">{{ c.title }}</span>',
    )
    body = body.replace(
        '<span style="display:block; margin-top:10px; font-size:0.85rem; line-height:1.4; letter-spacing:0.02em; color:#4A4945;">{{ c.role }}</span>',
        '<span class="case-role" style="display:block; margin-top:10px; font-size:0.85rem; line-height:1.4; letter-spacing:0.02em; color:#4A4945;">{{ c.role }}</span>',
    )
    body = body.replace(
        '<span style="display:block; margin-top:12px; font-size:0.85rem; line-height:1.4; letter-spacing:0.02em; color:#4A4945;">{{ c.role }}</span>',
        '<span class="case-role" style="display:block; margin-top:12px; font-size:0.85rem; line-height:1.4; letter-spacing:0.02em; color:#4A4945;">{{ c.role }}</span>',
    )
    return body


def update_case_hover(body: str) -> str:
    old = """
    document.querySelectorAll("a[data-reveal]").forEach((a) => {
      const t = a.querySelector(".case-title");
      if (!t) return;
      a.addEventListener("mouseenter", () => { t.style.borderBottomColor = "#2A2AE5"; });
      a.addEventListener("mouseleave", () => { t.style.borderBottomColor = "transparent"; });
    });
"""
    return body.replace(old, "")


def update_hash_scroll(body: str) -> str:
    old = """  componentDidMount() {
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;"""
    new = """  componentDidMount() {
    const scrollToHash = () => {
      if (!window.location.hash) return;
      let id = window.location.hash.slice(1);
      try { id = decodeURIComponent(id); } catch (e) {}
      const target = document.getElementById(id);
      if (target) target.scrollIntoView({ block: "start" });
    };
    window.setTimeout(scrollToHash, 0);
    window.setTimeout(scrollToHash, 250);
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;"""
    return body.replace(old, new)


def update_copy_and_case_text(body: str) -> str:
    replacements = {
        'navProjects: "Projekte", navContact: "Kontakt",': 'navProjects: "Projekte", navContact: "Kontakt", navMenuLabel: "Menü",',
        'navProjects: "Projects", navContact: "Contact",': 'navProjects: "Projects", navContact: "Contact", navMenuLabel: "Menu",',
        'navProjects: "Projekty", navContact: "Kontakt",': 'navProjects: "Projekty", navContact: "Kontakt", navMenuLabel: "Menu",',
        'label: "Etwas anderes, erzähle ich im Gespräch"': 'label: "Etwas anderes, das ich im Gespräch erläutere"',
        'label: "Something else, I\'ll explain in the call"': 'label: "Something else to explain in the call"',
        'label: "Coś innego, opowiem w rozmowie"': 'label: "Coś innego do omówienia w rozmowie"',
        'h1: "Systemmigration im Konzernverbund"': 'h1: "Systemmigration im Konzernverbund: nahtloser Wechsel eines zentralen Werkstatt-Systems"',
        'h1: "System migration within the group"': 'h1: "System migration within the group: a seamless switch for a central workshop system"',
        'h1: "Migracja systemów w ramach grupy"': 'h1: "Migracja systemów w grupie: płynna zmiana centralnego systemu warsztatowego"',
        'h1: "Dokumentation für Fahrzeugumbauten"': 'h1: "Dokumentation für Fahrzeugumbauten: Service-Wissen weltweit auffindbar machen"',
        'h1: "Documentation for vehicle conversions"': 'h1: "Documentation for vehicle conversions: making service knowledge findable worldwide"',
        'h1: "Dokumentacja przebudów pojazdów"': 'h1: "Dokumentacja przebudów pojazdów: wiedza serwisowa dostępna globalnie"',
        "2019 bis 2022": "2021-2023",
        "2019 to 2022": "2021-2023",
        "2019 do 2022": "2021-2023",
        "2022 haben wir das Projekt eingestellt.": "2023 haben wir das Projekt eingestellt.",
        "In 2022 we shut the project down.": "In 2023 we shut the project down.",
        "W 2022 roku zakończyliśmy projekt.": "W 2023 roku zakończyliśmy projekt.",
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
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
    try {{ document.cookie = "db-lang=" + code + "; Path=/; Max-Age=31536000; SameSite=Lax; Secure"; }} catch (e) {{}}
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
        '<p style="margin:clamp(16px,2.5vh,24px) 0 0; font-size:0.95rem; line-height:1.4; color:#4A4945; max-width:42ch;">{{ t.contactIntro }}</p>',
        '<p style="margin:clamp(16px,2.5vh,24px) 0 0; font-size:0.95rem; line-height:1.4; color:#4A4945; max-width:42ch;">{{ t.contactIntro }}</p>\n'
        '      <p style="margin:14px 0 0; font-size:0.95rem; line-height:1.4; color:#4A4945; max-width:42ch;">\n'
        '        <a href="mailto:kontakt@daniel-baran.com" style="color:#0D0D0C; border-bottom:1.5px solid #0D0D0C; padding-bottom:2px;" style-hover="border-bottom-color:#2A2AE5;">kontakt@daniel-baran.com</a>\n'
        '      </p>',
    )
    body = body.replace(
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); display:grid;',
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); position:relative; display:grid;',
    )
    body = body.replace(
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); position:relative; display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr)); gap:clamp(32px,5vw,80px); align-items:start; border-top:1.5px solid #0D0D0C; padding-top:clamp(24px,4vh,40px);">',
        '<form data-reveal onSubmit="{{ submitForm }}" novalidate style="margin-top:clamp(32px,5vh,56px); position:relative; display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr)); gap:clamp(32px,5vw,80px); align-items:start; border-top:1.5px solid #0D0D0C; padding-top:clamp(24px,4vh,40px);">\n'
        '      <input type="text" name="website" autocomplete="off" tabindex="-1" aria-hidden="true" style="position:absolute; inset:0 auto auto 0; width:1px; height:1px; opacity:0; clip-path:inset(50%); pointer-events:none;">',
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
    video_src = f"https://www.youtube-nocookie.com/embed/{html.escape(VESTIUM_YOUTUBE_ID, quote=True)}?rel=0&modestbranding=1"
    body = body.replace(
        '<x-import component-from-global-scope="image-slot" from="./image-slot.js" id="case05-prototype" shape="rect" radius="0" placeholder="{{ t.shotPlaceholder }}" hint-size="100%,360px" style="width:100%; height:100%; display:block;"></x-import>',
        '<sc-if value="{{ hasVestiumVideo }}" hint-placeholder-val="{{ false }}">\n'
        f'                  <iframe src="{video_src}" title="Vestium prototype video" loading="lazy" allow="fullscreen; encrypted-media; picture-in-picture" allowfullscreen style="width:100%; height:100%; border:0; display:block; background:#0D0D0C;"></iframe>\n'
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
    body = update_copy_and_case_text(body)
    body = update_responsive_markup(body, lang, kind)
    body = update_case_hover(body)
    body = update_hash_scroll(body)
    if kind == "case":
        body = update_case_mobile_layout(body)
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
    portrait = HANDOFF / "uploads" / "DSCF5508.jpg"
    shutil.copy2(portrait, target / "DSCF5508.jpg")
    if not shutil.which("cwebp"):
        raise RuntimeError("cwebp is required to generate assets/redesign/DSCF5508.webp")
    subprocess.run(
        [
            "cwebp",
            "-quiet",
            "-q",
            "82",
            "-resize",
            "1280",
            "0",
            str(portrait),
            "-o",
            str(target / "DSCF5508.webp"),
        ],
        check=True,
    )


def write_pages() -> None:
    for kind, source_name in PAGE_SOURCES.items():
        for lang in LANGS:
            output = out_path(kind, lang)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(transform(source_name, lang, kind), encoding="utf-8")

    for kind in ("imprint", "privacy"):
        for lang in LANGS:
            output = out_path(kind, lang)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(render_legal(kind, lang), encoding="utf-8")

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
