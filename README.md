# findings-report
Kleines Werkzeug: strukturierte Pruefberichte (JSON) als lesbare HTML-Seite. Wird von einer automatischen Software-Factory mitgepflegt.

## Was es ist

Ein Kommandozeilen-Werkzeug in Python (>= 3.12, nur Standardbibliothek). Es liest **eine** JSON-Datei mit einem
Pruefbericht (Titel, Urteil, Befunde nach Schwere) und schreibt **eine** selbstenthaltene HTML-Seite: kein Server,
kein Internet, keine nachgeladenen Skripte oder Schriften, jeder Text aus der Eingabe HTML-escaped.

Stand: Geruest. Die Funktionen entstehen Schritt fuer Schritt aus Issues (siehe `factory/MISSION.md`).

## Wie man es laeuft

```bash
python3 -m findings_report bericht.json              # Prüfen (Exit 0: OK: <n> Befunde)
python3 -m findings_report bericht.json bericht.html  # HTML erzeugen (Exit 0: OK: bericht.html)
python3 -m unittest -v factory/tests/test_*.py        # Tests
```

## Wie das Repo gepflegt wird

Eine automatische Software-Factory bearbeitet Issues dieses Repos: sie prueft jedes Issue gegen
`factory/MISSION.md` und `factory/RULES.md`, baut auf Zweigen `factory/<issue>`, schreibt eigene Tests unter
`factory/tests/test_<issue>_*.py` und oeffnet einen Pull Request. Gemergt wird nur, wenn die Pflicht-Checks
`factory-gate` und `factory-ci` gruen sind. Mission, Regeln und `.github/` aendert die Factory nie; das
geschieht nur von Hand.