# Krav til Eksamensprojekt – Programmering

## Projektoversigt

Type: Individuelt eller gruppe (op til 4 studerende)

Afleveringsdato: 5. december 2025

Aflevering: ZIP-fil + rapport via WISEflow

Eksamensformat: 30 minutter:
- 5 min præsentation
- 20 min live-kodning og spørgsmål/svar
- 5 min bedømmelse


## Kontekst

Sikkerhedsfirmaet SECO står fortsat over for sikkerhedsudfordringer. Med udgangspunkt i
dit arbejde fra Obligatorisk Opgave 1 og 2 skal du nu udvikle et omfattende system til
trusselsanalyse ved hjælp af den live hændelses-API.

Vigtigt: API’en genererer nu hændelser kontinuerligt. Hvis den tilgås efter en måned, kan
der være ca. 2000+ hændelser i systemet. Dit program skal håndtere store datamængder
effektivt.


## Programkrav

1. API-integration
    - Forbind til hændelses-API og hent autentificeringstoken
    - Implementér korrekt token-håndtering (lagring/fornyelse)
    - Håndter store datamængder (2000+ hændelser) effektivt via pagination
    - Brug passende HTTP-metoder med korrekte headers
    - Implementér retry-logik ved fejl i forespørgsler
2. Databehandling
    - Pars JSON-hændelsesdata til Python-objekter
    - Udtræk og kategorisér Indicators of Compromise (IOCs)
    - Håndter manglende eller fejlformaterede data elegant
3. Database-lagring
    - Design og implementér en SQLite-database
    - Gem hændelser med korrekte relationer mellem tabeller
    - Minimum anbefalet skema:
        - Incidents-tabel: `incidentId`, `incidentName`, `severity`, `status`, `createdTime`
        - Alerts-tabel: `alertId`, `incidentId`, `machineId`, `detectionSource`, `firstActivity`
        - IOCs (entities)-tabel: `incidentId`, `type` (fx `domains`, `emails`, `fileHashes`, `ips`,
       `processes`, osv.), `value`
    - Implementér korrekte databaseforbindelser og transaktioner
    - Håndter dubletter korrekt
4. Fejlhåndtering
    - Validér alle API-responser
    - Håndter netværksfejl og timeouts
    - Administrér rate limiting (50 forespørgsler/minut, 1500/time)
    - Validér data før indsættelse i databasen
    - Implementér korrekt exception-håndtering
    - Implementér grundlæggende logging (skriv til fil eller brug logging-modul)
    - Log fejl, advarsler og vigtige operationer
5. Kodekvalitet
    - Følg PEP8-konventioner
    - Inkludér omfattende dokumentation:
    - Funktion-docstrings
    - Inline-kommentarer til kompleks logik
    - Organisér koden i logiske funktioner
    - Brug meningsfulde variabel- og funktionsnavne
    - Hvis AI bruges til dokumentation, skal det markeres tydeligt


## Tekniske krav

Påkrævede Python-moduler:
- requests – API-kommunikation
- json – JSON-parsing
- sqlite3 – Databaseoperationer
- datetime – Tidsstempel-håndtering

Anbefalede ekstra moduler:
- logging – Logging
- time – Rate limiting/forsinkelser


## Afleveringer

1. Kildekode
    - Velorganiserede Python-filer
    - Konfigurationsfil til API-indstillinger (uden hardkodede tokens)
    - Script til oprettelse af database
2. Skriftlig rapport (maks. 5 sider)
    - Problemanalyse
    - Designbeslutninger og begrundelser
    - Udfordringer og løsninger
    - Fremtidige forbedringer


## Præsentation (5 minutter)

Vælg at præsentere:
- Systemarkitektur og design
- Live-demonstration af programfunktionalitet
- Tekniske udfordringer og løsninger
- Dataanalyse og indsigter
- Gennemgang af kritiske kodeafsnit
- Forslag til fremtidige forbedringer

Vigtigt: Ved hentning af 2000 hændelser med 100 pr. forespørgsel:
- Kræver 20 API-kald
- Tager ca. 24–30 sekunder (med rate limiting)
- Planlæg din implementering derefter
- Husk: Vi ønsker ikke dubletter i databasen

Sikkerhedsovervejelser
- Hardkod aldrig API-tokens i kildekoden
- Brug miljøvariabler eller konfigurationsfiler
- Implementér korrekte fejlmeddelelser uden at afsløre følsomme oplysninger
- Håndter API-legitimationsoplysninger sikkert


## Ressourcer

- API-dokumentation: [API_GUIDE.md](./API_GUIDE.md)
- Python-dokumentation: https://docs.python.org/3/
- SQLite-dokumentation: https://docs.python.org/3/library/sqlite3.html
- Requests-bibliotek: https://requests.readthedocs.io/
- PEP8 Style Guide: https://pep8.org/

Held og lykke med dit eksamensprojekt!
