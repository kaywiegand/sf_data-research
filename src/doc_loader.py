import os
from IPython.display import Markdown, display

# Konfiguration der Pfade (Single Source of Truth)
DOC_PATHS = {
    "meteo": "../../data/interim/vbz/meteo/meteo-master.md",
    "events": "../../data/interim/vbz/events/events-master.md"
}

def show_doc(key):
    """
    Lädt ein Markdown-Dokument basierend auf einem kurzen Key.
    """
    path = DOC_PATHS.get(key.lower())
    
    if not path:
        print(f"Fehler: Key '{key}' nicht gefunden. Verfügbar: {list(DOC_PATHS.keys())}")
        return

    if not os.path.exists(path):
        print(f"Fehler: Datei nicht gefunden unter {os.path.abspath(path)}")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            display(Markdown(f.read()))
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")