## Datenwörterbuch — Events-Master-Dataset

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **Datum** | datetime64[us] | Datum des Events (tagesgenau, keine Uhrzeit). Join-Schlüssel für Tram-IST-Daten über `dt.normalize()`. |
| **Event_Name** | str | Bezeichnung des Events. |
| **Typ** | str | Kategorie: Feiertag, Stadtfest, Konzert, Fachmesse, Kongress, Super League, Schweizer Cup, UEFA … |
| **Gewichtung** | float64 | Besucherintensität: 1 = Mittel (1k–10k), 2 = Hoch (10k–30k), 3 = Sehr hoch (>30k). |
| **Ort** | str | Veranstaltungsort / Stadtteil. |


> **EDA-Aufgaben:**    
* Binäres Feature `has_event` (0/1),    
* Kombination von Gewichtung und Typ als kategoriale Variable, Analyse Verspätung vs. Gewichtungsstufe.   

