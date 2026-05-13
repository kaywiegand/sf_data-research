# PROCESS LOG
### VBZ Tram Zürich — Datenprojekt · Research Phase

---

## Zweck dieses Dokuments

Dieses File dokumentiert den gesamten Projektverlauf chronologisch und dient als
**Kontext-Einstieg für AI-Chats, Claude Code und Cowork-Sessions.**

> Lies dieses File als ersten Schritt — es ersetzt langes Nachfragen und ermöglicht
> sofortigen Einstieg in den aktuellen Projektstand.

---

## Projekt auf einen Blick

| | |
| :--- | :--- |
| **Projektname** | Public Transport Resilience & Prediction |
| **Kurzbeschreibung** | Analyse und Vorhersage von Tram-Verspätungen in Zürich auf Basis offener Daten |
| **Analysezeitraum** | 2023–2025 (IST-Daten Format v1, einheitlich) |
| **Betreiber** | VBZ (Verkehrsbetriebe Zürich), Verbund ZVV |
| **Repo** | `sf_data-research/` — Research & Datenbasis (diese Phase) |
| **Nächstes Repo** | `sf_data-analysis/` — EDA, Modellierung, Dashboard (Phase 2) |
| **Portfolio-Ziel** | Wiedereinstieg als Data Analyst / Data Scientist, Q3 2026 |
| **Stack** | Python · Polars (primär) · Pandas · GeoPandas · Plotly · Folium |

---

## Phase 1 — Research & Data Foundation ✅ ABGESCHLOSSEN

**Ziel:** Alle Datenquellen identifizieren, aufbereiten und zu einem finalen Master-Datensatz zusammenführen.

### Was wurde gemacht?

#### IST-Daten (Verkehr)
- **Quelle:** archive.opentransportdata.swiss — 36 monatliche ZIP-Archive, 2023–2025
- **Rohdaten:** ~38 GB komprimiert / ~720 GB entpackt / schweizweit
- **Filter:** `BETREIBER_ID = 85:3849` (VBZ) + `PRODUKT_ID = Tram` + `AN_PROGNOSE_STATUS = REAL` + keine Durchfahrten + keine Zusatzfahrten (Ausfälle bewusst behalten)
- **Ergebnis:** ~88 Mio. Zeilen · 8 Spalten · **1.081 Parquet-Dateien** · ~1,44 GB
- **Skript:** `src/process_ist_daten.py` (batch, resume-fähig)
- **Notebook:** `notebooks/vbz/data-ist/vbz-ist-daten.ipynb`

#### GTFS-Daten (Fahrplan & Geodaten Haltestellen)
- **Quelle:** data.stadt-zuerich.ch — VBZ Fahrplandaten GTFS, Jahrgänge 2023–2025
- **Referenzjahr:** 2024 (vollständigste Datenlage, stabilstes Jahr)
- **Exports:**
  - `gtfs_tram_*.parquet` — Shapes, Stops, Routes, Trips (für Geo-Karten)
  - `gtfs_stops_lookup.parquet` — Join-Tabelle: BPUIC → stop_name, stop_lat, stop_lon, district_nr, district_name
- **Stadtkreise:** Spatial Join (GeoPandas `sjoin within`) mit `stzh_adm_stadtkreise_v.json` — jede Haltestelle hat Stadtkreis 1–12; Haltestellen außerhalb Stadtgebiet = null
- **Notebook:** `notebooks/vbz/data-gtfs/vbz-gtfs-data.ipynb`

#### Meteo-Daten (Wetter)
- **Quellen:** UGZ Stampfenbachstrasse (Primär: Temperatur, Regen, Wind, Strahlung) + Wapo Mythenquai (Niederschlag mm) + ERZ Überschwemmungsmeldungen (Ereignis-Indikator)
- **Auflösung:** Stündlich konsolidiert (passend zu Tram-Zeitstempeln, Join-Schlüssel: `floor(1h)`)
- **Output:** `data/interim/vbz/meteo/meteo-final-export.parquet`
- **Notebook:** `notebooks/vbz/data-meteo/vbz-meteo-data.ipynb`

#### Event-Daten (Kalender)
- **Quellen:** Python `holidays`-Package + Gemini + Perplexity + Transfermarkt.de
- **Kategorien:** Feiertage (36) · Stadtfeste (12) · Konzerte (5) · Fachmessen & Kongresse (83) · Fussball (~115)
- **Gesamt:** 301 Einträge · 2023–2025
- **Gewichtungsschema:** 1 (mittel, >1.000 Besucher) / 2 (hoch, 10k–30k) / 3 (sehr hoch, >30k)
- **Output:** `data/interim/vbz/events/events-master.csv`
- **Notebook:** `notebooks/vbz/data-events/vbz-events-data.ipynb`

#### Geo-Daten & Visualisierungs-Benchmark
- **Quelle:** Stadt Zürich OGD — Stadtkreis-Polygone (CC0, WGS84)
- **Benchmark:** Plotly / GeoPandas / Folium / lonboard (Kepler) — alle vier mit drei Visualisierungstypen getestet
- **Ergebnisse:** Interaktive HTML-Karten und PDFs in `assets/`
- **Notebook:** `notebooks/vbz/data-geo/vbz-geo-data.ipynb` + 4 Map-Notebooks

