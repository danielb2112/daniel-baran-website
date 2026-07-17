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
        "de": "Daniel Baran | IT Project & Product Manager",
        "en": "Daniel Baran | IT Project & Product Manager",
        "pl": "Daniel Baran | Projekty IT i Product Ownership",
    },
    "about": {
        "de": "Über Daniel Baran | IT-Projektleitung",
        "en": "About Daniel Baran | IT Delivery",
        "pl": "O Danielu Baranie | IT Delivery",
    },
    "projects": {
        "de": "IT Case Studies | Daniel Baran",
        "en": "IT Project Case Studies | Daniel Baran",
        "pl": "Case studies IT | Daniel Baran",
    },
    "imprint": {
        "de": "Impressum und Kontakt | Daniel Baran",
        "en": "Legal Notice and Contact | Daniel Baran",
        "pl": "Nota prawna i kontakt | Daniel Baran",
    },
    "privacy": {
        "de": "Datenschutz und Privacy | Daniel Baran",
        "en": "Privacy Policy and Contact | Daniel Baran",
        "pl": "Prywatność i dane | Daniel Baran",
    },
}

DESCRIPTIONS = {
    "home": {
        "de": "Daniel Baran unterstützt Teams als Senior IT Project & Product Manager bei IT-Projekten, Product Ownership, KI-Enablement und Streaming-Delivery.",
        "en": "Daniel Baran supports teams as a senior IT project and product manager for IT delivery, product ownership, AI enablement and streaming platforms.",
        "pl": "Daniel Baran wspiera zespoły jako Senior IT Project & Product Manager w projektach IT, product ownership, wdrażaniu AI i platformach streamingowych.",
    },
    "about": {
        "de": "Profil von Daniel Baran: Erfahrung in IT-Projektleitung, Product Ownership, KI-Enablement, Streaming-Infrastruktur und Arbeit mit Teams in Europa.",
        "en": "Profile of Daniel Baran: experience in IT project delivery, product ownership, AI enablement, streaming infrastructure and European remote teams.",
        "pl": "Profil Daniela Barana: doświadczenie w prowadzeniu projektów IT, product ownership, wdrażaniu AI, infrastrukturze streamingowej i pracy z zespołami.",
    },
    "projects": {
        "de": "Neun Case Studies von Daniel Baran zu KI-Empfehlungen, Streaming-Infrastruktur, Metaverse-Projekten, Fashion-Tech und Automotive-Systemen.",
        "en": "Nine Daniel Baran case studies covering AI recommendations, streaming infrastructure, metaverse projects, fashion tech and automotive systems.",
        "pl": "Dziewięć case studies Daniela Barana o rekomendacjach AI, infrastrukturze streamingu, projektach metaverse, fashion tech i systemach automotive.",
    },
    "imprint": {
        "de": "Impressum, Anbieterkennzeichnung und Kontaktinformationen von Daniel Baran für die Website daniel-baran.com und freiberufliche IT-Dienstleistungen.",
        "en": "Legal notice, provider details and contact information for Daniel Baran, daniel-baran.com and freelance IT project services.",
        "pl": "Nota prawna, dane identyfikacyjne i informacje kontaktowe Daniela Barana dla strony daniel-baran.com oraz usług IT freelance.",
    },
    "privacy": {
        "de": "Datenschutzerklärung für daniel-baran.com mit Informationen zu Hosting, Kontaktformular, lokalen Schriftarten, Sprachwahl und Betroffenenrechten.",
        "en": "Privacy policy for daniel-baran.com covering hosting, contact form processing, local fonts, language choice and GDPR rights.",
        "pl": "Polityka prywatności dla daniel-baran.com: hosting, formularz kontaktowy, lokalne czcionki, wybór języka i prawa wynikające z RODO.",
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
        "de": "SWR KI-Empfehlungen | Daniel Baran",
        "en": "SWR AI Recommendations | Daniel Baran",
        "pl": "Rekomendacje AI dla SWR | Daniel Baran",
    },
    "swr-ki-testphase": {
        "de": "SWR KI-Testphase | Daniel Baran",
        "en": "SWR AI Pilot Phase | Daniel Baran",
        "pl": "Faza testów AI w SWR | Daniel Baran",
    },
    "swr-multiplatform-service": {
        "de": "ARD Multiplatform-Service | Daniel Baran",
        "en": "ARD Multiplatform Service | Daniel Baran",
        "pl": "Serwis multiplatformowy ARD | Daniel Baran",
    },
    "swr-ard-transcoding": {
        "de": "ARD Transcoding | Daniel Baran",
        "en": "ARD Transcoding | Daniel Baran",
        "pl": "Transcoding ARD | Daniel Baran",
    },
    "vestium": {
        "de": "Vestium Fashion-Tech | Daniel Baran",
        "en": "Vestium Fashion Tech | Daniel Baran",
        "pl": "Vestium Fashion Tech | Daniel Baran",
    },
    "infinite-playa": {
        "de": "Infinite Playa Metaverse | Daniel Baran",
        "en": "Infinite Playa Metaverse | Daniel Baran",
        "pl": "Infinite Playa Metaverse | Daniel Baran",
    },
    "uci-track-champions-league": {
        "de": "UCI Metaverse Experience | Daniel Baran",
        "en": "UCI Metaverse Experience | Daniel Baran",
        "pl": "UCI Metaverse Experience | Daniel Baran",
    },
    "systemmigration-konzernverbund": {
        "de": "MAN/VW Systemmigration | Daniel Baran",
        "en": "MAN/VW System Migration | Daniel Baran",
        "pl": "Migracja systemu MAN/VW | Daniel Baran",
    },
    "fahrzeugumbauten-dokumentation": {
        "de": "Fahrzeugumbauten-Doku | Daniel Baran",
        "en": "Vehicle Conversion Docs | Daniel Baran",
        "pl": "Dokumentacja przebudów | Daniel Baran",
    },
}

