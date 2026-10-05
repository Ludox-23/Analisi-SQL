# Automated Data Monitoring & AI Anomaly Analysis

## Descrizione

Progetto personale di analisi e monitoraggio automatico di dati finanziari, sviluppato per applicare in un contesto pratico competenze di **Python, SQL e analisi dei dati**.

Il progetto utilizza i dati giornalieri del cambio **EUR/USD** pubblicati dalla European Central Bank (ECB) e costruisce un flusso di lavoro che parte dall'acquisizione dei dati e arriva alla loro analisi e al rilevamento di variazioni significative.

L'obiettivo è sviluppare progressivamente un sistema in grado di:

* acquisire dati da una fonte esterna;
* archiviare i dati in un database SQLite;
* analizzare l'andamento storico attraverso SQL;
* calcolare variazioni giornaliere e percentuali;
* individuare variazioni che superano determinate soglie;
* classificare automaticamente i risultati;
* integrare successivamente strumenti di AI per supportare l'interpretazione delle anomalie.

Il progetto è in fase di sviluppo e verrà esteso progressivamente con nuove analisi e funzionalità di automazione.

## Data Source

I dati utilizzati nel progetto provengono dalla **European Central Bank (ECB)** attraverso la sua API ufficiale.

La serie analizzata è il cambio **EUR/USD**, espresso come numero di dollari statunitensi per 1 euro.

Ad esempio:

```text
2026-09-29 → 1.1355
```

significa che:

```text
1 EUR = 1.1355 USD
```

## Python: Data Acquisition & Storage

Python viene utilizzato per automatizzare le prime fasi del processo:

1. inviare una richiesta all'API della European Central Bank;
2. ricevere i dati relativi al cambio EUR/USD;
3. salvare la risposta originale in formato XML;
4. estrarre dalla risposta le date e i valori del cambio;
5. creare e aggiornare un database SQLite;
6. verificare il numero di osservazioni disponibili;
7. recuperare le osservazioni più recenti per le successive analisi.

La libreria `requests` viene utilizzata per effettuare la richiesta HTTP, mentre `xml.etree.ElementTree` permette di leggere e analizzare la struttura XML restituita dall'API.

Il database SQLite contiene attualmente una tabella `exchange_rates` con due colonne:

| Colonna | Tipo | Descrizione             |
| ------- | ---- | ----------------------- |
| `date`  | TEXT | Data dell'osservazione  |
| `rate`  | REAL | Tasso di cambio EUR/USD |

Il dataset contiene osservazioni giornaliere del tasso di cambio. I giorni per i quali non è disponibile un'osservazione vengono mantenuti nella serie e gestiti durante l'analisi.

La fonte viene interrogata tramite Python e i dati vengono successivamente archiviati in un database **SQLite** per le analisi SQL.

**Source:** European Central Bank – Data API
