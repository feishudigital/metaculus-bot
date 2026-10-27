# STATE — Metaculus-Prognose-Bot

**Stand:** 2026-10-28 · Bot vorbereitet, noch nicht live

## Was es ist
Fork von `Metaculus/metac-bot-template` als `feishudigital/metaculus-bot` (öffentlich).
Läuft per GitHub Actions im FutureEval-Bot-Wettbewerb (Herbst 2026) und in der MiniBench.
Hintergrund, Regeln, Preisgeld: Memory `reference-passiv-ki-trading-optionen-2026-10`.

## Aufbau (Commit c7b73bb)
- Recherche: Claude Sonnet 5.5 mit Websuche (max. 5 Suchen je Frage, über litellm `web_search_options`).
- Prognose: 3× Claude Opus 5.5 (Effort medium), veröffentlicht wird der Median.
- Parser/Zusammenfassung: Claude Haiku 5.5.
- Kostendeckel `budget.py`: Kostenbuch `kosten.json` (je Monat, vom Workflow zurück-committet).
  Ab 70 $ prognostiziert Sonnet statt Opus, ab 85 $ setzt der Bot bis Monatsende aus. Budget 100 $/Monat.
- Workflows Tournament + Test teilen die Warteschlange `bot-cost-ledger`. Der Bot-Job hat nur Leserechte;
  das Kostenbuch kommt als Artefakt in den Job `save_ledger` (einziger mit Schreibrecht, committet auf main).

## Offen
1. Kevin: `gh auth refresh -h github.com -s workflow`, dann Push (Commits c7b73bb..HEAD).
2. Direkt nach dem Push: Workflows „Forecast on new AI tournament questions“ und „Metaculus Cup“ deaktivieren
   (Cup bringt Bots kein Preisgeld und kostet nur).
3. Kevin: Secrets `METACULUS_TOKEN` + `ANTHROPIC_API_KEY` im Repo anlegen.
4. Test Bot (bot-testing-area) laufen lassen: echte Kosten je Frage messen, alle Fragetypen prüfen.
5. Erst danach Tournament-Workflow aktivieren. Nur die ERSTE MiniBench zählt für Leistungsgutschriften.

## Fallen
- forecasting-tools 0.3.5 lässt `temperature` automatisch weg, wenn ein Modell ihn ablehnt; trotzdem nie setzen.
- litellm 1.105.1 kennt die Preise der 5.5-Modelle und zählt Websuche mit 0,01 $ je Suche.
- Gratis-LLM-Guthaben von Metaculus ist für die Herbstsaison geschlossen; neuer Antrag ein paar Wochen vor Januar.
