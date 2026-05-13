# ROADMAP.md – Data-Research

---

## Phase 0 — Research & Data Foundation ✅ ABGESCHLOSSEN
> Vollständig dokumentiert in [`sf_data-research`](https://github.com/kaywiegand/sf_data-research)

- ✅ IST-Daten: Download, Filter, Parquet-Konvertierung
- ✅ IST-Daten: 8 Spalten, ~88 Mio. Zeilen, 1.036 Parquets, ~1,44 GB
- ✅ GTFS: Einlesen, Filtern auf VBZ Tram, 4 Parquet-Exports
- ✅ GTFS: `gtfs_stops_lookup.parquet` mit Spatial Join (Stadtkreise 1–12)
- ✅ Meteo: 3 Quellen konsolidiert → `meteo-final-export.parquet` (stündlich)
- ✅ Events: 5 Kategorien, 301 Einträge, Gewichtungsschema
- ✅ Polars vs. Pandas Benchmark → Polars (4× schneller, 4× weniger RAM)
- ✅ Master-Datensatz `vbz_master.parquet` erstellt — 24 Spalten: IST + GTFS + Meteo + Events
- ✅ Validierung abgeschlossen (8 Checks: Schema, Abdeckung, Wertebereiche, Nulls, Join-Qualität)

---

## Phase 1 — Setup & Dateneinstieg 

---

## Phase 2 — EDA & Analyse 
### EDA Notebook
### Zentrale Analysefragen
### Visualisierungen

---

## Phase 3 — Cleaning & Vorbereitung · AKTUELL
### Cleaning-Architektur (aus EDA-Findings)
### Feature Engineering

---

## Phase 4 — Modellierung · GEPLANT
### Modell-Entscheidung (aus EDA-Findings)

---

## Phase 5 — Dashboard & Präsentation · GEPLANT
### Tooling-Entscheidung
### Interface

---