CASE_DESCRIPTIONS = {
    "swr-ki-empfehlungsengine": {
        "de": "Case Study zu einem KI-Empfehlungssystem für die SWR-Website: Product Ownership, redaktionelles Feedback, Modelltraining und produktiver Vergleich mit dem Altsystem.",
        "en": "Case study on an AI recommendation system for the SWR website: product ownership, editorial feedback, model training and production rollout.",
        "pl": "Case study systemu rekomendacji AI dla strony SWR: product ownership, feedback redakcji, trening modelu i porównanie produkcyjne ze starym systemem.",
    },
    "swr-ki-testphase": {
        "de": "Case Study zur KI-Testphase beim SWR: Use-Case-Auswahl, Governance, Team-Befähigung und der Weg von Experimenten zu belastbaren Arbeitsweisen.",
        "en": "Case study on the SWR AI pilot phase: use case selection, governance, team enablement and the path from experiments to reliable operating models.",
        "pl": "Case study fazy testów AI w SWR: wybór use case'ów, governance, wsparcie zespołów i przejście od eksperymentów do stabilnych sposobów pracy.",
    },
    "swr-multiplatform-service": {
        "de": "Case Study zum ARD-Multiplattformservice: Product Ownership für cloud-native Streaming-Infrastruktur, Manifest-Logik und Betrieb in der ARD-Mediathek.",
        "en": "Case study on the ARD multiplatform service: product ownership for cloud-native streaming infrastructure, manifest logic and ARD Mediathek operations.",
        "pl": "Case study serwisu multiplatformowego ARD: product ownership dla cloud-native infrastruktury streamingu, logiki manifestów i działania ARD Mediathek.",
    },
    "swr-ard-transcoding": {
        "de": "Case Study zum zentralen ARD-Transcoding: Projektleitung für VOD- und Live-Workflows, Schnittstellen, Rollout und robuste Medienproduktion.",
        "en": "Case study on central ARD transcoding: project leadership for VOD and live workflows, interfaces, rollout and robust media production.",
        "pl": "Case study centralnego transcodingu ARD: prowadzenie projektu dla workflow VOD i live, interfejsów, rolloutów i stabilnej produkcji mediów.",
    },
    "vestium": {
        "de": "Case Study zum Fashion-Tech-Startup Vestium: 3D-Scan-Avatare, virtuelle Anprobe, Teamaufbau und Produktarbeit zwischen Vision und technischer Machbarkeit.",
        "en": "Case study on the fashion tech startup Vestium: 3D scan avatars, virtual try-on, team building and product work between vision and technical feasibility.",
        "pl": "Case study startupu fashion tech Vestium: awatary ze skanów 3D, wirtualna przymiarka, budowa zespołu i produkt między wizją a wykonalnością.",
    },
    "infinite-playa": {
        "de": "Case Study zu The Infinite Playa: virtuelle Burning-Man-Welt, internationale Delivery, Support-Prozesse und Führung eines interdisziplinären Teams.",
        "en": "Case study on The Infinite Playa: virtual Burning Man world, international delivery, support processes and leadership of an interdisciplinary team.",
        "pl": "Case study The Infinite Playa: wirtualny świat Burning Man, międzynarodowa realizacja, procesy wsparcia i prowadzenie interdyscyplinarnego zespołu.",
    },
    "uci-track-champions-league": {
        "de": "Case Study zum UCI Track Champions League Metaverse: immersive Fanplattform, Event-Delivery und Abstimmung zwischen Studio, Partnern und Sportmarke.",
        "en": "Case study on the UCI Track Champions League metaverse: immersive fan platform, event delivery and alignment between studio, partners and sports brand.",
        "pl": "Case study metaverse UCI Track Champions League: immersyjna platforma fanowska, realizacja eventu i koordynacja studia, partnerów oraz marki sportowej.",
    },
    "systemmigration-konzernverbund": {
        "de": "Case Study zur MAN/VW-Systemmigration: weltweiter After-Sales-Kontext, Schnittstellensteuerung, Support-Aufbau und Migration eines zentralen Werkstatt-Systems.",
        "en": "Case study on MAN/VW system migration: global after-sales context, interface steering, support setup and migration of a central workshop system.",
        "pl": "Case study migracji systemu MAN/VW: globalny kontekst after-sales, koordynacja interfejsów, budowa supportu i migracja centralnego systemu warsztatowego.",
    },
    "fahrzeugumbauten-dokumentation": {
        "de": "Case Study zur Dokumentation von Fahrzeugumbauten: IT-Projektarbeit, strukturierte Service-Informationen und weltweit auffindbares Wissen für Werkstätten.",
        "en": "Case study on vehicle conversion documentation: IT project work, structured service information and globally findable knowledge for workshops.",
        "pl": "Case study dokumentacji przebudów pojazdów: praca projektowa IT, uporządkowane informacje serwisowe i globalnie dostępna wiedza dla warsztatów.",
    },
}

