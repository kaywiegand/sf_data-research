# Data Foundation — VBZ Tram-Daten Dokumentation

Dieses Dokument dient als **Single Source of Truth** für die Herkunft, Struktur und Besonderheiten der Master-Daten in `sf_data-research`.

Neue Sessions können hier alles nachschlagen statt im Code zu raten.

---

## Überblick

**Master-Datensatz:** `data/interim/vbz/vbz_master.parquet`

| | |
| :--- | :--- |
| **Zeilen** | 94,358,531 |
| **Spalten** | 26 |
| **Größe** | 567 MB |
| **Analyse-Zeitraum** | 2023-01-01 bis 2025-12-31 |
| **Betreiber** | VBZ (Verkehrsbetriebe Zürich) |
| **Produkt** | Tram (Straßenbahnen) |
| **Datenquellen** | IST-Echtzeitdaten + GTFS Fahrplan + Wetterdaten + Events |

---

## 1. Datenherkunft & Aufbereitung

### 1.1 IST-Daten (Verkehr)

**Quelle:** [archive.opentransportdata.swiss](https://archive.opentransportdata.swiss/istdaten/)

- 36 monatliche ZIP-Archive (2023–2025)
- ~38 GB komprimiert → ~720 GB entpackt (schweizweit)
- **Filter:** `BETREIBER_ID = 85:3849` (VBZ) + `PRODUKT_ID = Tram`
- **Zeilenfilter:**
  - ✅ `AN_PROGNOSE_STATUS = 'REAL'` — verlässliche Echtzeitmessungen
  - ✅ `FAELLT_AUS_TF = 'true'` — Ausfälle (extremste Verspätungen)
  - ❌ `DURCHFAHRT_TF = 'true'` — kein Halt = nicht relevant
  - ❌ `ZUSATZFAHRT_TF = 'true'` — kein Fahrplan-Soll vorhanden

**Verarbeitung:** Skript `src/process_ist_daten.py` (batch, resume-fähig)

**Ergebnis:** 1.096 Parquet-Dateien, 92,906,148 Zeilen, 608 MB

### 1.2 GTFS-Daten (Fahrplan & Geodaten)

**Quelle:** [data.stadt-zuerich.ch](https://data.stadt-zuerich.ch/dataset/vbz_fahrplandaten_gtfs)

**Referenzjahr:** 2024 (vollständigste Datenlage, stabilstes Jahr)

**Exports:**
| File | Zeilen | Zweck |
| :--- | ---: | :--- |
| `gtfs_tram_stops.parquet` | 7.202 | Haltestellen: `stop_id`, `stop_name`, `stop_lat`, `stop_lon` |
| `gtfs_tram_routes.parquet` | 49 | Linien: `route_id`, `route_short_name`, `route_color` |
| `gtfs_tram_trips.parquet` | 182.976 | Fahrten: `trip_id`, `route_id`, `shape_id`, `direction_id` |
| `gtfs_tram_shapes.parquet` | 535.930 | Streckengeometrie: `shape_id`, `lat`, `lon`, `sequence` |
| `gtfs_stops_lookup.parquet` | — | **Extended:** BPUIC → `stop_name`, `stop_lat`, `stop_lon`, `district_nr`, `district_name` |

**Warum `gtfs_stops_lookup` statt `gtfs_tram_stops`?**

Die `gtfs_tram_stops.parquet` nutzt SLOID-Format als Schlüssel (`ch:1:sloid:90805::0`), der nicht direkt mit `bpuic` (IST-Daten) joinbar ist.

Die Lookup-Tabelle wurde speziell gebaut (Notebook: `vbz-gtfs-data.ipynb`):
- BPUIC aus `stop_url` extrahiert
- 1 Zeile pro eindeutige Haltestelle
- Mittlere Koordinaten für alle Duplikate
- **Spatial Join** mit `stzh_adm_stadtkreise_v.json` → `district_nr` (1–12) + `district_name` ("Kreis N")
  - Haltestellen außerhalb Stadtgebiet → `district_nr = null`

**Verarbeitung:** Notebook `notebooks/vbz/data-gtfs/vbz-gtfs-data.ipynb`

### 1.3 Wetterdaten (Meteo)

**Quellen:**
- **UGZ Stampfenbachstrasse** (Primär): Temperatur, Luftfeuchtigkeit, Regen, Windgeschwindigkeit, Globalstrahlung
- **Wapo Mythenquai** (Niederschlag): Zusätzliche Regenmessung (Seelage)
- **ERZ Überschwemmungsmeldungen**: Hochwasser-Indikator

**Auflösung:** Stündlich konsolidiert (passend zu Tram-Zeitstempeln)

**Join-Schlüssel:** `floor(arrival_schedule, '1h')` = `date_time`

**Verarbeitung:** Notebook `notebooks/vbz/data-meteo/vbz-meteo-data.ipynb`

**Ergebnis:** `meteo-final-export.parquet`, 26.304 Einträge

### 1.4 Event-Daten (Kalender)

**Quellen:**
- Python `holidays`-Package (Schweizer Feiertage)
- Gemini + Perplexity (Manueller Crawl)
- Transfermarkt.de (Fussball-Spielplan)

**Kategorien & Gewichtung:**
- Feiertage (36) — Gewicht 1 (mittel)
- Stadtfeste (12) — Gewicht 1–2
- Konzerte (5) — Gewicht 2–3
- Fachmessen & Kongresse (83) — Gewicht 1–2
- Fussball (~115) — Gewicht 2–3 (nach Ligastufe)

**Schwellenwert:** >1.000 Besucher (kleinere Events kein messbarer Netzeinfluss)

**Verarbeitung:** Notebook `notebooks/vbz/data-events/vbz-events-data.ipynb`

**Ergebnis:** `events-master.csv`, 258 Einträge (2023–2025)

---

## 2. stop_sequence — Herkunft & Berechnung

### Was ist stop_sequence?

Die **Reihenfolge des Halts innerhalb einer Fahrt** (1-basiert, nach Ankünftszeit sortiert).

Beispiel Fahrt `L11-2023-05-15-11:30`:
```
stop_sequence  stop_name             arrival_schedule
1              Albisgütli           11:30:00
2              Tramhalle Werkhof    11:34:00
3              Binzmühlestr.        11:36:00
...
N              Endstation           12:15:00
```

### Herkunft

**Quelle:** IST-Rohdaten von opentransportdata.swiss

**Berechnung:** `vbz-ist-daten.ipynb`

```python
# Sortiere nach Soll-Ankunftszeit (chronologisch)
df = df.sort_values(["BETRIEBSTAG", "FAHRT_BEZEICHNER", "ANKUNFTSZEIT"])

# Reihenfolge berechnen: 1, 2, 3, ... pro Fahrt
df["stop_sequence"] = (
    df.groupby(["BETRIEBSTAG", "FAHRT_BEZEICHNER"]).cumcount() + 1
).astype("int16")
```

### Warum ist das elegant?

- ✅ **GTFS stop_times.parquet ist nicht nötig** — stop_sequence kommt direkt aus IST-Daten
- ✅ **Automatisch konsistent** — IST-Daten kommen bereits in chronologischer Reihenfolge
- ✅ **Keine Duplikate oder Anomalien** — groupby+cumcount ist garantiert eindeutig
- ✅ **Speichereffizient** — nur `Int16` (2 Bytes pro Halt)

### Was bedeutet die Sortierung?

Die Sortierung nach `arrival_schedule` (Soll-Ankunftszeit) ist **korrekt** weil:
1. IST-Daten sind *immer* chronologisch nach Ankunftszeit geordert
2. `stop_sequence` folgt der **geplanten** Reihenfolge (nicht der tatsächlichen)
3. Verspätete oder zu früh angekommene Fahrten ändern die Reihenfolge nicht

### Historischer Hintergrund

- **Frühe Version:** `FAHRT_BEZEICHNER` (trip_id) war fälschlicherweise gelöscht
  → Keine Trip-Level-Aggregation möglich
- **2026-05-15:** Nachtrag: `FAHRT_BEZEICHNER` + `stop_sequence` hinzugefügt
  → Alle 1.096 Parquets neu prozessiert
  → Master-Datensatz aktualisiert (88 Mio. → 92,9 Mio. Zeilen)

---

## 3. GTFS-Struktur

### Dateien & Übersicht

| File | Vorhanden? | Größe | Format | Zweck | Notizen |
| :--- | :---: | :--- | :--- | :--- | :--- |
| `gtfs_tram_stops.parquet` | ✅ | ~5 MB | Parquet | Haltestellen: stop_id, name, lat, lon | Jahrgänge: 2023, 2024, 2025 |
| `gtfs_tram_routes.parquet` | ✅ | <1 MB | Parquet | Linien: route_id, route_short_name, route_color | per year |
| `gtfs_tram_trips.parquet` | ✅ | ~10 MB | Parquet | Fahrten: trip_id, route_id, shape_id, direction_id | per year |
| `gtfs_tram_shapes.parquet` | ✅ | ~15 MB | Parquet | Streckengeometrie: shape_id, lat, lon, sequence | per year |
| `gtfs_stops_lookup.parquet` | ✅ | ~2 MB | Parquet | **Join-Tabelle:** bpuic → stop_name, coords, district | de-duped, extended |
| `stop_times.parquet` | ❌ | — | — | **NICHT konvertiert** | Raw .txt existiert in `data/raw/` |

### Warum stop_times.parquet fehlt

**Raw-Files existieren:** `data/raw/vbz/gtfs/*/stop_times.txt` (für jedes Jahr)

**Wurden NICHT zu Parquet konvertiert** weil:
- `stop_sequence` wird aus **IST-Daten berechnet** (elegantere Lösung)
- GTFS stop_times ist daher redundant
- Speichert eine GB+ an unkomprimiertem Format

**Wenn du stop_times.parquet brauchst:**
1. Raw `.txt`-Dateien sind vorhanden
2. Konvertierungs-Script könnte hinzugefügt werden
3. Aktuell nicht im Scope — nach Diskussion

### GTFS ändert sich pro Jahr

**Wichtig:** Alle GTFS-Files haben eine **year-Dimension** (2023, 2024, 2025)

| Aspekt | Was sich ändert | Beispiel |
| :--- | :--- | :--- |
| Liniennummern | Selten | 2024: L2, L3, L8, L11, L13, L14, L15 — 2025: gleich |
| Streckenplan (shapes) | Gelegentlich | Umbauten, Baustellen, neue Haltestellen |
| Haltestellen (stops) | Regelmäßig | +/- Provisorische Halte während Baustellen |
| Fahrtplan (trips) | Täglich | Fahrplanwechsel 2× pro Jahr |

**Best Practice:** Immer `year` filtern beim Join mit GTFS

```python
# Falsch:
master.join(gtfs_trips, on='trip_id')  # Mismatches zwischen Jahren

# Richtig:
master = master.with_columns(
    pl.col('operating_date').dt.year().alias('year')
)
master.join(
    gtfs_trips.with_columns(pl.col('year')),
    on=['trip_id', 'year'],
    how='left'
)
```

### BPUIC vs. SLOID

**BPUIC** (6–7 Ziffern, z.B. `8590805`):
- IST-Daten verwenden BPUIC
- `gtfs_stops_lookup.parquet` nutzt BPUIC als Schlüssel
- Haltestellen-Kennziffer der Schweizer Verkehrsbetriebe

**SLOID** (Format `ch:1:sloid:90805::0`):
- GTFS Standard-Format
- `gtfs_tram_stops.parquet` nutzt SLOID
- Müsste extrahiert werden für direkten Join

**Join-Strategie:** Über `gtfs_stops_lookup` (BPUIC) — SLOID ist nicht nötig

---

## 4. Master-Schema (26 Spalten)

### Spalten nach Kategorie

#### Zeitstempel & Fahrt

| Spalte | Typ | Nullable | Beschreibung |
| :--- | :--- | :---: | :--- |
| `operating_date` | Date | ❌ | Betriebstag (eindeutig pro Fahrt) |
| `trip_id` | Utf8 | ❌ | Fahrt-Identifier (`FAHRT_BEZEICHNER`) — eindeutig pro Fahrt + Betriebstag |
| `arrival_schedule` | Datetime | ⚠️ 0.15% | Soll-Ankunftszeit (für Delays und Tageszeit-Analyse) |
| `departure_schedule` | Datetime | ⚠️ 0.15% | Soll-Abfahrtszeit |
| `stop_sequence` | Int16 | ❌ | Reihenfolge des Halts im Trip (1-basiert) |

#### Linie & Haltestelle

| Spalte | Typ | Nullable | Beschreibung |
| :--- | :--- | :---: | :--- |
| `line_name` | Categorical | ❌ | Tramliniennummer ("2", "11", "13", etc.) |
| `bpuic` | Int32 | ❌ | Haltestellen-ID (Join-Schlüssel mit GTFS) |
| `stop_name` | Categorical | ⚠️ 0.10% | Haltestellenname (via GTFS Join) |
| `stop_lat` | Float32 | ⚠️ 0.10% | Breitengrad WGS84 |
| `stop_lon` | Float32 | ⚠️ 0.10% | Längengrad WGS84 |
| `district_nr` | Int8 | ⚠️ 6.87% | Stadtkreis 1–12 (null = außerhalb Zürich Stadtgebiet) |
| `district_name` | Categorical | ⚠️ 6.87% | Stadtkreisname ("Kreis 1", "Kreis 11", etc.) |

#### Verspätungen (delays)

| Spalte | Typ | Nullable | Beschreibung |
| :--- | :--- | :---: | :--- |
| `arrival_delay` | Float32 | ❌ | Verspätung Ankunft in Sekunden (positiv = verspätet) |
| `departure_delay` | Float32 | ❌ | Verspätung Abfahrt in Sekunden |
| `canceled` | Boolean | ❌ | Fahrt ausgefallen (True = Ausfall) |

#### Wetterdaten (stündlich)

| Spalte | Typ | Nullable | Beschreibung |
| :--- | :--- | :---: | :--- |
| `temperature` | Float32 | ⚠️ 0.35% | Temperatur °C (UGZ Stampfenbachstrasse) |
| `humidity` | Float32 | ⚠️ 0.35% | Luftfeuchtigkeit % |
| `rain_duration` | Float32 | ⚠️ 0.35% | Regendauer min/h |
| `precipitation` | Float32 | ⚠️ 0.35% | Niederschlag mm (konsolidiert: Stampe + Mythenquai) |
| `wind_speed` | Float32 | ⚠️ 0.35% | Windgeschwindigkeit km/h |
| `global_radiation` | Float32 | ⚠️ 0.35% | Globalstrahlung W/m² |
| `flood_intensity` | Int16 | ⚠️ 0.15% | Hochwasser-Indikator (0 = normal) |

#### Event-Daten

| Spalte | Typ | Nullable | Beschreibung |
| :--- | :--- | :---: | :--- |
| `event_name` | Categorical | ⚠️ 78.55% | Name des Events ("Neujarstag", "Ironman Zurich", etc.) |
| `event_type` | Categorical | ⚠️ 78.55% | Kategorie ("Feiertag", "Fussball", "Konzert", etc.) |
| `event_size` | Int8 | ⚠️ 78.55% | Gewichtung: 1=mittel, 2=hoch, 3=sehr hoch |
| `event_location` | Categorical | ⚠️ 78.55% | Veranstaltungsort |

**Hinweis:** Event-Spalten sind "null" für 78.55% der Zeilen (kein Event an dem Tag). Das ist normal und erwartet.

### Datentyp-Optimierungen

| Datentyp | Wahl | Grund |
| :--- | :--- | :--- |
| **Float32 vs. Float64** | Float32 | Halbiert RAM-Bedarf bei ausreichender Präzision für Delays/Wetter |
| **Int32 vs. Int64** | Int32 für `bpuic` | Ausreichend für Wertebereich, spart Platz |
| **Categorical** | Für Strings die <100 Unique-Werte haben | Massive Speicherersparnis bei `line_name`, `stop_name`, etc. |
| **Date vs. Datetime** | Date für `operating_date` | 4 Bytes statt 8, und schnellere Tageszeit-Operationen |
| **Int8/Int16 vs. Int64** | Int8 für district, Int16 für stop_sequence | Nutzt minimalen Wertebereich |

### Null-Quoten

| Spalte | Null-Anteil | Ursache |
| :--- | :---: | :--- |
| `event_*` | 78.55% | Normal — die meisten Tage haben keine Events |
| `district_nr` / `district_name` | 6.87% | Haltestellen außerhalb Stadtgebiet |
| `temperature`, `humidity`, `precipitation`, etc. | 0.35% | Wenige Stunden ohne Meteo-Match (bei Zeitumstellung) |
| `arrival_schedule`, `departure_schedule` | 0.15% | Fehlerhafte Zeitstempel in Rohdaten |
| `stop_name`, `stop_lat`, `stop_lon` | 0.10% | BPUIC-IDs die nicht in GTFS vorhanden sind (sehr selten) |

---

## 5. Gotchas & Bekannte Tücken

### 1. stop_sequence ist chronologisch, nicht kausal

**Problem:** `stop_sequence` folgt der **geplanten** Reihenfolge (Soll-Ankunftszeit), nicht der tatsächlichen.

**Beispiel:**
```
Eine Fahrt kommt mit großer Verspätung an — überschreitet aber nicht die geplante Reihenfolge
Stop 1 (Soll 10:00) → tatsächlich 10:45 
Stop 2 (Soll 10:05) → tatsächlich 10:30  ← kommt VOR Stop 1 an, aber stop_sequence=2
```

**Implikation:** Wenn du die **tatsächliche** Reihenfolge brauchst (z.B. für Umsteige-Analysen), sortiere nach `arrival_schedule` (Soll), nicht nach tatsächlicher Ankunft.

**Best Practice:** Immer nach `arrival_schedule` sortieren für Analysen auf Fahrt-Ebene.

### 2. GTFS ändert sich pro Jahr

**Problem:** Linien, Routen und Haltestellen können sich zwischen Jahren unterscheiden.

**Beispiel:**
```
2024: Linie L11 mit Haltestelle "Bellevue"
2025: Linie L11 bekommt Umleitungs-Haltestelle "Bellevue Temp"
```

**Best Practice:**
- Filtere immer `year` beim Arbeiten mit GTFS-Daten
- Nutze `operating_date.year()` um Jahrgänge zu trennen
- Dokumentiere welche GTFS-Version (Jahr) du nutzt

### 3. Kurs-Varianten (z.B. L17a/L17b)

**Problem:** Manche Linien haben mehrere `shape_id` pro `direction_id` (unterschiedliche Routen an unterschiedlichen Tagen).

**Beispiel:**
```
Linie 11:
- shape_id 1: Hauptstrecke (täglich)
- shape_id 2: Umleitungs-Route (während Baustelle)
```

**Best Practice:**
Wenn du die dominanteste Route brauchst:
```python
df_trip = df.group_by('shape_id').agg(pl.len()).sort('len', descending=True)
dominant_shape = df_trip[0, 'shape_id']
```

### 4. Fahrtrichtung ist mehrdeutig

**Problem:** `direction_id` ist generisch (0 oder 1), nicht aussagekräftig. `trip_headsign` ist aussagekräftig aber nicht normalisiert.

**Beispiel:**
```
Linie 11:
- direction_id = 0 → trip_headsign = "Flughafenplatz"
- direction_id = 1 → trip_headsign = "Hauptbahnhof"

ABER: Textabweichungen möglich ("Flughafen-Platz", "HB Zürich", etc.)
```

**Best Practice:** Nutze **beide** Spalten für Richtungs-Analyse:
```python
direction_lookup = {
    ('L11', 0): 'outbound',  # zu Flughafen
    ('L11', 1): 'inbound',   # zu HB
}
```

### 5. stop_times.parquet fehlt — absichtlich

**Situation:** Raw-Files existieren (`data/raw/vbz/gtfs/*/stop_times.txt`), wurden aber nicht zu Parquet konvertiert.

**Grund:**
- `stop_sequence` wird aus **IST-Daten** berechnet (bessere Lösung)
- GTFS stop_times ist redundant
- Spart ~1 GB Speicher

**Wenn du stop_times brauchst:**
1. Konvertierungs-Script könnte hinzugefügt werden
2. Dokumentiere dazu den konkreten Use-Case
3. Alle 3 Jahre (2023, 2024, 2025) konvertieren

---

## 6. Quality Checks (Validierung)

**Notebook:** `notebooks/vbz/vbz-data-master-validation.ipynb`

8 automatisierte Checks wurden durchgeführt:

1. ✅ **Schema**: Alle 26 Spalten vorhanden, korrekte Datentypen
2. ✅ **Abdeckung**: Kein unerwarteter Datenverlust durch Joins
3. ✅ **Wertebereiche**: Delays, Temperaturen, Koordinaten im erwarteten Bereich
4. ✅ **Nulls**: Null-Quoten entsprechen Erwartungen (siehe Sektion 4)
5. ✅ **Join-Qualität**: <1% ungematchte BPUIC, Meteo, Events
6. ✅ **Cross-Check**: Verifizierung der Beziehungen (z.B. stop_sequence monoton pro Trip)
7. ✅ **Business-Logik**: Delays korrekt berechnet, Ausfälle plausibel
8. ✅ **Zusammenfassung**: Master ist production-ready

---

## 7. Reproduzierbarkeit

### Alles von Anfang neu aufbereiten

```bash
# 1. IST-Daten neu herunterladen (optional)
# vbz-ist-daten.ipynb → "Initialer Download" laufen lassen

# 2. IST-Daten filtern & parquetisieren
# vbz-ist-daten.ipynb → "Filterung & Parquet-Konvertierung" laufen lassen
# src/process_ist_daten.py wird aufgerufen

# 3. GTFS aufbereiten (meist nicht nötig)
# vbz-gtfs-data.ipynb → einmal durchlaufen

# 4. Wetterdaten konsolidieren
# vbz-meteo-data.ipynb → einmal durchlaufen

# 5. Event-Kalender aktualisieren (manuell)
# events-master.csv editieren wenn neue Events nötig sind

# 6. Master-Merge durchführen
# vbz-data-master-preparation.ipynb → einmal durchlaufen
# Ergebnis: data/interim/vbz/vbz_master.parquet

# 7. Validierung
# vbz-data-master-validation.ipynb → einmal durchlaufen
```

### Resume-Punkte

**`src/process_ist_daten.py`** ist resume-fähig:
- Arbeitet Datei-für-Datei
- Überspringt bereits verarbeitete Parquets
- Ideal für bei Fehlern neu zu starten

---

## 8. Kontakt & Weitere Fragen

**Fragen zu dieser Dokumentation?**
→ Siehe `PROCESS_LOG.md` für detailliertes Projektjournal
→ Siehe Notebooks für vollständigen Code und Erklärungen
→ Memory: `~/.claude/projects/-Users-kaywiegand-Workspace/memory/sf_data_research_documentation.md`
