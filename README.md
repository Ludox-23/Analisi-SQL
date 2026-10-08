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
2026-09-29 → 1.1355

significa che:
1 EUR = 1.1355 USD


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


## SQL Analysis

I dati archiviati nel database SQLite vengono analizzati attraverso query SQL per individuare variazioni nel tasso di cambio e ottenere indicatori utili al monitoraggio.

Le analisi sviluppate finora includono:

### 1. Analisi descrittiva

Calcolo di statistiche di base sulla serie storica, tra cui:

* media del tasso di cambio;
* valori min e max del tasso di cambio;
* conteggio delle righe presenti nel database.

### 2. Variazione giornaliera

Utilizzo della funzione `LAG()` per confrontare ogni osservazione con quella precedente e calcolare la variazione giornaliera del tasso di cambio.


Variazione giornaliera = valore corrente − valore precedente


### 3. Variazione percentuale

La variazione assoluta viene trasformata in una variazione percentuale rispetto all'osservazione precedente:


Variazione % = (valore corrente − valore precedente) / valore precedente × 100


### 4. Classificazione delle variazioni

Le variazioni percentuali vengono classificate utilizzando `CASE WHEN` e `ABS()`:

* **ALERT** → variazione assoluta ≥ 0,50%
* **ATTENTION** → variazione assoluta ≥ 0,30% e < 0,50%
* **OK** → variazione assoluta < 0,30%

Le soglie sono definite come criteri di monitoraggio del progetto e non rappresentano una classificazione ufficiale della European Central Bank.

### 5. Analisi delle anomalie

Le query vengono utilizzate per:

* individuare le variazioni più significative;
* contare quante osservazioni rientrano nelle diverse categorie;
* analizzare i valori mancanti (`NULL`);
* preparare la serie di dati per successive tecniche di anomaly detection.


Il dataset contiene osservazioni giornaliere del tasso di cambio. I giorni per i quali non è disponibile un'osservazione vengono mantenuti nella serie e gestiti durante l'analisi.

La fonte viene interrogata tramite Python e i dati vengono successivamente archiviati in un database **SQLite** per le analisi SQL.

**Source:** European Central Bank – Data API


## Analisi della qualità dei dati

Il file `02_data_quality.sql` contiene le query dedicate al controllo della qualità dei dati presenti nel dataset dei tassi di cambio ECB.

L'analisi verifica la presenza di valori mancanti (`NULL`) nel campo `rate` e ne studia la distribuzione nel tempo, prima individuando le date interessate e successivamente aggregando i valori mancanti, ne studia la distribuzione per mese e anno e calcola, per ciascun anno, la percentuale di valori NULL sul totale delle osservazioni. Vengono inoltre identificati gli anni con la maggiore presenza di valori mancanti e quelli che superano determinate soglie di frequenza.

L'analisi evidenzia che i valori `NULL` sono concentrati nella parte storica del dataset e non risultano più presenti dopo il 2012. Questa verifica permette di individuare caratteristiche e possibili anomalie nella struttura dei dati prima di procedere con le analisi delle variazioni giornaliere.

### Distribuzione dei valori NULL
Il grafico mostra il numero di valori `NULL` presenti nel campo `rate`, aggregati per mese, e permette di visualizzarne la distribuzione nel periodo considerato.