STATIC_PAGE_COPY = {
    "home": {
        "de": {
            "eyebrow": "Kurzprofil",
            "heading": "Was Daniel Baran für IT- und Produktteams leistet",
            "paragraphs": [
                "Daniel Baran ist Senior IT Project & Product Manager für Organisationen, die komplexe digitale Vorhaben zuverlässig in Produktion bringen müssen. Der Schwerpunkt liegt auf IT-Projektmanagement, Product Ownership, KI-Enablement, cloud-nativer Streaming-Infrastruktur und Schnittstellen zwischen Fachbereich, Engineering, Partnern und Management.",
                "Die Arbeit beginnt dort, wo ein Projekt nicht nur technisch, sondern auch organisatorisch anspruchsvoll ist: mehrere Stakeholder, gewachsene Systeme, knappe Fachkapazitäten, Datenschutzanforderungen, externe Dienstleister und ein Zielbild, das in belastbare Arbeitspakete übersetzt werden muss.",
                "Aus Projekten bei SWR, ARD, MAN/Volkswagen, Adastra Studios und dem Fashion-Tech-Startup Vestium bringt Daniel Erfahrung aus Medien, Automotive, Entertainment, Streaming, KI und Startup-Aufbau mit. Die Case Studies zeigen Produktarbeit, Projektleitung, Teamkoordination und technische Delivery in realen Produktionskontexten.",
                "Teams buchen Daniel, wenn sie einen Umsetzer brauchen, der technische Details versteht, Projektstruktur schafft, Entscheidungen vorbereitet und gleichzeitig Menschen mitnimmt. Ziel ist nicht nur ein sauberer Plan, sondern ein Ergebnis, das nutzbar, wartbar und im Alltag tragfähig ist.",
            ],
            "bullets": [
                "IT-Projektmanagement für komplexe System- und Plattformvorhaben",
                "Product Ownership für digitale Produkte, Backlogs und Roadmaps",
                "KI-Enablement von Use-Case-Auswahl bis produktiver Einführung",
                "Streaming-, Cloud- und Transcoding-Projekte im Medienumfeld",
                "Remote-Zusammenarbeit auf Deutsch, Englisch und Polnisch",
            ],
        },
        "en": {
            "eyebrow": "Profile summary",
            "heading": "What Daniel Baran delivers for IT and product teams",
            "paragraphs": [
                "Daniel Baran is a senior IT Project & Product Manager for organizations that need to take complex digital initiatives reliably into production. His focus is IT project management, product ownership, AI enablement, cloud-native streaming infrastructure and the interface between business teams, engineering, partners and management.",
                "The work starts where a project is not only technically demanding but organizationally difficult: multiple stakeholders, legacy systems, limited subject-matter capacity, data protection requirements, external vendors and a target picture that has to become clear work packages.",
                "Through projects with SWR, ARD, MAN/Volkswagen, Adastra Studios and the fashion-tech startup Vestium, Daniel brings experience across media, automotive, entertainment, streaming, AI and startup building. The case studies document product work, project leadership, team coordination and technical delivery in real production environments.",
                "Teams bring Daniel in when they need someone who understands technical detail, creates project structure, prepares decisions and keeps people aligned. The goal is not just a neat plan but an outcome that is usable, maintainable and robust in daily operations.",
            ],
            "bullets": [
                "IT project management for complex system and platform initiatives",
                "Product ownership for digital products, backlogs and roadmaps",
                "AI enablement from use-case selection to production adoption",
                "Streaming, cloud and transcoding projects in media environments",
                "Remote collaboration in German, English and Polish",
            ],
        },
        "pl": {
            "eyebrow": "Krótki profil",
            "heading": "Jak Daniel Baran wspiera zespoły IT i produktowe",
            "paragraphs": [
                "Daniel Baran jest Senior IT Project & Product Managerem dla organizacji, które muszą niezawodnie doprowadzać złożone inicjatywy cyfrowe do produkcji. Główne obszary to zarządzanie projektami IT, product ownership, wdrażanie AI, cloud-native infrastruktura streamingu oraz praca na styku biznesu, engineeringu, partnerów i managementu.",
                "Praca zaczyna się tam, gdzie projekt jest wymagający nie tylko technicznie, lecz także organizacyjnie: wielu interesariuszy, starsze systemy, ograniczony czas ekspertów, wymagania ochrony danych, zewnętrzni dostawcy i cel, który trzeba przełożyć na konkretne pakiety pracy.",
                "Dzięki projektom dla SWR, ARD, MAN/Volkswagen, Adastra Studios oraz startupu fashion-tech Vestium Daniel wnosi doświadczenie z mediów, automotive, entertainment, streamingu, AI i budowy startupu. Case studies pokazują product work, prowadzenie projektów, koordynację zespołów i techniczną realizację w realnych środowiskach produkcyjnych.",
                "Zespoły angażują Daniela, gdy potrzebują osoby, która rozumie szczegóły techniczne, porządkuje projekt, przygotowuje decyzje i utrzymuje alignment między ludźmi. Celem nie jest tylko dobry plan, lecz rezultat, który działa, da się utrzymać i sprawdza się w codziennej pracy.",
            ],
            "bullets": [
                "Zarządzanie projektami IT dla złożonych systemów i platform",
                "Product ownership dla produktów cyfrowych, backlogów i roadmap",
                "Wdrażanie AI od wyboru use case'ów po produkcyjne użycie",
                "Projekty streamingowe, cloud i transcoding w środowisku mediów",
                "Współpraca zdalna po niemiecku, angielsku i polsku",
            ],
        },
    },
    "about": {
        "de": {
            "eyebrow": "Erfahrung und Arbeitsweise",
            "heading": "Zwischen Technik, Produkt und Organisation",
            "paragraphs": [
                "Daniel Baran arbeitet an der Schnittstelle von Projektleitung, Product Ownership und technischer Delivery. Seine Rolle ist besonders wirksam, wenn ein Vorhaben mehrere Systeme, Teams und Interessen verbindet und trotzdem einen klaren Weg in Richtung Produktion braucht.",
                "Seine Erfahrung reicht von öffentlich-rechtlicher Medieninfrastruktur über KI-Empfehlungssysteme und Transcoding-Workflows bis zu Metaverse-Events, Fashion-Tech und Automotive-Systemmigration. Diese Breite hilft, technische Anforderungen, Business-Ziele und operative Realität zusammenzubringen.",
                "Methodisch verbindet er strukturierte Projektarbeit mit pragmatischer Produktverantwortung: klare Entscheidungsgrundlagen, nachvollziehbare Backlogs, belastbare Roadmaps, transparente Kommunikation und genug technisches Verständnis, um Risiken früh zu erkennen.",
            ],
            "bullets": [
                "Certified Product Management Expert (XDi)",
                "Generative AI & GPAI Weiterbildung bei Bitkom",
                "AI for Business über Wharton Online",
                "Google Project Management über Coursera",
                "Deutsch, Englisch und Polnisch in Projekten einsetzbar",
            ],
        },
        "en": {
            "eyebrow": "Experience and working style",
            "heading": "Between technology, product and organization",
            "paragraphs": [
                "Daniel Baran works at the intersection of project leadership, product ownership and technical delivery. His role is strongest when an initiative connects several systems, teams and interests but still needs a clear path toward production.",
                "His experience ranges from public broadcasting infrastructure, AI recommendation systems and transcoding workflows to metaverse events, fashion tech and automotive system migration. This range helps connect technical requirements, business goals and operational reality.",
                "His working style combines structured project management with pragmatic product responsibility: clear decision material, transparent backlogs, reliable roadmaps, direct communication and enough technical understanding to identify risks early.",
            ],
            "bullets": [
                "Certified Product Management Expert (XDi)",
                "Generative AI & GPAI training with Bitkom",
                "AI for Business through Wharton Online",
                "Google Project Management through Coursera",
                "German, English and Polish available in project work",
            ],
        },
        "pl": {
            "eyebrow": "Doświadczenie i sposób pracy",
            "heading": "Między technologią, produktem i organizacją",
            "paragraphs": [
                "Daniel Baran pracuje na styku prowadzenia projektów, product ownership i technicznej realizacji. Jego rola jest szczególnie skuteczna wtedy, gdy inicjatywa łączy kilka systemów, zespołów i interesów, ale nadal potrzebuje jasnej drogi do produkcji.",
                "Doświadczenie obejmuje infrastrukturę mediów publicznych, systemy rekomendacji AI, workflow transcodingu, eventy metaverse, fashion tech oraz migracje systemów automotive. Ta szerokość pomaga łączyć wymagania techniczne, cele biznesowe i realia operacyjne.",
                "Sposób pracy łączy uporządkowane zarządzanie projektem z pragmatyczną odpowiedzialnością produktową: jasne materiały decyzyjne, przejrzyste backlogi, realistyczne roadmapy, bezpośrednia komunikacja i techniczne zrozumienie ryzyk.",
            ],
            "bullets": [
                "Certified Product Management Expert (XDi)",
                "Szkolenie Generative AI & GPAI w Bitkom",
                "AI for Business przez Wharton Online",
                "Google Project Management przez Coursera",
                "Niemiecki, angielski i polski w pracy projektowej",
            ],
        },
    },
    "projects": {
        "de": {
            "eyebrow": "Case-Study-Übersicht",
            "heading": "Nachweise aus Medien, KI, Streaming, Startup und Automotive",
            "paragraphs": [
                "Die Projekte zeigen, wie Daniel Baran Produkt- und Projektverantwortung in unterschiedlichen Umfeldern übernommen hat: öffentlich-rechtliche Medien, cloud-native Streaming-Services, KI-Empfehlungen, virtuelle Events, Fashion-Tech und globale Automotive-Prozesse.",
                "Jede Case Study beschreibt einen konkreten Kontext, die eigene Rolle, zentrale Entscheidungen und das Ergebnis. Entscheidend ist dabei nicht nur die Technologie, sondern auch die Übersetzung zwischen Stakeholdern, Teams, Systemen und operativem Betrieb.",
                "Die Auswahl ist bewusst breit: Sie zeigt, dass Delivery nicht an einer Branche hängt, sondern an sauberer Kommunikation, technischer Anschlussfähigkeit, klaren Prioritäten und einem realistischen Verständnis von Organisationen.",
            ],
            "bullets": [],
        },
        "en": {
            "eyebrow": "Case study overview",
            "heading": "Proof across media, AI, streaming, startup and automotive",
            "paragraphs": [
                "The projects show how Daniel Baran has taken product and project responsibility in different environments: public broadcasting, cloud-native streaming services, AI recommendations, virtual events, fashion tech and global automotive processes.",
                "Each case study describes a concrete context, Daniel's role, key decisions and the outcome. The important part is not only the technology but the translation between stakeholders, teams, systems and operational reality.",
                "The selection is intentionally broad. It shows that delivery is not tied to one industry but to clear communication, technical fluency, realistic prioritization and an understanding of how organizations actually work.",
            ],
            "bullets": [],
        },
        "pl": {
            "eyebrow": "Przegląd case studies",
            "heading": "Dowody pracy w mediach, AI, streamingu, startupie i automotive",
            "paragraphs": [
                "Projekty pokazują, jak Daniel Baran przejmował odpowiedzialność produktową i projektową w różnych środowiskach: media publiczne, cloud-native usługi streamingowe, rekomendacje AI, eventy wirtualne, fashion tech i globalne procesy automotive.",
                "Każde case study opisuje konkretny kontekst, rolę Daniela, kluczowe decyzje i rezultat. Ważna jest nie tylko technologia, lecz także tłumaczenie między interesariuszami, zespołami, systemami i codzienną operacją.",
                "Wybór jest celowo szeroki. Pokazuje, że delivery nie zależy od jednej branży, lecz od jasnej komunikacji, technicznego zrozumienia, realistycznych priorytetów i wiedzy o tym, jak działają organizacje.",
            ],
            "bullets": [],
        },
    },
}

