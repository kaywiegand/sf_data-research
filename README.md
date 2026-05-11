# Public Transport Resilience & Prediction
### Datenanalyse und Vorhersage im Stadtverkehr am Beispiel Tram Zürich

---

## Inhalt

1. [Kurzbeschreibung](#1-kurzbeschreibung)
2. [Die Idee](#2-die-idee)
3. [Warum Zürich — warum Tram?](#3-warum-zürich--warum-tram)
4. [Das Problem](#4-das-problem)
5. [Zentrale Fragen](#5-zentrale-fragen)
6. [Projekt-Phasen](#6-projekt-phasen)
7. [Daten & Quellen](#7-daten--quellen)
8. [Business Cases & KPIs](#8-business-cases--kpis)
9. [Motivation & Portfolio-Mehrwert](#9-motivation--portfolio-mehrwert)

---

## Projektstruktur



````
sf_data-research/
├── README.md
├── ROADMAP.md
│
├── notebooks/
│   ├── vbz/                           # Zürich (VBZ) Forschung
│   │   ├── data-events/               # Notebooks für Event-Processing
│   │   ├── data-geo/                  # Geodaten & Mapping Benchmarks (Folium, Kepler, etc.)
│   │   ├── data-gtfs/                 # Fahrplandaten-Aufbereitung
│   │   ├── data-ist/                  # Ist-Daten Analyse & Demos
│   │   ├── data-meteo/                # Wetterdaten-Pipeline
│   │   ├── vbz-data-preparation.ipynb # Haupt-Pipeline zur Datenbereinigung
│   │   ├── vbz-data-strategy.ipynb    # Technische Strategie & Typ-Optimierung
│   │   ├── vbz-pandas-vs-polars.ipynb # Performance-Vergleiche
│   │   └── vbz-master-validation.ipynb# Validierung des finalen Datensatzes
│   └── vbb/                           # Berlin/Brandenburg (VBB) Forschung
│       ├── vbb.ipynb                  # Basis-Analyse VBB
│       └── vbb-rt-feed.ipynb          # Realtime-Feed (GTFS-RT) Experimente
│
├── src/                               # Modularisierter Code & Skripte
│   ├── process_ist_daten.py           # Batch-Processing für tägliche Ist-Daten
│   └── doc_loader.py                  # Hilfsfunktionen für Dokumentation/Metadaten
│
├── reports/                           # Visualisierungen & Export-Ergebnisse
│   ├── *.html                         # Interaktive Karten (Folium)
│   ├── *.pdf                          # Statische Karten (GeoPandas)
│   └── *.svg                          # Pipeline-Diagramme & Status-Grafiken
│
├── data/
│   ├── raw/                           # Unveränderte Originaldaten (⚠️ .gitignore)
│   │   ├── vbz/                       # Rohdaten Zürich (GTFS, Meteo, Geo, Events)
│   │   └── vbb/                       # Rohdaten Berlin (GTFS 2023/24, RT-Logs)
│   │
│   └── interim/                       # Aufbereitete Daten im Zwischenformat
│       ├── vbz/                       # Bereinigte Parquet/CSV Dateien für Zürich
│       │   ├── ist-daten/             # ~1.100 tägliche Parquet-Dateien (2023–2025)
│       │   ├── gtfs/                  # Tram- & Regional-Lookups (Parquet)
│       │   ├── meteo/                 # Kombinierter meteo-master.parquet
│       │   ├── events/                # Zentraler events-master.csv
│       │   └── vbz_master.parquet     # Der finale, bereinigte Forschungs-Datensatz
│       └── vbb/                       # Zwischenstände Berlin (z.B. Linienfarben)
````


> Download-Anleitung Ist-Daten: `vbz-ist-daten.ipynb` und `vbz-ist-daten-demo.ipynb`

---


Dieses Projekt dient der Projekt-Idee und -Scope findung. Weiter der Recherche aller notwendigen Daten, Daten-Quellen und derer Aufbereitung für den eigentlich Projektstart. 

## 1. Kurzbeschreibung

Verspätungen im öffentlichen Nahverkehr sind ärgerlich — für Menschen und für das System.
Dieses Projekt zeigt, was mit offenen Daten und moderner Datenanalyse möglich ist:
Wo entstehen Probleme, warum — und wie lässt sich das vorhersagen?

Als Fallbeispiel dient das Tramnetz Zürich (VBZ). Das Modell soll auch als Blaupause
für andere Städte wie Berlin dienen, die noch kaum Daten öffentlich zur Verfügung stellen.

---

## 2. Die Idee

Aufbau einer vollständigen Datenpipeline zur Analyse und Vorhersage von Verspätungen
im städtischen ÖPNV — vom Rohdaten-Ingestion bis zum interaktiven Dashboard.

**Kernziel:** Zeigen, was Daten im Alltag bewirken können — konkret, nachvollziehbar, menschlich relevant.

---

## 3. Warum Zürich — warum Tram?

**Zürich als Datenbasis:**
- Außergewöhnlich gute Open-Data-Landschaft (Stadt, VBZ, Wetter, Geodaten)
- Hochattraktiver ÖV mit entsprechend hoher Nutzung → gute Analysegrundlage
- Kann als Inspiration und Benchmark für deutsche Städte dienen

**Tram als Fokus:**
- Tram fährt im offenen Stadtverkehr — beeinflusst durch Autos, Fußgänger, Wetter, Topografie
- Kein geschlossenes System wie S-Bahn → mehr und interessantere Einflussfaktoren
- Macht die Analyse für Betreiber und Stadtplanung besonders relevant

**Und Berlin?**
Berlin wäre das emotionalere Beispiel — aber die Datenlage lässt eine solche Analyse
aktuell nicht zu. Das Ziel: dieses Projekt als Anstoß, das zu ändern.

---

## 4. Das Problem

Verspätungen kennt jeder. Aber selten fragt man: **Warum passiert das eigentlich — und
könnte man es verhindern?**

Ein paar Situationen, die jeder kennt:
- Nach dem Konzert oder Fußballspiel stundenlang im Stau — der schöne Abend versaut
- Regelmäßig zu spät beim Arzt oder zur Arbeit — Stress, Frust, schlechte Laune
- Das Tram kommt einfach nicht — und keine verlässliche Info, wann es endlich kommt

Hinter diesen Momenten stecken oft vermeidbare Engpässe: bestimmte Haltestellen,
bestimmte Uhrzeiten, bestimmte Wetterbedingungen. Genau das will dieses Projekt sichtbar machen.

---

## 5. Zentrale Fragen

- Wo entstehen Verspätungen im Tramnetz — und zu welchen Zeiten?
- Welche Einflussfaktoren spielen die größte Rolle? (Wetter, Topografie, Tageszeit, Events)
- Lassen sich Verspätungen vorhersagen, bevor sie entstehen?
- Welche Haltestellen oder Streckenabschnitte lösen Kettenreaktionen aus?
- Was kann ein Betreiber oder eine Stadt konkret besser machen?

---

## 6. Projekt-Phasen

Der Scope ist bewusst in aufeinander aufbauende Versionen gestaffelt — um den MVP
sicher im Projektzeitrahmen zu erreichen und Raum für Erweiterungen zu lassen.

#### MVP – "The Foundation"
- **Data Wrangling:** Pipeline für Multi-Gigabyte-Archive (schweizweit), gefiltert auf `Betreiber: VBZ` & `Produkt: Tram`
- **Cleaning:** Bereinigung von Ausreißern, Transformation der Zeitstempel, Feature Engineering der Verspätungs-Metrik
- **EDA & Reporting:** Historische Analyse der Hotspots (Kreise/Haltestellen) und Korrelationsmatrix (Wetter vs. Delay)
- Einsatz des eigenen **wgnd-toolkit** und **wgnd-scaffolding**

#### v1.1 – "The Intelligence"
- Definition der Metriken und Methoden
- **Modellierung:** Training eines oder mehrerer Modelle zur Vorhersage von Verspätungen basierend auf Wetter, Zeit und Events
- **Evaluation:** Validierung der Vorhersagegenauigkeit pro Linie und Stadtteil

#### v1.2 – "The Interface"
- **Interaktives Dashboard:**
  - Tooling: Tableau vs. Dash & Plotly (Entscheidung im Projektverlauf)
  - Historik: Heatmaps der Stadtkreise und Zeitverläufe
  - Predictive: "What-if"-Eingabemaske — z.B. *Freitag + Regen + Spiel im Letzigrund → Erwarteter Delay*

#### v1.3 – "Individual Traffic Impact"
- Ergänzung der Verkehrsdichte aus Zählstellendaten (Induktionsschleifen Zürich) als zusätzliches Feature
- Aufzeigen des Zusammenspiels zwischen Tram-Verspätungen und Individualverkehr

---

## 7. Daten & Quellen

**Analysezeitraum:** 2023 – 2025

| Datentyp | Quelle | Strategie | Verzeichnis | Format |
| :--- | :--- | :--- | :--- | :--- |
| Verkehrsdaten | [opentransportdata.swiss](https://data.opentransportdata.swiss) | 2023–25, Filterung auf VBZ & Tram; Umstieg auf Format v2 berücksichtigt | `ist-daten/` | .zip / .parquet |
| Wetterdaten | [Stadt Zürich OGD](https://data.stadt-zuerich.ch/dataset/ugz_meteodaten_stundenmittelwerte) | Stundenmittelwerte (Niederschlag, Temperatur, Wind), Stationen Fluntern & Mythenquai | `meteo/` | .csv |
| Geodaten | [ZVV / Zürich OGD](https://data.stadt-zuerich.ch/dataset/vbz_fahrplandaten_gtfs) | GTFS-Pakete für Haltestellen-Koordinaten und Stadtkreis-Zuordnung | `gtfs/` | .txt |
| Eventdaten | Manueller Crawl | Kategorisiert nach: Stadion-Events, Stadtfeste, Konzerte, Messen, Ferien | `events/` | .csv |

**Zur Datenmenge:**
- 36 ZIP-Dateien über 3 Jahre → ca. **38 GB** komprimiert
- Entpackt: **500–750 GB** (schweizweite CSV-Rohdaten)
- Nach Filterung auf VBZ & Tram im Parquet-Format → **XXX GB** (wird ergänzt)
- Fallback: Reduktion auf repräsentative Stichproben + event-gelabelte Tage, falls Verarbeitungsaufwand zu hoch

---

## 8. Business Cases & KPIs

### Für den Betreiber (VBZ / Operative Exzellenz)
Ziel: Pünktlichkeit verbessern, Ressourcen gezielter einsetzen

| KPI | Beschreibung |
|---|---|
| On-Time Performance (OTP) | Anteil Fahrten < 2 Min Verspätung |
| Bottleneck Score | Haltestellen, die systemweite Folgeverspätungen auslösen |
| District Delay Index | Durchschnittliche Verspätung pro Stadtkreis |
| Recovery Time | Wie lange braucht das Netz nach einer Störung zur Stabilisierung? |
| Peak Load Variance | Auslastungsschwankungen zu Stoßzeiten |

### Für die Stadtplanung (Infrastruktur & Resilienz)
Ziel: Schwachstellen im Netz identifizieren, Investitionen priorisieren

| KPI | Beschreibung |
|---|---|
| Elevation Impact Ratio | Korrelation zwischen Streckensteigung und wetterbedingten Verspätungen |
| Hotspot Heatmap | Geografische Verteilung der Verspätungsdichte (GIS-basiert) |
| Weather Sensitivity Score | Wie stark reagiert eine Linie auf Regen, Schnee, Glatteis? |
| Infrastructure Bottleneck Index | Physische Engpässe mit regelmäßigem Verspätungsmuster |
| Event Impact Score | Verspätungsanstieg rund um Großveranstaltungen |

### Für Fahrgäste (Citizen Experience & Transparenz)
Ziel: Weniger Stress, mehr Verlässlichkeit im Alltag

| KPI | Beschreibung |
|---|---|
| Prediction Accuracy (MAE) | Vorhersagegenauigkeit pro Stadtteil oder Linie |
| Wait Time Variance | Wo schwanken Wartezeiten am stärksten? |
| Realtime Reliability Score | Übereinstimmung von Echtzeitanzeige und tatsächlicher Ankunft |
| Comfort Window | Anteil Fahrten mit planbarem Puffer für Anschlüsse |

### Gesellschaftlicher Impact (Nachhaltigkeit & Stadtqualität)
Ziel: ÖPNV attraktiver machen, Individualverkehr reduzieren

| KPI | Beschreibung |
|---|---|
| Modal Shift Potential | Geschätzte CO₂-Einsparung bei x% Verlagerung vom Auto |
| SDG 11 Readiness Score | Erfüllungsgrad der UN-Ziele für nachhaltigen Stadtverkehr |
| Noise & Emission Hotspots | Kritische Orte mit hoher Verkehrsbelastung und Alternativpotenzial |
| Livability Index Contribution | Einfluss von ÖPNV-Qualität auf die Lebensqualität pro Stadtkreis |

---

## 9. Motivation & Portfolio-Mehrwert

**Warum dieses Thema?**
Data Science und KI wirken für viele abstrakt. Dieses Projekt macht den Mehrwert
greifbar — an einem Thema, das jeden täglich betrifft.

**Impact — warum das mehr ist als ein Datenprojekt:**
- 🏙️ **Feel-Good City:** Verlässlicher ÖPNV verbessert direkt die Lebensqualität im Stadtraum
- 🌱 **Nachhaltigkeit:** Attraktiverer ÖPNV reduziert Individualverkehr — weniger CO₂, weniger Lärm
- 😤 **Emotionaler Alltag:** Verspätungen erzeugen echten Stress — Frust, Aggression, verpasste Termine
- 🗺️ **Städtebau:** Schwachstellen im Netz identifizieren und Investitionen gezielt steuern
- 🌍 **SDG 11:** Beitrag zu den UN-Zielen für nachhaltige Städte und Gemeinden

**Was steckt technisch drin?**
- Data Engineering: Ingestion, Cleaning, Wrangling großer Datenmengen
- Explorative Analyse (EDA) & Reporting
- Geodaten-Integration & Visualisierung
- Zeitreihenanalyse & Machine Learning (Vorhersagemodell)
- Interaktive Web-App als Abschluss

**Das größere Bild:**
Zürich dient als Referenzmodell — für Städte wie Berlin, die ihre Datenpotenziale
noch nicht ausschöpfen. Das Ziel ist nicht nur ein Portfolio-Projekt, sondern ein
konkreter Anstoß: Bessere Daten = bessere Städte = besserer Alltag für alle.