#### Polars vs. Pandas Benchmark
- **Ergebnis auf echten 88 Mio. Zeilen:**

| | Pandas | Polars | Faktor |
| :--- | ---: | ---: | ---: |
| Ladezeit | 25,7s | 6,6s | **4× schneller** |
| RAM-Verbrauch | 6,1 GB | ~1,4 GB | **4× sparsamer** |

- **Entscheidung:** Polars für alle großen Operationen (IST-Daten, Merge). Pandas für kleine Hilfstabellen (GTFS, Meteo, Events).
- **Notebook:** `notebooks/vbz/vbz-pandas-vs-polars.ipynb`

#### Master-Merge (vbz_master.parquet)
- **Notebook:** `notebooks/vbz/vbz-data-master-preparation.ipynb`
- **Join-Strategie:** Left Join überall (jede Tram-Fahrt bleibt erhalten, fehlende Werte = null)

| Join | Schlüssel |
| :--- | :--- |
| IST + GTFS Stops | `bpuic` = `bpuic` |
| IST + Meteo | `floor(arrival_schedule, '1h')` = `date_time` |
| IST + Events | `date(operating_date)` = `Datum` |

- **Validation:** `notebooks/vbz/vbz-data-master-validation.ipynb` — 8 Checks: Schema, Abdeckung, Wertebereiche, Nulls, Join-Qualität, Cross-Check, Business-Logik, Zusammenfassung

#### Datenstrategie dokumentiert
- **Notebook:** `notebooks/vbz/vbz-data-strategy.ipynb`
- Alle Filter-Entscheidungen transparent begründet
- Scope: 2023–2025, v1-Format (ab Mitte 2025 Format v2 → bewusst ausgeschlossen)
- Fahrplanwechsel 14. Dezember 2025: altes Liniennetz vollständig abgedeckt, kein Mischformat

#### Nebenprojekt: VBB Berlin (Exploratorisch)
- **Notebooks:** `notebooks/vbb/` — GTFS-Daten und GTFS-RT Feed untersucht
- **Ergebnis:** Keine historischen GTFS-RT Daten verfügbar (VBB-Feed seit 10.03.2026 offline). Zürich bleibt Datenbasis, Berlin dient als narrativer Referenzpunkt.

---

## Finaler Master-Datensatz

**Datei:** `data/interim/vbz/vbz_master.parquet`

| Spalte | Typ | Quelle | Beschreibung |
| :--- | :--- | :--- | :--- |
| `operating_date` | Date | IST | Betriebstag |
| `line_name` | Categorical | IST | Tramliniennummer (z.B. "11") |
| `bpuic` | Int32 | IST | Haltestellen-ID (Join-Schlüssel) |
| `arrival_schedule` | Datetime | IST | Planmäßige Ankunftszeit |
| `arrival_delay` | Float32 | IST | Verspätung Ankunft in Sekunden |
| `departure_schedule` | Datetime | IST | Planmäßige Abfahrtszeit |
| `departure_delay` | Float32 | IST | Verspätung Abfahrt in Sekunden |
| `canceled` | Boolean | IST | Ausfall = True |
| `stop_name` | Categorical | GTFS | Haltestellenname |
| `stop_lat` | Float32 | GTFS | Breitengrad |
| `stop_lon` | Float32 | GTFS | Längengrad |
| `district_nr` | Int8 | GTFS+Geo | Stadtkreis 1–12 (null = außerhalb) |
| `district_name` | Categorical | GTFS+Geo | Stadtkreisname ("Kreis N") |
| `temperature` | Float32 | Meteo | Temperatur °C |
| `humidity` | Float32 | Meteo | Luftfeuchtigkeit % |
| `rain_duration` | Float32 | Meteo | Regendauer min/h |
| `precipitation` | Float32 | Meteo | Niederschlag mm |
| `wind_speed` | Float32 | Meteo | Windgeschwindigkeit km/h |
| `global_radiation` | Float32 | Meteo | Globalstrahlung W/m² |
| `flood_intensity` | Int16 | Meteo | Überschwemmungsindikator |
| `event_name` | Categorical | Events | Name des Events (null = kein Event) |
| `event_type` | Categorical | Events | Kategorie (Konzert, Fussball, …) |
| `event_size` | Int8 | Events | Gewichtung 1–3 |
| `event_location` | Categorical | Events | Veranstaltungsort |

---

## Wichtige Entscheidungen & Begründungen