CASE_STATIC_BULLETS = {
    "swr-ki-empfehlungsengine": {
        "de": ["Product Ownership für ein KI-Empfehlungssystem", "Feedback-Prozess für ausgelastete Redaktionen", "Produktiver Vergleich mit dem bisherigen System"],
        "en": ["Product ownership for an AI recommendation system", "Feedback process for busy editorial teams", "Production comparison with the previous system"],
        "pl": ["Product ownership systemu rekomendacji AI", "Proces feedbacku dla obciążonych redakcji", "Porównanie produkcyjne z poprzednim systemem"],
    },
    "swr-ki-testphase": {
        "de": ["Bewertung realer KI-Anwendungsfälle", "Governance für Datenschutz und Modellwahl", "Befähigung von Teams statt isolierter Experimente"],
        "en": ["Evaluation of real AI use cases", "Governance for privacy and model selection", "Team enablement instead of isolated experiments"],
        "pl": ["Ocena realnych zastosowań AI", "Governance dla ochrony danych i wyboru modeli", "Wspieranie zespołów zamiast izolowanych eksperymentów"],
    },
    "swr-multiplatform-service": {
        "de": ["Cloud-native Streaming-Infrastruktur", "Manifest-Logik für HLS/DASH-Workflows", "Betrieb im Umfeld der ARD-Mediathek"],
        "en": ["Cloud-native streaming infrastructure", "Manifest logic for HLS/DASH workflows", "Operations in the ARD Mediathek environment"],
        "pl": ["Cloud-native infrastruktura streamingowa", "Logika manifestów dla workflow HLS/DASH", "Działanie w środowisku ARD Mediathek"],
    },
    "swr-ard-transcoding": {
        "de": ["Zentrale Workflows für VOD und Live", "Koordination technischer Schnittstellen", "Projektleitung für robuste Medienproduktion"],
        "en": ["Central workflows for VOD and live", "Coordination of technical interfaces", "Project leadership for robust media production"],
        "pl": ["Centralne workflow dla VOD i live", "Koordynacja interfejsów technicznych", "Prowadzenie projektu stabilnej produkcji mediów"],
    },
    "vestium": {
        "de": ["3D-Scan-Avatare für virtuelle Anprobe", "Teamaufbau für Rendering und Visualisierung", "Produktarbeit zwischen Vision und Machbarkeit"],
        "en": ["3D scan avatars for virtual try-on", "Team setup for rendering and visualization", "Product work between vision and feasibility"],
        "pl": ["Awatary ze skanów 3D do wirtualnej przymiarki", "Budowa zespołu renderingu i wizualizacji", "Produkt między wizją i wykonalnością"],
    },
    "infinite-playa": {
        "de": ["Virtuelle Burning-Man-Welt", "Internationale Delivery mit interdisziplinärem Team", "Support-Prozesse für ein neues Eventformat"],
        "en": ["Virtual Burning Man world", "International delivery with an interdisciplinary team", "Support processes for a new event format"],
        "pl": ["Wirtualny świat Burning Man", "Międzynarodowa realizacja z interdyscyplinarnym zespołem", "Procesy wsparcia dla nowego formatu eventu"],
    },
    "uci-track-champions-league": {
        "de": ["Immersive Fanplattform für ein Sportevent", "Abstimmung zwischen Studio, Partnern und Marke", "Event-Delivery mit sichtbarem Nutzererlebnis"],
        "en": ["Immersive fan platform for a sports event", "Alignment between studio, partners and brand", "Event delivery with a visible user experience"],
        "pl": ["Immersyjna platforma fanowska dla eventu sportowego", "Koordynacja studia, partnerów i marki", "Realizacja eventu z widocznym doświadczeniem użytkownika"],
    },
    "systemmigration-konzernverbund": {
        "de": ["Migration eines zentralen Werkstatt-Systems", "Schnittstellensteuerung zwischen MAN und Volkswagen", "Aufbau einer globalen Support-Funktion"],
        "en": ["Migration of a central workshop system", "Interface steering between MAN and Volkswagen", "Setup of a global support function"],
        "pl": ["Migracja centralnego systemu warsztatowego", "Koordynacja interfejsów między MAN i Volkswagenem", "Budowa globalnej funkcji supportu"],
    },
    "fahrzeugumbauten-dokumentation": {
        "de": ["Strukturierte Dokumentation für Fahrzeugumbauten", "Auffindbares Service-Wissen für Werkstätten", "IT-Projektarbeit im Automotive-Umfeld"],
        "en": ["Structured documentation for vehicle conversions", "Findable service knowledge for workshops", "IT project work in an automotive environment"],
        "pl": ["Uporządkowana dokumentacja przebudów pojazdów", "Dostępna wiedza serwisowa dla warsztatów", "Praca projektowa IT w środowisku automotive"],
    },
}

