## Datenwörterbuch — Events Quell-CSVs

Alle fünf Quelldateien haben identische Spaltenstruktur:

| Spalte | Dtype | Beschreibung |
| :--- | :--- | :--- |
| **Datum** | datetime64[us] | Datum des Events (tagesgenau). |
| **Event_Name** | str | Bezeichnung des Events. |
| **Typ** | str | Kategorie (Feiertag, Stadtfest, Konzert, Fachmesse, Kongress, Super League, …). |
| **Gewichtung** | int / float | Besucherintensität: 1 = Mittel, 2 = Hoch, 3 = Sehr hoch. |
| **Ort** | str | Veranstaltungsort / Stadt. |