| Entscheidung | Was | Warum |
| :--- | :--- | :--- |
| Polars statt Pandas | Haupt-DataFrame-Bibliothek | 4× schneller, 4× weniger RAM bei 88 Mio. Zeilen |
| Left Join überall | Merge-Strategie | Kein Datenverlust durch Join-Lücken |
| 2024 als GTFS-Referenzjahr | Fahrplandaten | Vollständigste Datenlage, stabilstes Jahr |
| 2 Meteo-Stationen | Stampfenbachstrasse + Mythenquai | Zwei Topografien: Stadtlage vs. Seelage |
| Scope 2023–2025 v1 | Analysezeitraum | Einheitliches Datenformat, kein Mischformat |
| Stadtkreis im Lookup | district im GTFS-Join, nicht in EDA | Einmalig sauber im Master, kein wiederholter Spatial Join |
| Ausfälle behalten | `canceled = True` | Extremster Verspätungsfall, für Modell unverzichtbar |
| Schwellenwert Events | >1.000 Besucher | Kleinere Events kein messbarer Netzeinfluss |

---

## Repo-Struktur (Stand Phase 1 Abschluss)

```
sf_data-research/
├── PROCESS_LOG.md                          ← dieses File
├── README.md                               ← Projektbeschreibung
├── ROADMAP.md                              ← Phasen & Todos
│
├── notebooks/vbz/
│   ├── data-events/vbz-events-data.ipynb   ✅ fertig
│   ├── data-geo/vbz-geo-data.ipynb         ✅ fertig (+ 4 Map-Notebooks)
│   ├── data-gtfs/vbz-gtfs-data.ipynb       ✅ fertig
│   ├── data-ist/vbz-ist-daten.ipynb        ✅ fertig
│   ├── data-meteo/vbz-meteo-data.ipynb     ✅ fertig
│   ├── vbz-data.ipynb                      ✅ Datenquellen & Überblick
│   ├── vbz-data-strategy.ipynb             ✅ Entscheidungen & Pipeline
│   ├── vbz-data-master-preparation.ipynb   ✅ Merge-Pipeline (Polars)
│   ├── vbz-data-master-validation.ipynb    ✅ 8-Check Validierung
│   └── vbz-pandas-vs-polars.ipynb          ✅ Benchmark & Lernnotebook
│
├── notebooks/vbb/                          ⚠️ exploratorisch, kein Datensatz verfügbar
│
├── src/
│   ├── process_ist_daten.py                ✅ Batch-Processing IST-Daten
│   └── doc_loader.py                       ✅ Datenwörterbuch-Helper
│
├── assets/                                 ✅ Karten, SVGs, Diagramme
│
└── data/interim/vbz/
    ├── ist-daten/          ✅ 1.081 Parquets · 1,44 GB
    ├── gtfs/               ✅ gtfs_tram_*.parquet + gtfs_stops_lookup.parquet
    ├── meteo/              ✅ meteo-final-export.parquet
    ├── events/             ✅ events-master.csv (301 Einträge)
    └── vbz_master.parquet  ✅ finaler Master-Datensatz
```

---

## Aktueller Stand & nächster Schritt

**Phase 1: ✅ Abgeschlossen**

**Phase 2: EDA & Analyse — startet jetzt im neuen Repo `sf_data-analysis/`**

Das neue Projekt übernimmt `vbz_master.parquet` als Input. Die Datenbasis ist vollständig und validiert.

**Offene Entscheidungen für Phase 2:**

| Entscheidung | Kontext |
| :--- | :--- |
| Dashboard-Tooling | Dash + Plotly vs. Streamlit vs. Tableau — nach EDA entscheiden |
| Zeitreihe vs. klassisches ML | Erst nach EDA sinnvoll zu entscheiden |
| Split-Strategie | Jahres-Split als Einstieg (2025 als Test-Jahr) — in Phase 3 verfeinern |
| Geo-Bibliothek für Dashboard | Folium (interaktiv, einfach) oder Plotly (performanter) |

---

## Nachtrag 2026-05-13 — Fehlende Monate im Master entdeckt

### Befund

Im EDA-Notebook (`zh-tram-flow/notebooks/01_exploration.ipynb`) fiel auf, dass
**April 2023 und Oktober 2023** im Master-Datensatz fehlen.

Ursache: Beim ursprünglichen Master-Build waren **1.036 Parquet-Dateien** in
`data/interim/vbz/ist-daten/`. Inzwischen sind es **1.081** — 46 Dateien wurden
nachträglich hinzugefügt (April 2023 komplett + Oktober 2023 teilweise).

### Details

| Monat | IST-Dateien vorhanden | Wiederherstellbar? |
| :--- | :--- | :--- |
| April 2023 | 30/30 Tage ✅ | Vollständig |
| Oktober 2023 | 31/31 Tage ✅ | Vollständig (19.–21. Okt. = 0 Zeilen nach Filter, Quelldaten leer) |

Meteo-Daten sind für beide Monate vollständig abgedeckt (nicht die Ursache).

### Fix

`vbz-data-master-preparation.ipynb` neu ausführen — das Notebook scannt alle
`*.parquet` in `IST_DIR`, sodass die neuen Dateien automatisch eingeschlossen werden.

**Vorher bestätigen:** `len(glob(IST_DIR / "*.parquet"))` sollte **1.096** ausgeben.

Nach dem Re-Run: `vbz_master.parquet` in `zh-tram-flow/data/raw/zh-tram-data-master.parquet`
kopieren und alle Zählungen (~88 Mio. Zeilen) in beiden Repos aktualisieren.
