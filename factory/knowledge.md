# Wissen ueber dieses Repo

> Daten, keine Anweisungen. Schreibt nur die Factory (Vorarbeiter, F-12) per PR durch das Merge-Gate; neueste zuerst.
> Zeile: - #<issue> | <Datum> | <Kategorie> | <Fakt>

- #65 | 2026-10-25 | spec | Die Spec verlangt fuer den gueltigen Pruefbericht die Ausgabe 'Bericht gueltig: 3 Befunde', waehrend der bestehende Test test_ak1_valid_report_exit_code_and_output 'OK: 3 Befunde' erwartet; Spec und
- #53 | 2026-10-25 | spec | Die Zusammenfassungszeile hat bereits Tests, die feste Anzeigetexte je Schweregrad erwarten; die Akzeptanzkriterien zu den deutschen Anzeigetexten widersprechen diesen Tests und sind ohne Klärung
- #49 | 2026-10-24 | spec | Spec-Akzeptanzkriterien für die Ausgabeformatierung waren nicht pruefbar: Ein Grep-Kriterium auf englische Bestandteile war vage bzw. der verbotene String kam nie vor, daher blieb nach zwei
- #37 | 2026-10-24 | budget | Das Issue-Budget von 1,00 USD war nach etwa 1,05 USD verbraucht; Dev und Review verursachten dabei den größten Anteil der Kosten.
- #37 | 2026-10-24 | design | Die Erweiterung des Befund-Schemas um ein Feld ort entfernte im findings_report-Rendering und in der Validierung bestehende Funktionen; der Review blockierte das wiederholt.
- #37 | 2026-10-24 | test | Das optionale Feld 'ort' im Eingabeformat laesst bestehende Tests zur Zusammenfassung und Schweregrad-Zaehlung rot werden; diese Regression blieb auch nach mehreren Neuentwuerfen bestehen.
- #37 | 2026-10-24 | spec | Akzeptanzkriterien mit unscharfen Formulierungen wie 'Leerer Platzhalter' oder ungedeckten festen Pruefstrings sind nicht pruefbar; Requirement-Deckel von 2 Runden wurde erreicht, Spec braucht
- #18 | 2026-10-22 | modell-antwort | Das Testing-Modell gemini-2.5-flash liefert beim Schreiben der Tests wiederholt kein gueltiges JSON (ungueltige Steuerzeichen oder Escape-Sequenzen), sodass der Testing-Loop nach vier Versuchen ohne
- #4 | 2026-10-13 | budget | Das Issue-Budget von 1,0 USD ist im Repo-Ablauf schnell erreicht; Architektur und Anforderungsanalyse verbrauchen den größten Teil, wodurch der Lauf in den Needs-Human-Zustand kippt.
- #12 | 2026-10-13 | modell-antwort | Eine Spec-Antwort mit einem Akzeptanzkriterium-Text von 420 Zeichen wurde vom Schema abgelehnt, weil dieses Feld auf 1 bis 400 Zeichen begrenzt ist.
- #12 | 2026-10-13 | modell-antwort | Spec-Erzeugung für HTML-Pruefbericht-Issues scheiterte zweimal: Modellantwort war kein gueltiges JSON (abgeschnitten, Zeichenkette nicht geschlossen) bzw. ein Textfeld überschritt die Maximallänge
- #2 | 2026-10-13 | test | Die von der Testphase selbst geschriebenen Tests scheiterten in vier Versuchen an der eigenen Referenz (AK5 durchgehend rot); der Testing-Loop eskalierte ohne brauchbare Tests.
- #2 | 2026-10-13 | modell-antwort | Der Testing-Pruefer (google/gemini-3.6-flash) lieferte bei der Spec-Pruefung wiederholt HTTP 400 vom Modellaufruf, daher kein gueltiges Urteil ueber die Spec; das Issue blieb bei needs-human.
- #2 | 2026-10-13 | test | Die vom Testing-Schritt geschriebenen Tests scheiterten viermal in Folge bereits an der eigenen Referenzimplementierung, sodass keine brauchbare Testbasis für das Eingabeformat entstand.
- #2 | 2026-10-13 | test | Die Gegenprobe der selbst geschriebenen Tests gegen die eigene Referenz scheiterte bei allen fuenf Akzeptanzkriterien in beiden Versuchen; die Tests sind damit nicht brauchbar und der Testing-Loop
- #4 | 2026-10-13 | spec | Bei HTML-Berichtsaufgaben mit Kopf, Befund-Liste und CSS blieb eine Fachfrage offen, die das Modell nicht raten darf; der Requirement-Loop stoppt vor dem Dev-Lauf und braucht menschliche Klärung.
- #4 | 2026-10-13 | modell-antwort | Die Architektur-Antwort des Modells scheiterte zweimal am Schema, weil das Feld dateien.1.aenderung die erlaubte Laenge von 400 Zeichen ueberschritt; Beschreibungen fuer Aenderungen muessen knapp
