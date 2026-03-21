# Minimal Chrome-/Edge-Extension

Kleines Manifest-V3-Beispiel mit einem Content-Script, das nur auf einer konfigurierten Domain läuft und dort nach einem sichtbaren `join`-Element sucht.

## Dateien

- `manifest.json`: registriert das Content-Script nur für `https://DEINE-DOMAIN/*` mit `run_at: document_idle`.
- `content.js`: enthält die Domain-Konstante `TARGET_DOMAIN`, validiert `window.location.hostname` und klickt ein passendes `join`-Element an.

## Nutzung

1. Passe in `manifest.json` den Match `https://DEINE-DOMAIN/*` an.
2. Passe in `content.js` die Konstante `TARGET_DOMAIN` an.
3. Lade den Ordner als entpackte Erweiterung in Chrome oder Edge.