STATIC_EXTRA_PARAGRAPHS = {
    "home": {
        "de": [
            "Typische Einsätze sind Übergaben zwischen Strategie und Umsetzung, festgefahrene Backlogs, unklare technische Abhängigkeiten, Tool- oder Systemmigrationen, KI-Initiativen nach der ersten Experimentierphase und Plattformprojekte, die mehrere Teams gleichzeitig betreffen. In solchen Situationen braucht es jemanden, der Struktur schafft, ohne die technische Realität zu vereinfachen.",
            "Die Zusammenarbeit ist auf klare Verantwortung ausgelegt: Ziele schärfen, Risiken sichtbar machen, Stakeholder synchronisieren, Lieferobjekte definieren und die nächsten Entscheidungen vorbereiten. Dadurch entsteht ein Arbeitsmodus, der sowohl für Fachbereiche als auch für Engineering-Teams nachvollziehbar bleibt.",
            "Besonders relevant ist diese Rolle, wenn bestehende Teams bereits viel Wissen haben, aber zu wenig Zeit, um daraus ein tragfähiges Vorgehen zu formen. Daniel verdichtet Informationen, trennt Annahmen von gesicherten Fakten und sorgt dafür, dass Entscheidungen dokumentiert, anschlussfähig und später überprüfbar bleiben.",
            "Der Fokus liegt dabei nicht auf mehr Prozess um des Prozesses willen. Entscheidend ist, dass Planung, Produktlogik und technische Umsetzung in eine Form kommen, die im Alltag nutzbar ist: mit klaren Verantwortlichkeiten, transparenten Abhängigkeiten, belastbaren Prioritäten und einem gemeinsamen Verständnis für das gewünschte Ergebnis.",
            "So wird die Website auch für Suchsysteme klarer: Sie benennt konkrete Einsatzfelder, Rollen, Branchen und Ergebnisse statt nur allgemein Projektmanagement zu behaupten.",
        ],
        "en": [
            "Typical engagements include handovers between strategy and implementation, stuck backlogs, unclear technical dependencies, tool or system migrations, AI initiatives after the first experiment phase and platform projects that affect several teams at once. In these situations, the work needs structure without oversimplifying the technical reality.",
            "The collaboration is built around clear ownership: sharpening goals, making risks visible, synchronizing stakeholders, defining deliverables and preparing the next decisions. That creates a working mode that remains understandable for both business teams and engineering teams.",
            "This role is especially useful when existing teams already hold a lot of knowledge but lack the time to turn it into a reliable delivery path. Daniel condenses information, separates assumptions from confirmed facts and keeps decisions documented, connected and reviewable later.",
            "The focus is not more process for its own sake. What matters is turning planning, product logic and technical implementation into a working format: clear responsibilities, transparent dependencies, reliable priorities and a shared understanding of the outcome the team is trying to reach.",
            "That also makes the website clearer for search systems: it names concrete engagement types, roles, industries and outcomes instead of making only generic project management claims.",
        ],
        "pl": [
            "Typowe zadania to przejścia między strategią a realizacją, zablokowane backlogi, niejasne zależności techniczne, migracje narzędzi lub systemów, inicjatywy AI po pierwszej fazie eksperymentów oraz projekty platformowe obejmujące kilka zespołów jednocześnie. W takich sytuacjach potrzebna jest struktura bez upraszczania rzeczywistości technicznej.",
            "Współpraca opiera się na jasnej odpowiedzialności: doprecyzowaniu celów, uwidocznieniu ryzyk, synchronizacji interesariuszy, zdefiniowaniu rezultatów i przygotowaniu kolejnych decyzji. Dzięki temu sposób pracy pozostaje zrozumiały zarówno dla biznesu, jak i zespołów engineeringowych.",
            "Ta rola jest szczególnie przydatna, gdy zespoły mają już dużo wiedzy, ale brakuje im czasu, aby przełożyć ją na stabilną ścieżkę delivery. Daniel kondensuje informacje, oddziela założenia od faktów i dba o to, aby decyzje były udokumentowane, połączone z kontekstem i możliwe do późniejszej weryfikacji.",
            "Nie chodzi przy tym o proces dla samego procesu. Najważniejsze jest przełożenie planowania, logiki produktu i implementacji technicznej na format pracy: jasne odpowiedzialności, widoczne zależności, wiarygodne priorytety i wspólne rozumienie rezultatu, do którego dąży zespół.",
            "Dzięki temu strona jest czytelniejsza także dla systemów wyszukiwania: pokazuje konkretne typy zadań, role, branże i rezultaty zamiast ogólnych deklaracji o project management.",
        ],
    },
    "about": {
        "de": [
            "In der Praxis bedeutet das: Anforderungen so formulieren, dass Teams sie bauen können; technische Diskussionen so strukturieren, dass Fachbereiche entscheiden können; und Risiken so früh adressieren, dass sie nicht erst im Rollout sichtbar werden. Diese Übersetzungsarbeit ist oft der Unterschied zwischen einem Projekt, das gut klingt, und einem Projekt, das tatsächlich funktioniert.",
            "Daniel arbeitet nicht als reine Koordinationsschicht. Er geht tief genug in Architektur, Datenflüsse, Betriebsfragen und Nutzerbedürfnisse, um technische Abhängigkeiten realistisch einzuschätzen. Gleichzeitig bleibt der Blick auf Budget, Timing, Verantwortlichkeiten und Kommunikationswege erhalten.",
            "Seine Stärke liegt besonders in Umfeldern, in denen mehrere Organisationen oder Abteilungen beteiligt sind. Dort braucht Delivery mehr als Statusmeetings: klare Entscheidungswege, belastbare Dokumentation, priorisierte Arbeitspakete und eine Sprache, die technische und nichttechnische Beteiligte verbindet.",
            "Das Ergebnis dieser Arbeitsweise ist ein Projektmodus, in dem Teams schneller wissen, was als Nächstes zählt. Offene Punkte werden nicht versteckt, sondern priorisiert; Entscheidungen werden vorbereitet statt vertagt; und Fortschritt wird an nutzbaren Ergebnissen gemessen.",
            "Die Erfahrung reicht von öffentlich-rechtlichen Medienplattformen über KI-gestützte Workflows bis zu Automotive-Systemen und digitalen Produktteams. Diese Breite hilft dabei, Muster früh zu erkennen: wo Governance fehlt, wo Produktentscheidungen unklar sind und wo technische Risiken vor dem nächsten Meilenstein sauber geklärt werden müssen.",
            "Für Auftraggeber zählt vor allem diese Kombination: operative Umsetzungskraft, saubere Kommunikation und genug technisches Verständnis, um schwierige Abwägungen nicht nur zu moderieren, sondern entscheidungsreif zu machen.",
        ],
        "en": [
            "In practice, that means framing requirements so teams can build them, structuring technical discussions so business stakeholders can decide, and addressing risks early enough that they do not first appear during rollout. This translation work is often the difference between a project that sounds good and a project that actually works.",
            "Daniel does not work as a pure coordination layer. He goes deep enough into architecture, data flows, operations and user needs to judge technical dependencies realistically. At the same time, budget, timing, ownership and communication paths stay visible.",
            "His strength is especially relevant in environments where several organizations or departments are involved. Delivery then needs more than status meetings: clear decision paths, reliable documentation, prioritized work packages and a language that connects technical and non-technical participants.",
            "The result is a project mode in which teams understand faster what matters next. Open points are not hidden but prioritized, decisions are prepared instead of postponed, and progress is measured against usable outcomes.",
            "The experience spans public media platforms, AI-supported workflows, automotive systems and digital product teams. That range helps identify patterns early: where governance is missing, where product decisions are unclear and where technical risks need to be resolved before the next milestone.",
            "For clients, the useful part is this combination: operational delivery strength, clear communication and enough technical understanding to turn difficult trade-offs into decisions.",
        ],
        "pl": [
            "W praktyce oznacza to formułowanie wymagań tak, aby zespoły mogły je zbudować, porządkowanie dyskusji technicznych tak, aby biznes mógł podejmować decyzje, oraz adresowanie ryzyk zanim ujawnią się dopiero przy rolloutcie. Ta praca translatorska często decyduje, czy projekt tylko dobrze brzmi, czy rzeczywiście działa.",
            "Daniel nie działa wyłącznie jako warstwa koordynacyjna. Wchodzi wystarczająco głęboko w architekturę, przepływy danych, operacje i potrzeby użytkowników, aby realistycznie ocenić zależności techniczne. Jednocześnie pozostają widoczne budżet, timing, odpowiedzialności i komunikacja.",
            "Jego mocną stroną są szczególnie środowiska z udziałem kilku organizacji lub działów. Delivery wymaga wtedy czegoś więcej niż status meetingów: jasnych ścieżek decyzyjnych, rzetelnej dokumentacji, priorytetowych pakietów pracy i języka łączącego osoby techniczne oraz nietechniczne.",
            "Efektem jest tryb projektu, w którym zespoły szybciej rozumieją, co jest następne i najważniejsze. Otwarte tematy nie są ukrywane, lecz priorytetyzowane; decyzje są przygotowywane zamiast odkładane; a postęp mierzy się użytecznymi rezultatami.",
            "Doświadczenie obejmuje publiczne platformy medialne, workflow wspierane przez AI, systemy automotive oraz zespoły produktów cyfrowych. Ta szerokość pomaga wcześnie rozpoznawać wzorce: gdzie brakuje governance, gdzie decyzje produktowe są niejasne i gdzie ryzyka techniczne trzeba rozwiązać przed kolejnym milestone.",
            "Dla klientów praktyczna jest właśnie ta kombinacja: operacyjna siła delivery, jasna komunikacja i wystarczające zrozumienie techniczne, aby trudne kompromisy doprowadzić do decyzji.",
        ],
    },
    "projects": {
        "de": [
            "Die Case Studies sind so ausgewählt, dass sie unterschiedliche Arten von Komplexität zeigen: Produktentscheidungen in KI-Systemen, Plattform- und Infrastrukturarbeit im Streaming, internationale Event-Delivery, Startup-Aufbau und Migrationen in Konzernstrukturen. Dadurch entsteht ein nachvollziehbares Bild der Arbeitsweise in sehr verschiedenen Rahmenbedingungen.",
            "Für potenzielle Auftraggeber sind die Beispiele vor allem als Entscheidungshilfe gedacht. Sie zeigen, welche Arten von Problemen Daniel bereits bearbeitet hat, welche Rollen er übernommen hat und wo seine Kombination aus Projektleitung, Product Ownership und technischem Verständnis besonders gut passt.",
        ],
        "en": [
            "The case studies are selected to show different kinds of complexity: product decisions in AI systems, platform and infrastructure work in streaming, international event delivery, startup building and migrations in corporate structures. Together they create a concrete picture of how Daniel works under very different conditions.",
            "For potential clients, the examples are meant as decision support. They show what kinds of problems Daniel has already worked on, which roles he has taken and where his combination of project leadership, product ownership and technical understanding fits especially well.",
        ],
        "pl": [
            "Case studies dobrano tak, aby pokazać różne rodzaje złożoności: decyzje produktowe w systemach AI, pracę platformową i infrastrukturalną w streamingu, międzynarodową realizację eventów, budowę startupu oraz migracje w strukturach korporacyjnych. Razem tworzą konkretny obraz pracy w różnych warunkach.",
            "Dla potencjalnych klientów przykłady są wsparciem decyzyjnym. Pokazują, z jakimi problemami Daniel już pracował, jakie role przejmował i gdzie szczególnie dobrze pasuje połączenie project leadership, product ownership oraz technicznego zrozumienia.",
        ],
    },
    "case": {
        "de": [
            "Die Case Study ist bewusst als Arbeitsnachweis formuliert. Sie beschreibt nicht nur ein Endergebnis, sondern auch die Art der Komplexität: beteiligte Systeme, Abstimmungsbedarf, Entscheidungsdruck und die Übersetzung zwischen produktfachlichen und technischen Anforderungen.",
            "Für ähnliche Projekte ist vor allem relevant, welche Rolle Daniel übernommen hat: Struktur schaffen, Stakeholder synchronisieren, technische Optionen verständlich machen, Prioritäten klären und den Weg in Richtung produktiver Nutzung absichern.",
            "Der praktische Wert liegt in der Verbindung aus Projektführung und Produktverständnis. Dadurch werden Anforderungen nicht nur gesammelt, sondern bewertet, in sinnvolle Sequenzen gebracht und so kommuniziert, dass Teams handlungsfähig bleiben.",
            "Die beschriebenen Beispiele zeigen außerdem, wie wichtig belastbare Übergaben sind: Entscheidungen, Annahmen, Risiken und nächste Schritte müssen so dokumentiert werden, dass sie auch außerhalb einzelner Meetings nachvollziehbar bleiben und neue Beteiligte schnell anschließen können.",
        ],
        "en": [
            "The case study is written as evidence of work, not only as a final result. It describes the kind of complexity involved: systems, alignment needs, decision pressure and the translation between product-facing and technical requirements.",
            "For similar projects, the relevant part is the role Daniel took: creating structure, synchronizing stakeholders, making technical options understandable, clarifying priorities and securing the path toward production use.",
            "The practical value lies in combining project leadership with product understanding. Requirements are not only collected but evaluated, sequenced and communicated in a way that keeps teams able to act.",
            "The examples also show why reliable handovers matter: decisions, assumptions, risks and next steps need to be documented so they remain understandable outside individual meetings and new contributors can join the work quickly.",
        ],
        "pl": [
            "Case study jest opisane jako dowód pracy, nie tylko jako rezultat końcowy. Pokazuje rodzaj złożoności: systemy, potrzebę uzgodnień, presję decyzyjną oraz tłumaczenie między wymaganiami produktowymi i technicznymi.",
            "Dla podobnych projektów najważniejsza jest rola Daniela: tworzenie struktury, synchronizacja interesariuszy, wyjaśnianie opcji technicznych, porządkowanie priorytetów i zabezpieczanie drogi do użycia produkcyjnego.",
            "Praktyczna wartość polega na połączeniu prowadzenia projektu ze zrozumieniem produktu. Wymagania są nie tylko zbierane, lecz oceniane, układane w sensowną kolejność i komunikowane tak, aby zespoły mogły działać.",
            "Przykłady pokazują także, dlaczego ważne są stabilne przekazania: decyzje, założenia, ryzyka i kolejne kroki muszą być udokumentowane tak, aby były zrozumiałe poza pojedynczymi spotkaniami i aby nowe osoby mogły szybko wejść w pracę.",
        ],
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
                ("2. Allgemeines", "Diese Website ist ein rein informatives Angebot. Es werden keine Tracking- oder Analyse-Dienste eingesetzt, keine Cookies gesetzt und keine personenbezogenen Daten zu Werbezwecken verarbeitet. Schriftarten werden lokal von dieser Website geladen; es findet keine Verbindung zu Google Fonts oder ähnlichen Diensten statt."),
                ("3. Hosting (Cloudflare)", 'Diese Website wird bei Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA, gehostet. Beim Aufruf der Website verarbeitet Cloudflare technisch notwendige Daten wie IP-Adresse, Datum und Uhrzeit des Zugriffs, aufgerufene Seite, Browsertyp und Betriebssystem (Server-Logfiles). Diese Verarbeitung ist für den sicheren und stabilen Betrieb der Website erforderlich (Art. 6 Abs. 1 lit. f DSGVO – berechtigtes Interesse). Cloudflare ist unter dem EU-U.S. Data Privacy Framework zertifiziert; zudem bestehen Standardvertragsklauseln. Weitere Informationen: <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">https://www.cloudflare.com/privacypolicy/</a>'),
                ("4. Lokale Speicherung (Sprachwahl)", "Die Website stellt feste Sprachversionen unter /, /pl/ und /en/ bereit. Beim Aufruf der Startseite kann der Browser-Header Accept-Language technisch ausgewertet werden, um Besucher einmalig auf die passende Sprachversion zu leiten. Zusätzlich kann die gewählte Sprache lokal im Browser gespeichert werden, wenn Sie den Sprachumschalter nutzen. Diese Speicherung dient nur der Navigation auf dieser Website."),
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
                ("2. General information", "This website is purely informational. No tracking or analytics services are used, no cookies are set, and no personal data is processed for advertising purposes. Fonts are loaded locally from this website; no connection is made to Google Fonts or similar services."),
                ("3. Hosting (Cloudflare)", 'This website is hosted by Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA. When the website is accessed, Cloudflare processes technically necessary data such as IP address, date and time of access, page requested, browser type and operating system (server log files). This processing is necessary for the secure and stable operation of the website (Art. 6(1)(f) GDPR – legitimate interest). Cloudflare is certified under the EU-U.S. Data Privacy Framework; standard contractual clauses are also in place. Further information: <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">https://www.cloudflare.com/privacypolicy/</a>'),
                ("4. Local storage (language choice)", "The website provides fixed language versions at /, /pl/ and /en/. When the homepage is accessed, the browser header Accept-Language may be technically evaluated once to direct visitors to the appropriate language version. In addition, the selected language may be stored locally in your browser when you use the language switcher. This storage is used only for navigation on this website."),
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
                ("2. Informacje ogólne", "Ta strona internetowa ma wyłącznie charakter informacyjny. Nie są wykorzystywane żadne usługi śledzenia ani analityki, nie są ustawiane pliki cookie i żadne dane osobowe nie są przetwarzane do celów reklamowych. Czcionki są ładowane lokalnie z tej strony; nie następuje połączenie z Google Fonts ani podobnymi usługami."),
                ("3. Hosting (Cloudflare)", 'Ta strona jest hostowana przez Cloudflare, Inc., 101 Townsend St, San Francisco, CA 94107, USA. Podczas korzystania ze strony Cloudflare przetwarza technicznie niezbędne dane, takie jak adres IP, data i godzina dostępu, wywołana strona, typ przeglądarki i system operacyjny. Przetwarzanie to jest niezbędne do bezpiecznego i stabilnego działania strony (art. 6 ust. 1 lit. f RODO – prawnie uzasadniony interes). Cloudflare posiada certyfikację w ramach EU-U.S. Data Privacy Framework; stosowane są również standardowe klauzule umowne. Więcej informacji: <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">https://www.cloudflare.com/privacypolicy/</a>'),
                ("4. Lokalne przechowywanie (wybór języka)", "Strona udostępnia stałe wersje językowe pod adresami /, /pl/ i /en/. Przy wejściu na stronę główną nagłówek przeglądarki Accept-Language może zostać technicznie oceniony jednorazowo, aby skierować odwiedzających do odpowiedniej wersji językowej. Dodatkowo wybrany język może zostać zapisany lokalnie w przeglądarce po użyciu przełącznika języka. Zapis ten służy wyłącznie nawigacji po tej stronie."),
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
    .case-root { overflow-x:hidden; }
    .case-track { min-height:100svh; }
    .case-sticky { min-height:100svh; display:grid; grid-template-columns:minmax(260px,30vw) minmax(0,1fr); gap:clamp(24px,4vw,64px); align-items:stretch; padding:clamp(96px,13vh,132px) clamp(20px,3vw,48px) clamp(36px,5vh,64px); box-sizing:border-box; }
    .case-aside { min-width:0; align-self:start; position:sticky; top:clamp(88px,13vh,120px); }
    .slides-col { position:relative; min-width:0; overflow:hidden; }
    .panels { display:flex; gap:6vw; min-width:0; will-change:transform; transition:transform 0.08s linear; }
    .panel-wrap { flex:0 0 min(72vw,980px); min-width:0; min-height:min(68vh,720px); display:flex; }
    .panel { width:100%; min-width:0; box-sizing:border-box; overflow:hidden; }
    .seo-static-grid { display:grid; grid-template-columns:minmax(160px,220px) minmax(0,860px); gap:clamp(24px,5vw,76px); align-items:start; }
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
      .case-root .site-header { grid-template-columns:minmax(0,1fr) auto !important; padding:12px 16px !important; gap:12px !important; }
      .case-root .site-header > span:first-child { display:none !important; }
      .case-root .site-header > span:nth-child(2) { font-size:0.78rem !important; letter-spacing:0.03em !important; overflow:hidden !important; text-overflow:ellipsis !important; }
      .case-root .site-header nav { justify-content:flex-end !important; gap:10px !important; min-width:0 !important; }
      .case-root .site-header nav > a { display:none !important; }
      .case-root .site-header nav span { gap:8px !important; }
      .case-root .site-header nav button { min-width:30px !important; min-height:30px !important; padding:0 !important; }
      .case-root .mobile-nav { display:none !important; }
      .case-sticky { display:block !important; min-height:0 !important; padding:86px 0 0 !important; }
      .case-aside { position:relative !important; top:auto !important; padding:0 20px 28px !important; box-sizing:border-box; }
      .case-aside h1 { max-width:100% !important; font-size:clamp(1.8rem,8.2vw,2.35rem) !important; line-height:0.96 !important; overflow-wrap:anywhere !important; word-break:normal !important; hyphens:auto !important; }
      .case-aside p, .case-aside dd { max-width:100% !important; overflow-wrap:anywhere !important; word-break:normal !important; }
      .case-aside dl > div { grid-template-columns:minmax(96px,34%) minmax(0,1fr) !important; gap:14px !important; }
      .slides-col { overflow:visible !important; }
      .panels { display:grid !important; grid-template-columns:1fr !important; gap:0 !important; transform:none !important; transition:none !important; }
      .panel-wrap { display:block !important; flex:none !important; width:100% !important; min-height:0 !important; opacity:1 !important; transform:none !important; }
      .panel { min-height:0 !important; border-left:0 !important; border-right:0 !important; padding:28px 20px !important; overflow:visible !important; }
      .panel h2, .panel p, .panel span, .panel dd { max-width:100% !important; overflow-wrap:anywhere !important; word-break:normal !important; }
      .panel h2 { font-size:clamp(1.55rem,7vw,2.2rem) !important; line-height:0.98 !important; }
      .panel [style*="grid-template-columns:minmax(0,1fr) minmax(0,1fr)"], .panel [style*="grid-template-columns:minmax(0,3fr) minmax(0,2fr)"] { grid-template-columns:1fr !important; gap:22px !important; }
      .panel [style*="gap:clamp(14px,1.8vw,24px)"], .panel [style*="gap: clamp(14px, 1.8vw, 24px)"] { flex-direction:column !important; }
      .panel [style*="align-items:flex-start"], .panel [style*="align-items: flex-start"] { display:grid !important; grid-template-columns:1fr !important; gap:18px !important; }
      .panel [style*="align-items:flex-start"] > span[aria-hidden="true"], .panel [style*="align-items: flex-start"] > span[aria-hidden="true"] { display:none !important; }
      .case-hud { display:none !important; }
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
      .seo-static-grid { grid-template-columns:1fr !important; gap:18px !important; }
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


def breadcrumb_items(kind: str, lang: str, slug: str | None = None) -> list[tuple[str, str]]:
    labels = {
        "de": {"home": "Startseite", "about": "Über mich", "projects": "Projekte", "imprint": "Impressum", "privacy": "Datenschutz"},
        "en": {"home": "Home", "about": "About", "projects": "Projects", "imprint": "Legal Notice", "privacy": "Privacy"},
        "pl": {"home": "Strona główna", "about": "O mnie", "projects": "Projekty", "imprint": "Nota prawna", "privacy": "Prywatność"},
    }[lang]
    items = [(labels["home"], SITE + route("home", lang))]
    if kind == "home":
        return items
    if kind == "case":
        items.append((labels["projects"], SITE + route("projects", lang)))
        items.append((CASE_SEO_TITLES[slug][lang].split(" | ")[0], SITE + route("case", lang, slug)))
        return items
    items.append((labels[kind], SITE + route(kind, lang)))
    return items


def breadcrumb_schema(kind: str, lang: str, slug: str | None = None) -> dict[str, object] | None:
    items = breadcrumb_items(kind, lang, slug)
    if len(items) < 2:
        return None
    return {
        "@type": "BreadcrumbList",
        "@id": f"{SITE}{route(kind, lang, slug)}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": name,
                "item": url,
            }
            for idx, (name, url) in enumerate(items)
        ],
    }


