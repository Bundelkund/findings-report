# Mission: findings-report

> Die Triage der Factory liest diese Datei frisch von `main`. Die Factory darf sie nie aendern; Aenderungen nur von
> Hand per PR mit Freigabe des Repo-Inhabers.

## Zweck

Kleines Kommandozeilen-Werkzeug: es wandelt einen strukturierten Pruefbericht (eine JSON-Datei mit Titel, Urteil
und einer Liste von Befunden) in **eine** lesbare, selbstenthaltene HTML-Seite. Die Seite oeffnet man im Browser
ohne Server und ohne Internet; sie zeigt Urteil, Zusammenfassung und Befunde nach Schwere geordnet.

## Nutzer

- Menschen, die Pruefberichte lesen (Code-Reviews, Audits, Checklisten) und eine Seite statt rohem JSON wollen.
- Programme, die einen Bericht als JSON schreiben und das Werkzeug danach aufrufen
  (`python -m findings_report <bericht.json> [ausgabe.html]`).
- Der Repo-Inhaber (Konto Bundelkund) als einziger Auftraggeber: er schreibt die Issues und liest die PRs.

## Ziele (was angenommen wird)

- Das Eingabeformat beschreiben und pruefen: Pflichtfelder, erlaubte Werte (z.B. Schwere CRITICAL, HIGH, MEDIUM,
  LOW, INFO; Urteil pass, warn, fail), klare Fehlermeldung mit Exit-Code ungleich 0 bei ungueltiger Eingabe.
- Die HTML-Ausgabe: Kopf mit Titel und Urteil, Zusammenfassung, Befund-Liste, optionale Tabelle, eingebettetes CSS,
  hell und dunkel lesbar, zugaenglich (Ueberschriften-Reihenfolge, Kontrast, keine Information nur ueber Farbe).
- Ein kleiner, eng begrenzter Markdown-Teil fuer Textfelder (Absaetze, Listen, Fett, Code), der vorher escaped.
- Kommandozeile, Tests und Doku dieses Werkzeugs.
- Jede Aufgabe ist in einer Dev-Runde loesbar und durch Akzeptanzkriterien pruefbar (eigene Tests unter
  `factory/tests/test_<issue>_*.py`).

## Feste Leitplanken

- Python >= 3.12, nur Standardbibliothek: keine Abhaengigkeiten, keine `requirements.txt`, kein Paket-Upload.
- Ein Lauf liest genau eine Eingabedatei und schreibt genau eine HTML-Datei (oder stdout); sonst nichts.
- Kein Netzwerk: keine Downloads, keine API-Aufrufe, kein Nachladen externer Skripte, Stylesheets, Schriften oder
  Bilder in der erzeugten Seite. Alles, was die Seite braucht, steht in ihr.
- Jeder Text aus der Eingabe wird vor der Ausgabe vollstaendig HTML-escaped (auch Attribute und Links);
  die Seite enthaelt kein JavaScript, das Eingabedaten ausfuehrt.

## Nicht-Ziele (wird abgelehnt)

- Netzwerkzugriffe jeder Art, auch zur Laufzeit der erzeugten Seite (CDN, Web-Schriften, Tracking, Analytics).
- Neue Abhaengigkeiten, Paketinstallation, Build-Werkzeuge, Bundler, Frameworks.
- Ein Server, eine Web-App, eine Datenbank, mehrere Ausgabedateien oder ein Ausgabe-Verzeichnis je Lauf.
- Ausfuehren von Eingabedaten (`eval`, `exec`, `subprocess`, Vorlagen-Sprachen mit Code) und ungeescapte Ausgabe.
- Lesen oder Schreiben von Dateien ausser der einen Eingabe- und der einen Ausgabedatei.
- Nutzerdaten sammeln, speichern oder weitergeben; Veroeffentlichung, Releases, Pakete, Deploy.
- Aenderungen an der Factory selbst: `factory/MISSION.md`, `factory/RULES.md`, `.github/`, CI, Lizenz.
