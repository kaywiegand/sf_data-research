## Datenwörterbuch — Stadtkreise Zürich (GeoJSON)

Dieses Wörterbuch beschreibt die Attribute der geografischen Grenzen der 12 Zürcher Stadtkreise. Diese Daten sind essenziell für räumliche Analysen und Visualisierungen (Choroplethenkarten).

| Attribut | Datentyp | Beschreibung | Beispiel |
| :--- | :--- | :--- | :--- |
| **knr** | Integer | **Kreisnummer:** Eindeutiger Identifikator für den Stadtkreis (1 bis 12). | `9` |
| **kname** | String | **Kreisname:** Offizielle Bezeichnung des Stadtkreises. | `"Kreis 9"` |
| **objid** | Integer | **Objekt-ID:** Interne Kennung des Datensatzes im GIS-System der Stadt Zürich. | `42` |
| **geometry** | Polygon | **Geometrie:** Enthält die Koordinatenpunkte (WGS84 oder LV95), die die Grenze des Kreises definieren. | `[[[268..., 124...], ...]]` |

**Hinweise zur Verwendung:**
* **Join-Key:** Die Spalte `knr` ist der primäre Schlüssel, um Wetter- oder Tramdaten auf Kreisebene zu aggregieren.
* **Hierarchie:** Ein Stadtkreis besteht aus mehreren statistischen Quartieren. Für feinere Analysen sollte der Datensatz "Statistische Quartiere" verwendet werden.
* **Visualisierung:** In Python (GeoPandas) wird die Spalte `geometry` automatisch erkannt, um Karten zu plotten.