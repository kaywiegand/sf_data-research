import os
from pathlib import Path
from IPython.display import Markdown, display

# Wir definieren das Projekt-Root-Verzeichnis relativ zu dieser Datei
# Angenommen doc_loader.py liegt in /src/
# .parent ist /src/, .parent.parent ist das Root-Verzeichnis (sf_data-research)
ROOT_DIR = Path(__file__).resolve().parent.parent

DOC_PATHS = {
    "meteo":        "data/interim/vbz/meteo/meteo-master.md",
    "events":       "data/interim/vbz/events/events-master.md",
    "ist_daten":    "data/interim/vbz/ist-daten/ist-daten.md",
    "gtfs":         "data/interim/vbz/gtfs/gtfs.md",

    "geo":          "data/raw/vbz/geo/geo.md",
    "event_subs":   "data/raw/vbz/events/event-subs.md",
    "gtfs_raw":     "data/raw/vbz/gtfs/gtfs.md",
    "meteo_erz":    "data/raw/vbz/meteo/erz/erz-ent.md",
    "meteo_wapo":   "data/raw/vbz/meteo/wapo/messwerte_wapo.md",
    "meteo_ugz":    "data/raw/vbz/meteo/ugz/ugz_ogd_meteo.md",
}

def show_doc(key):
    rel_path = DOC_PATHS.get(key.lower())
    
    if not rel_path:
        print(f"Fehler: Key '{key}' nicht gefunden.")
        return

    # Kombiniere Root mit dem relativen Pfad zum File
    abs_path = ROOT_DIR / rel_path

    if not abs_path.exists():
        print(f"Fehler: Datei nicht gefunden unter {abs_path}")
        # Debug-Hilfe: Zeige an, wo wir gerade suchen
        print(f"ROOT_DIR wurde erkannt als: {ROOT_DIR}")
        return

    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            display(Markdown(f.read()))
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")