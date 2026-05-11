# Roadmap

---

## ✅ Phase 1 — Research & Data Foundation · ABGESCHLOSSEN

### Daten & Aufbereitung
- IST-Daten: Download, Filter, Parquet-Konvertierung ✅
- IST-Daten: 8 Spalten, ~88 Mio. Zeilen, 1.036 Parquets, ~1,44 GB ✅
- GTFS: Einlesen, Filtern auf VBZ Tram, 4 Parquet-Exports ✅
- GTFS: `gtfs_stops_lookup.parquet` mit Spatial Join (Stadtkreise 1–12) ✅
- Meteo: 3 Quellen konsolidiert → `meteo-final-export.parquet` (stündlich) ✅
- Events: 5 Kategorien, 301 Einträge, Gewichtungsschema → `events-master.csv` ✅
- Geo: Stadtkreis-Polygone, Tramlinien, Haltestellen ✅

### Tooling & Strategie
- Polars vs. Pandas Benchmark → Polars (4× schneller, 4× weniger RAM) ✅
- Join-Strategie dokumentiert (Left Join, alle 3 Schichten) ✅
- Datenstrategie vollständig dokumentiert (`vbz-data-strategy.ipynb`) ✅

### Master-Datensatz
- Merge-Pipeline gebaut (`vbz-data-master-preparation.ipynb`, Polars) ✅
- `vbz_master.parquet` erstellt — 24 Spalten: IST + GTFS + Meteo + Events ✅
- Validierung abgeschlossen (`vbz-data-master-validation.ipynb`, 8 Checks) ✅

### Visualisierungs-Benchmark
- Plotly, GeoPandas, Folium, lonboard/Kepler getestet ✅
- Netzübersicht, Heatmap und Streckenabschnitte in allen Tools ✅
- Ergebnisse in `assets/` (HTML, PDF, SVG) ✅

### Nebenprojekt VBB Berlin
- GTFS-Daten und GTFS-RT Feed untersucht ✅
- Kein historischer Datensatz verfügbar (Feed offline seit 10.03.2026) ✅
- Fazit: Zürich bleibt Datenbasis; Berlin dient als narrativer Referenzpunkt ✅

---

## Phase 2 — EDA & Analyse · NÄCHSTER SCHRITT

> Neues Repo: `sf_data-analysis/`
> Input: `vbz_master.parquet` aus diesem Research-Repo

### Setup
- Neues Projekt aufsetzen mit wgnd.scaffold und wgnd.toolkit
- `vbz_master.parquet` in das neue Repo überführen
- Erste Datenchecks: Was ist drin, Verteilungen, Datenqualität bestätigen

### Zentrale Analysefragen
- Wo entstehen die meisten Verspätungen? (Haltestelle, Linie, Stadtkreis)
- Wann? (Tageszeit, Wochentag, Saison)
- Korrelation Verspätung ↔ Wetter (Regen, Temperatur, Wind)
- Korrelation Verspätung ↔ Events (Gewichtung 1–3)
- Ausreißer & Extremfälle identifizieren (Ausfälle, Kettenverspätungen)

### Visualisierungen
- Heatmap Verspätungen nach Tageszeit und Wochentag
- Geografische Hotspot-Karte (Stadtkreise, Haltestellen)
- Zeitreihe Verspätungen 2023–2025
- Event-Tage vs. normale Tage — visueller Vergleich

---

## Phase 3 — Modellierung · GEPLANT

### Vorbereitung
- Feature Engineering finalisieren
- Split-Strategie festlegen (Jahres-Split als Einstieg: 2025 als Test-Jahr)
- 2025 als Test-Jahr reservieren — ab jetzt nicht mehr anfassen

### Modellierung
- Baseline-Modell definieren (einfachste sinnvolle Vorhersage)
- Zeitreihenmodell vs. klassisches ML entscheiden (nach EDA)
- Training & Evaluation

### Validierung
- Vorhersagegenauigkeit pro Linie und Stadtkreis
- Verhalten auf Event-Tagen prüfen
- Split-Strategie verfeinern (Option D: Bi-Weekly + Whitelist)

---

## Bonus — Dashboard & Präsentation · GEPLANT

### Tooling-Entscheidung
- Dash + Plotly vs. Streamlit vs. Tableau
- Entscheidung nach EDA-Erfahrung aus Phase 2

### Interface
- Historik: Heatmaps Stadtkreise und Zeitverläufe
- Predictive: What-if Eingabemaske
  (z.B. Freitag + Regen + Spiel im Letzigrund → Erwarteter Delay)

---

## Offene Entscheidungen

| Entscheidung | Wann |
| :--- | :--- |
| Dashboard-Tooling | Phase 2 Ende |
| Zeitreihe vs. klassisches ML | Phase 3 Anfang |
| Split-Strategie final | Phase 3 Anfang |
| Geo-Bibliothek für Dashboard | Phase 2 Ende (nach Erfahrung aus EDA) |
