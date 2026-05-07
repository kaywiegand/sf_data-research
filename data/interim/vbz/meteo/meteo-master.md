
## Datenwörterbuch — Meteo-Master-Dataset

| Spalte | Dtype | Einheit | Quelle | Beschreibung |
| :--- | :--- | :--- | :--- | :--- |
| **date_time** | datetime64[us] | — | UGZ | Zeitstempel, stündlich, CET, tz-naiv |
| **temperature** | float64 | °C | UGZ Stampfenbachstrasse | Lufttemperatur. Basis für `is_snow` in der EDA. |
| **humidity** | float64 | %Hr | UGZ Stampfenbachstrasse | Relative Luftfeuchtigkeit. |
| **air_pressure** | float64 | hPa | UGZ Stampfenbachstrasse | Luftdruck. |
| **rain_duration** | float64 | min | UGZ Stampfenbachstrasse | Niederschlagsdauer pro Stunde. |
| **global_radiation** | float64 | W/m² | UGZ Stampfenbachstrasse | Globalstrahlung (Sonneneinstrahlung). |
| **wind_direction** | float64 | ° | UGZ Stampfenbachstrasse | Windrichtung (0–360°). |
| **wind_speed** | float64 | m/s | UGZ Stampfenbachstrasse | Windgeschwindigkeit (skalar). |
| **wind_speed_vector** | float64 | m/s | UGZ Stampfenbachstrasse | Windgeschwindigkeit (Vektor). |
| **precipitation_mm** | float64 | mm | Wapo Mythenquai | Niederschlagsmenge, stündlich summiert. NaN wenn keine Wapo-Messung. |
| **flood_intensity** | int64 | Anzahl | ERZ | Summe Überschwemmungsmeldungen des Tages über alle Zonen. 0 = kein Ereignis. |

> **EDA-Aufgaben:**   
* `is_snow` (temperature < 1°C & rain_duration > 0),   
* `flood_alert` (Schwellenwert aus Verteilung),   
* Regen-Kategorien aus `precipitation_mm`.  