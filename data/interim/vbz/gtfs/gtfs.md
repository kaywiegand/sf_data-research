### Datenwörterbuch: GTFS Datasets

> **Verwendung:** `gtfs_tram_*` und `gtfs_zurich_*` sind für Geo-Karten und Visualisierungen.
> Für den Join mit IST-Daten → `gtfs_stops_lookup` (Export C).

---

**gtfs_tram_routes.parquet**

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **route_id** | str | Technischer Schlüssel der Linie |
| **route_short_name** | str | Kundenrelevante Linienbezeichnung (`2`, `11`, …) |
| **route_long_name** | str | Vollständiger Linienname |
| **route_color** | str | Offizielle VBZ-Linienfarbe (Hex, ohne `#`) |
| **route_text_color** | str | Textfarbe auf Linienbadge (Hex) |
| **year** | str | Fahrplanjahr (`2023`, `2024`, `2025`) |

**gtfs_tram_stops.parquet** ← Geo-Karten, nicht für Master-Merge

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **stop_id** | str | Haltestellen-ID im SLOID-Format (`ch:1:sloid:90805::0`) — kein direkter Join mit BPUIC möglich |
| **stop_name** | str | Lesbarer Haltestellenname (`Zürich, Paradeplatz`) |
| **stop_lat** | float64 | Breitengrad (WGS84) |
| **stop_lon** | float64 | Längengrad (WGS84) |
| **stop_url** | str | URL mit eingebetteter BPUIC (`...&input=8590805&...`) |
| **location_type** | float64 | GTFS Standorttyp |
| **parent_station** | str | Übergeordnete Haltestelle |
| **year** | str | Fahrplanjahr |

**gtfs_tram_shapes.parquet**

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **shape_id** | str | ID des Linienverlaufs |
| **shape_pt_lat** | float64 | Breitengrad des Streckenpunkts |
| **shape_pt_lon** | float64 | Längengrad des Streckenpunkts |
| **shape_pt_sequence** | int64 | Reihenfolge der Punkte entlang der Strecke |
| **year** | str | Fahrplanjahr |

**gtfs_tram_trips.parquet**

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **trip_id** | str | Eindeutige Fahrt-ID |
| **route_id** | str | Verknüpfung zu `gtfs_tram_routes` |
| **shape_id** | str | Verknüpfung zu `gtfs_tram_shapes` |
| **year** | str | Fahrplanjahr |

---

**gtfs_stops_lookup.parquet** ← Master-Merge (Join mit IST-Daten)

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **bpuic** | str | Haltestellen-ID — Join-Schlüssel zu `BPUIC` in IST-Daten |
| **stop_name** | str | Lesbarer Haltestellenname (`Zürich, Paradeplatz`) |
| **stop_lat** | float64 | Breitengrad (WGS84) — Mittelwert aller Bahnsteigkanten |
| **stop_lon** | float64 | Längengrad (WGS84) — Mittelwert aller Bahnsteigkanten |

> 1 Zeile pro BPUIC · Referenzjahr 2024 · 199/199 VBZ-Tram-Stops matchen ✓