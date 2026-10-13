# Testing-Bericht Issue #12

- Urteil: **pass** · Dev-Runde 1 · Dev-Stand `9ad99c6`
- Tests geschrieben von `google/gemini-2.5-flash` aus den Akzeptanzkriterien des Issues (ohne Dev-Code)
- Ausgefuehrt je Test in einem Wegwerf-Container (Repo nur lesend, ohne Netz), Urteil auf dem Wirt; nachstellen im Repo-Wurzelverzeichnis:
  `for f in factory/tests/test_*.py; do python3 -m unittest -v "$f"; done`
- AK im Issue: 8 · Beweis-Stufe 3 = Test ausgefuehrt, Ausgabe zitiert

AK1 | pass | Stufe: 3 | Test: test_ak1_valid_report_generates_html | Ausgabe: test_ak1_valid_report_generates_html ... ok
AK2 | pass | Stufe: 3 | Test: test_ak2_page_contains_title_and_verdict | Ausgabe: test_ak2_page_contains_title_and_verdict ... ok
AK3 | pass | Stufe: 3 | Test: test_ak3_findings_sorted_by_severity_and_input_order | Ausgabe: test_ak3_findings_sorted_by_severity_and_input_order ... ok
AK4 | pass | Stufe: 3 | Test: test_ak4_summary_shows_finding_counts_per_severity | Ausgabe: test_ak4_summary_shows_finding_counts_per_severity ... ok
AK5 | pass | Stufe: 3 | Test: test_ak5_input_texts_are_html_escaped | Ausgabe: test_ak5_input_texts_are_html_escaped ... ok
AK6 | pass | Stufe: 3 | Test: test_ak6_template_contains_no_scripts_or_external_resources | Ausgabe: test_ak6_template_contains_no_scripts_or_external_resources ... ok
AK7 | pass | Stufe: 3 | Test: test_ak7_invalid_report_or_missing_input_file_exit_code_2 | Ausgabe: test_ak7_invalid_report_or_missing_input_file_exit_code_2 ... ok
AK8 | pass | Stufe: 3 | Test: test_ak8_single_file_call_and_argument_handling | Ausgabe: test_ak8_single_file_call_and_argument_handling ... ok

## Akzeptanzkriterien (Wortlaut aus dem Issue)

- AK1: Gültiger Bericht → Exit-Code 0, die Ausgabedatei existiert, und auf stdout steht genau eine Zeile `OK: <ausgabe.html>`.
- AK2: Die Seite enthält den Titel des Berichts und das Urteil.
- AK3: Die Befunde stehen in der Reihenfolge der Schwere `CRITICAL` vor `HIGH` vor `MEDIUM` vor `LOW` vor `INFO`; bei gleicher Schwere in Eingabereihenfolge.
- AK4: Die Zusammenfassung nennt für jede vorkommende Schwere die Anzahl der Befunde.
- AK5: Texte aus der Eingabe werden vollständig HTML-escaped: Ein Titel `<script>alert(1)</script>` erscheint als Text, die Seite enthält kein `<script`-Tag.
- AK6: Die Vorlage der Seite (alles, was nicht aus der Eingabe stammt) enthält kein <script, keine http://- und keine https://-Adresse und lädt nichts von außen. Prüfbar an einem Bericht, dessen Texte keine Adressen enthalten: Dann kommt weder <script noch http:// noch https:// in der Seite vor. Eingabetexte werden nur escaped (AK5) und sonst unverändert ausgegeben, auch mit Adresse.
- AK7: Ungültiger Bericht oder fehlende Eingabedatei → Exit-Code 2 mit derselben Meldung wie beim Prüfen, und es wird keine Ausgabedatei angelegt.
- AK8: Aufruf mit nur einer Datei prüft wie bisher (Exit-Code 0 und `OK: <Anzahl> Befunde`, keine Ausgabedatei). Ohne jedes Argument oder mit mehr als zwei Argumenten → Exit-Code 2 und eine Meldung, die den Aufruf `python -m findings_report <bericht.json> [<ausgabe.html>]` zeigt.
