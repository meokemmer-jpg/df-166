# df-166 — PRODUKTION (codex-5.5) [CRUX-MK]
*2026-06-09T11:07:35.481600+00:00 | codex-5.5 | via codex-5.5*

# df-166 — LexVance Audit Hours Tracker

## Zweck

`df-166` steuert die Audit-Stunden von LexVance so, dass Familie Kemmer täglich sieht, wo abrechenbare Leistung entsteht, wo Fristen kippen und wo Mandantenlast Marge oder Vertrauen gefährdet.

## Aktueller Stand

- Offene Audits: `14`
- Monatsstunden: `428,5`
- Durchschnitt je Audit: `30,61` Stunden
- Deadline-Breaches: `1`
- Top-Mandanten: `Meyer & Co`, `NordTax GmbH`, `Rhein Ledger AG`
- Status: `Gelb`

Der aktuelle Breach entspricht `7,1 %` des offenen Bestands. Das ist steuerbar, aber nicht ignorierbar.

## Tagessteuerung

1. `08:00 UTC`: Stundenlauf aktualisieren.
2. `08:10 UTC`: Top-Mandanten gegen Fristen prüfen.
3. `08:20 UTC`: Abweichungen notieren: neue Audits, neue Breaches, Stundenanstieg.
4. `16:00 UTC`: Kontrolllauf für Nachbuchungen und Terminänderungen.

## Ampellogik

- Grün: `0` Breaches, maximal `28,0` Stunden je Audit, kein Mandant über `35 %` Lastanteil.
- Gelb: `1` Breach oder `28,01-32,0` Stunden je Audit.
- Rot: `>=2` Breaches oder mehr als `32,0` Stunden je Audit oder `5+` Audits mit gleicher Fälligkeit binnen `72` Stunden.

## 7-Tage-Plan

### Tag 1: Bestand sortieren

Alle `14` Audits werden nach Frist gruppiert: `<=7 Tage`, `8-14 Tage`, `>14 Tage`. Je Audit werden Stundenstand, Owner und nächster Arbeitsschritt ergänzt.

### Tag 2: Breach klären

Der vorhandene Breach bekommt genau eine Ursache: verspätete Unterlagen, interne Übergabe, Aufwandsschätzung, fehlende Freigabe oder Qualitätsnacharbeit.

### Tag 3: Top-Mandanten begrenzen

Für `Meyer & Co`, `NordTax GmbH` und `Rhein Ledger AG` gilt maximal `2` parallele Hauptstränge je Mandant. Das reduziert Kontextwechsel und schützt Durchlaufzeit.

### Tag 4: Stunden prüfen

Alle Buchungen über `4,5` Stunden ohne Zwischenstatus werden geprüft. Ziel ist saubere Trennung zwischen produktiver Audit-Arbeit, Suchzeit und Wartezeit.

### Tag 5: Fristtafel schließen

Jedes Audit erhält genau einen Owner und genau ein nächstes Datum. Fälle ohne Owner oder Datum gelten als Governance-Lücke.

### Tag 6: Monatsprojektion rechnen

Formel: `428,5 / 9 x 30 = 1.428,3` projizierte Monatsstunden bei linearem Verlauf zum 30-Tage-Monat. Diese Zahl wird gegen Teamkapazität, Rechnungslauf und Mandatsbudget gespiegelt.

### Tag 7: Eigentümer-Review

Das Wochenreview für Familie Kemmer enthält nur sechs Zahlen: offene Audits, Breaches, Monatsstunden, Stunden je Audit, Top-3-Lastanteil, Audits mit Frist `<=7 Tage`.

## Eskalation

Stufe A greift bei `1` neuem Breach, über `30,0` Stunden je Audit oder mehr als `3` Audits mit Frist `<=5 Tage`: Tagesumverteilung und Nebenaufgabenstopp.

Stufe B greift bei `2` Breaches im Monat, Top-3-Last über `65 %` oder Stundenanstieg über `12 %` binnen `7` Tagen: Kapazität und Scope-Creep prüfen.

Stufe C greift bei wiederholten Breaches über `2` Wochen oder Margenerosion: Eigentümerentscheidung zu Kapazität, Mandatsselektion oder Preisanpassung.

## Wert für Familie Kemmer

`df-166` macht Audit-Arbeit führbar. Aus einzelnen Stundenbuchungen wird ein Lagebild für Cashflow, Marge, Personalsteuerung und Mandantenrisiko. Der unmittelbare rho-Wert liegt darin, dass Familie Kemmer nicht erst am Monatsende erkennt, ob Leistung profitabel, fristgerecht und abrechenbar war. Die Steuerung erfolgt täglich, mit klaren Schwellen und konkreten Eingriffspunkten.