def page_schema_type(kind: str) -> str | list[str]:
    if kind in {"home", "about"}:
        return ["ProfilePage", "WebPage"]
    if kind == "projects":
        return ["CollectionPage", "WebPage"]
    return "WebPage"


def structured_data(kind: str, lang: str, slug: str | None = None) -> str:
    title, desc = metadata(kind, lang, slug)
    url = SITE + route(kind, lang, slug)
    organization = {
        "@type": "Organization",
        "@id": f"{SITE}/#organization",
        "name": "Daniel Baran",
        "url": SITE,
        "logo": f"{SITE}/assets/og-image.png",
        "sameAs": [LINKEDIN],
        "contactPoint": {
            "@type": "ContactPoint",
            "email": "kontakt@daniel-baran.com",
            "contactType": "business inquiries",
            "availableLanguage": ["de", "en", "pl"],
        },
    }
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
        "worksFor": {"@id": f"{SITE}/#organization"},
    }
    graph: list[dict[str, object]] = [organization, person]

    if kind == "home":
        graph.append(
            {
                "@type": "WebSite",
                "@id": f"{SITE}/#website",
                "name": "Daniel Baran",
                "url": SITE + "/",
                "inLanguage": ["de", "en", "pl"],
                "publisher": {"@id": f"{SITE}/#organization"},
            }
        )

    breadcrumb = breadcrumb_schema(kind, lang, slug)
    if breadcrumb:
        graph.append(breadcrumb)

    page: dict[str, object] = {
        "@type": page_schema_type(kind),
        "@id": f"{url}#webpage",
        "name": title,
        "description": desc,
        "url": url,
        "inLanguage": lang,
        "dateModified": LASTMOD,
        "isPartOf": {"@id": f"{SITE}/#website"},
        "about": {"@id": f"{SITE}/#person"},
    }
    if breadcrumb:
        page["breadcrumb"] = {"@id": breadcrumb["@id"]}

    if kind == "case":
        page["mainEntity"] = {"@id": f"{url}#case-study"}
        graph.append(
            {
                "@type": "CreativeWork",
                "@id": f"{url}#case-study",
                "name": title,
                "description": desc,
                "url": url,
                "inLanguage": lang,
                "author": {"@id": f"{SITE}/#person"},
                "publisher": {"@id": f"{SITE}/#organization"},
                "dateModified": LASTMOD,
                "image": f"{SITE}/assets/redesign/{CASE_IMAGE_BY_SLUG[slug]}",
            }
        )
    elif kind == "projects":
        page["mainEntity"] = {
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
        }
    elif kind in {"home", "about"}:
        page["mainEntity"] = {"@id": f"{SITE}/#person"}

    graph.append(page)

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


