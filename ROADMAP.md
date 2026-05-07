# Roadmap

---

## Woche 1 — Scoping & Tooling

### Daten & Wrangling
- Ist-Daten: Spaltenreduktion & Filterlogik finalisiert ✅
- Ist-Daten: Parquets auf 8 Spalten reduziert ✅
- Events: Kategorien, Gewichtung, Master-CSV ✅
- GTFS einlesen & Struktur verstehen
- Wetterdaten einlesen & Struktur verstehen

### Tooling & Strategy
- Pandas vs. Polars Benchmark ✅
- Polars Einstieg (Tutorial, Docs)
- Toolkit: Funktionen identifizieren die auf Polars umgestellt werden müssen
- Datenstrategie & Split-Optionen dokumentiert ✅

### Erste Visualisierung
- Alle Tramhaltestellen auf Zürich-Karte (Folium oder Plotly)
- Linienverläufe aus GTFS einzeichnen
- Tooling-Entscheidung: Folium vs. Plotly

---

## Woche 2 — EDA: Analyse

### Zentrale Analysefragen
- Wo entstehen die meisten Verspätungen? (Haltestelle, Linie, Stadtkreis)
- Wann? (Tageszeit, Wochentag, Saison)
- Korrelation Verspätung ↔ Wetter
- Korrelation Verspätung ↔ Events
- Ausreißer & Extremfälle identifizieren

### Joins & Datenzusammenführung
- Ist-Daten + GTFS (BPUIC → Koordinaten, Stadtkreis)
- Ist-Daten + Wetter (Datum + Stunde)
- Ist-Daten + Events (BETRIEBSTAG)

### Visualisierungen
- Heatmap Verspätungen nach Tageszeit und Wochentag
- Geografische Hotspot-Karte
- Zeitreihe Verspätungen 2023–2024
- Event-Tage vs. normale Tage — visueller Vergleich

---

## Woche 3 — DSC: Modell

### Vorbereitung
- Feature Engineering finalisieren
- Split-Strategie festlegen (Option A: Jahres-Split als Einstieg)
- 2025 als Test-Jahr reservieren — ab jetzt nicht mehr anfassen

### Modellierung
- Baseline-Modell definieren (einfachste sinnvolle Vorhersage)
- Zeitreihenmodell vs. klassisches ML entscheiden
- Training & Evaluation

### Validierung
- Vorhersagegenauigkeit pro Linie und Stadtkreis
- Verhalten auf Event-Tagen prüfen
- Split-Strategie verfeinern (Option D: Bi-Weekly + Whitelist)

---

## Bonus — Dashboard & Präsentation

### Tooling-Entscheidung
- Dash + Plotly vs. Streamlit vs. Tableau
- Entscheidung basierend auf EDA-Erfahrung aus Woche 2

### Interface
- Historik: Heatmaps Stadtkreise und Zeitverläufe
- Predictive: What-if Eingabemaske
  (z.B. Freitag + Regen + Spiel im Letzigrund → Erwarteter Delay)

---

## Offene Entscheidungen

| Entscheidung | Wann |
| :--- | :--- |
| Folium vs. Plotly für Karten | Woche 1 Ende |
| Dashboard-Tooling | Woche 2 Ende |
| Zeitreihe vs. klassisches ML | Woche 3 Anfang |
| Split-Strategie final | Woche 3 Anfang |