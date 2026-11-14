# STATE — Metaculus-Prognose-Bot

**Stand:** 2026-11-14 · Prüfung: läuft sauber; forecasting-tools 0.3.5 → 0.3.7

## Was es ist
Fork von `Metaculus/metac-bot-template` als `feishudigital/metaculus-bot` (öffentlich).
Läuft per GitHub Actions im FutureEval-Bot-Wettbewerb (Herbst 2026) und in der MiniBench.
Hintergrund, Regeln, Preisgeld: Memory `reference-passiv-ki-trading-optionen-2026-10`.

## Aufbau (Commit c7b73bb)
- Recherche: Claude Sonnet 5.5 mit Websuche (max. 5 Suchen je Frage, über litellm `web_search_options`).
- Prognose: 3× Opus 5.5 im Hauptwettbewerb, 3× Sonnet in der MiniBench (Kevin 02.11.: Topf/Frage ~165 $ vs. ~17 $), Median.
  MiniBench nur, solange 2 $ je Resttag unter der Sonnet-Schwelle fürs Hauptturnier frei bleiben (`budget.minibench_allowed`).
- Parser/Zusammenfassung: Claude Haiku 5.5.
- Kostendeckel `budget.py`: Kostenbuch `kosten.json` (je Monat, vom Workflow zurück-committet).
  Kevin 28.10.: Der Bot darf das ganze freie API-Guthaben nutzen (100 $/Monat, Reset am 1.), aber NIE darüber. Kein anderes Projekt nutzt die API zurzeit; ändert sich das, sagt Kevin Bescheid → Deckel senken.
  Deckel = Repo-Variable `BOT_MONTHLY_BUDGET_USD` (ohne Variable 95 $, Kevin 02.11.; 5 $ Reserve für Zählfehler);
  `BOT_BUDGET_MONTH_OVERRIDE` = „JJJJ-MM=Betrag“ gilt nur für diesen einen Monat. Ab 80 % Sonnet statt Opus,
  am Deckel setzt der Bot bis Monatsende aus. Das Kostenbuch kennt nur die Bot-Kosten.
- Nur die Prognose-Jobs (Tournament + Test) teilen die Warteschlange `bot-forecast` (max. 180 min; seit 02.11., weil am
  30.10. ein hängender save_ledger 24 h alles blockierte → 4 Fragen verpasst). Der Bot-Job hat nur Leserechte und
  checkt immer die Spitze von main aus. Er übergibt nur die eigenen Laufkosten (`run_cost.json`) als Artefakt an
  `save_ledger` (einziger Job mit Schreibrecht); der addiert sie auf `kosten.json` an der Spitze von main
  (`python3 budget.py merge-run-cost`, bis zu 3 Versuche). So überschreibt kein veralteter Stand neuere Summen.

## Offen
1. ✓ Secrets `METACULUS_TOKEN` + `ANTHROPIC_API_KEY`; Cup-Workflow aus (kein Bot-Preisgeld); Test nur von Hand.
2. Auslöser: Pi-Cron `3,33` (Dispatch-API, Kevins OK 02.11.), GitHub-Cron nur `47 */3` als Rückfall.
   Prüfung 14.11.: 279 von 281 Läufen 08.–14.11. grün (11.11.: 1× GitHub-Startfehler, 1× save_ledger
   abgebrochen ohne Kosten), Pi-Fehler nur 3× am 04./05.11. (HTTP 000/500). Hauptwettbewerb: 40 von 40
   neuesten Fragen beantwortet. Verpasst vor dem 02.11.: MiniBench 46368–46395, Haupt 46281 + 46285–46288.
3. Oktober 6,07 $, November 43,29 $ (14.11.); Hauptwettbewerb ~2,0 $/Tag (06.–14.11.). MiniBench pausiert seit
   05.11. (Reserve-Regel) → Hochrechnung ~77 $ am 30.11., ~18 $ unter dem Deckel ungenutzt. Vorschlag an Kevin
   (14.11.): Sonnet-Schwelle und MiniBench an Reserve statt fester 80 % koppeln. Voraussetzung: Console-Abgleich
   (02.11.: Console 3,51 $ vs. Kostenbuch 7,01 $; Nachprüfung vom 03.11. nie erfolgt) — Kevin liest ab.

## Fallen
- forecasting-tools 0.3.5 lässt `temperature` automatisch weg, wenn ein Modell ihn ablehnt; trotzdem nie setzen.
- Gratis-Guthaben von Metaculus: Herbst geschlossen, neuer Antrag wenige Wochen vor Januar.
- Fork: Zeitplan erst nach Klick „I understand my workflows…“ + Push auf main; zu viele Läufe → GitHub sperrt den Fork.