def seo_static_section(kind: str, lang: str, slug: str | None = None) -> str:
    if kind in {"imprint", "privacy"}:
        return ""
    if kind == "case":
        assert slug
        title = CASE_SEO_TITLES[slug][lang].split(" | ")[0]
        paragraphs = [
            CASE_DESCRIPTIONS[slug][lang],
            {
                "de": "Diese statische Zusammenfassung ergänzt die interaktive Case-Study-Ansicht und macht Kontext, Rolle und Ergebnis auch ohne JavaScript klar lesbar. Sie hilft Suchmaschinen und AI-Crawlern, die wichtigsten Fakten der Seite direkt im HTML zu erfassen.",
                "en": "This static summary complements the interactive case study view and keeps context, role and outcome readable without JavaScript. It helps search engines and AI crawlers understand the most important facts directly in the HTML.",
                "pl": "To statyczne podsumowanie uzupełnia interaktywny widok case study i sprawia, że kontekst, rola oraz rezultat są czytelne również bez JavaScriptu. Pomaga wyszukiwarkom i crawlerom AI odczytać najważniejsze fakty bezpośrednio w HTML.",
            }[lang],
        ] + STATIC_EXTRA_PARAGRAPHS["case"][lang]
        bullets = CASE_STATIC_BULLETS[slug][lang]
        eyebrow = {"de": "Case-Study-Zusammenfassung", "en": "Case study summary", "pl": "Podsumowanie case study"}[lang]
    else:
        copy = STATIC_PAGE_COPY[kind][lang]
        title = copy["heading"]
        paragraphs = copy["paragraphs"] + STATIC_EXTRA_PARAGRAPHS.get(kind, {}).get(lang, [])
        bullets = list(copy["bullets"])
        eyebrow = copy["eyebrow"]
        if kind == "projects":
            bullets = [
                f"{CASE_SEO_TITLES[case_slug][lang].split(' | ')[0]}: {CASE_DESCRIPTIONS[case_slug][lang]}"
                for case_slug in CASE_ORDER
            ]

    paragraph_html = "\n".join(
        f'      <p style="margin:0; font-size:1rem; line-height:1.58; color:#4A4945; max-width:74ch;">{html.escape(text)}</p>'
        for text in paragraphs
    )
    bullets_html = ""
    if bullets:
        bullets_html = "\n".join(
            f'        <li style="margin:0; padding:14px 0; border-top:1px solid rgba(13,13,12,0.18); font-size:0.96rem; line-height:1.45; color:#0D0D0C;">{html.escape(item)}</li>'
            for item in bullets
        )
        bullets_html = f'      <ul style="list-style:none; margin:clamp(24px,4vh,36px) 0 0; padding:0; max-width:78ch;">\n{bullets_html}\n      </ul>'

    project_link = ""
    if kind == "case":
        project_link = f'      <p style="margin:clamp(24px,4vh,36px) 0 0;"><a href="{route("projects", lang)}" style="font-weight:500; color:#0D0D0C; border-bottom:1.5px solid #0D0D0C; padding-bottom:3px;">{html.escape({"de": "Alle Case Studies ansehen", "en": "View all case studies", "pl": "Zobacz wszystkie case studies"}[lang])}</a></p>'

    return f"""
  <section id="seo-summary" aria-label="{html.escape(eyebrow)}" style="background:#F3F1EA; color:#0D0D0C; border-top:1.5px solid #0D0D0C; padding:clamp(56px,9vh,104px) clamp(20px,3vw,48px);">
    <div class="seo-static-grid">
      <p style="margin:0; font-size:0.78rem; letter-spacing:0.12em; text-transform:uppercase; color:#4A4945;">{html.escape(eyebrow)}</p>
      <div style="min-width:0;">
        <h2 style="margin:0 0 clamp(22px,4vh,36px); font-weight:500; text-transform:uppercase; font-size:clamp(2rem,5vw,4.6rem); line-height:0.92; letter-spacing:0; max-width:15ch;">{html.escape(title)}</h2>
        <div style="display:grid; gap:18px;">
{paragraph_html}
        </div>
{bullets_html}
{project_link}
        <p style="margin:clamp(24px,4vh,36px) 0 0; font-size:0.78rem; letter-spacing:0.08em; text-transform:uppercase; color:#4A4945;">Last updated: {LASTMOD}</p>
      </div>
    </div>
  </section>"""


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
        f'          <a href="{href}"{" aria-current=\"page\"" if code == lang else ""} style="border-bottom:1.5px solid {"#0D0D0C" if code == lang else "transparent"}; padding-bottom:2px; color:{"#0D0D0C" if code == lang else "#4A4945"};">{code.upper()}</a>'
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
        f'<a href="{href}"{" aria-current=\"page\"" if code == lang else ""} style="border-bottom:1.5px solid {"#0D0D0C" if code == lang else "transparent"}; padding-bottom:2px; color:{"#0D0D0C" if code == lang else "#4A4945"};">{code.upper()}</a>'
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
    if "<style>" in body:
        body = body.replace("<style>\n", "<style>\n" + FONT_CSS + SITE_CSS, 1)
    else:
        body = "<style>\n" + FONT_CSS + SITE_CSS + "</style>\n" + body
    body = re.sub(r"letter-spacing:-0\.[0-9]+em", "letter-spacing:0", body)
    return body


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
    vestium_embed_src = f"https://www.youtube-nocookie.com/embed/{VESTIUM_YOUTUBE_ID}?rel=0&modestbranding=1"
    body = body.replace(
        '<x-import component-from-global-scope="image-slot" from="./image-slot.js" id="case05-prototype" shape="rect" radius="0" placeholder="{{ t.shotPlaceholder }}" hint-size="100%,360px" style="width:100%; height:100%; display:block;"></x-import>',
        '<sc-if value="{{ hasVestiumVideo }}" hint-placeholder-val="{{ false }}">\n'
        f'                  <iframe src="{vestium_embed_src}" title="Vestium prototype video" loading="lazy" allow="fullscreen; encrypted-media; picture-in-picture" allowfullscreen style="width:100%; height:100%; border:0; display:block; background:#0D0D0C;"></iframe>\n'
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
    body = re.sub(r"\s*<helmet>.*?</helmet>\s*", "\n", body, count=1, flags=re.S)
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
    if kind == "home":
        body = update_home_form(body)
    if slug == "vestium":
        body = update_vestium_video(body)
    body = body.replace("./image-slot.js", "")
    page = f"{head(lang, kind, slug)}\n<body>\n{body}\n{seo_static_section(kind, lang, slug)}\n</body>\n</html>\n"
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
