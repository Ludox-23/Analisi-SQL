print("ECB Data auto Monitoring Project")


# Importiamo le librerie necessarie:
# requests per scaricare i dati dall'API ECB
# sqlite3 per lavorare con il database SQLite
# ElementTree per leggere il file XML restituito dall'ECB
# Path per gestire in modo sicuro i percorsi dei file
import requests
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
# datetime per registrare data e ora dell'aggiornamento  inizio
from datetime import datetime


# Individuiamo automaticamente la cartella in cui si trova questo script.
# In questo modo il programma può trovare il database e salvare i file
# correttamente anche quando viene eseguito automaticamente da Windows.
BASE_DIR = Path(__file__).resolve().parent


# Definiamo la cartella in cui verranno salvati i log.
# La cartella "logs" si trova un livello sopra la cartella Python.
LOG_DIR = BASE_DIR.parent / "logs"
#base_dir porta alla cartella dei file e da lì py cerca logs


# Creiamo la cartella "logs" se non esiste già.
LOG_DIR.mkdir(exist_ok=True)


# Definiamo il percorso del file di log.
LOG_PATH = LOG_DIR / "update_log.txt"


# Definiamo il percorso del database SQLite e del file XML
# utilizzando la cartella dello script come punto di riferimento.
DB_PATH = BASE_DIR / "ecb_data.db"
XML_PATH = BASE_DIR / "ecb_data.xml"


# Apriamo la connessione al database SQLite
# e creiamo un cursore per eseguire le query SQL.
#Python sa esattamente dove si trova il database, indipendentemente da dove Windows avvia lo script, importante per task sheduler
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# URL dell'API ECB utilizzata per ottenere il tasso di cambio EUR/USD.
# Il valore indica quanti dollari statunitensi corrispondono a 1 euro.
url = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"


# Inviamo una richiesta all'API ECB per scaricare i dati aggiornati.
response = requests.get(url)


# Verifichiamo il codice di risposta HTTP.
# 200 significa che la richiesta è stata completata correttamente.
print("Status code:", response.status_code)


# Salviamo la risposta dell'API in un file XML.
# Il file viene salvato nella cartella del progetto Python.
with open(XML_PATH, "w", encoding="utf-8") as file:
    file.write(response.text)

print("Dati ECB salvati in ecb_data.xml")


# Convertiamo il contenuto XML ricevuto dall'API
# in una struttura che Python può analizzare.
root = ET.fromstring(response.text)


# Cerchiamo tutte le osservazioni presenti nel file XML.
# Ogni osservazione contiene una data e il relativo tasso di cambio.
observations = root.findall(".//{*}Obs")

print("Numero osservazioni:", len(observations))

#fino a qui i dati vengono scaricati e letti, serve aggiornare il database data.db


#estrazione dati dall'XML per convertirli in PY e renderli leggibili da SQL
# Creiamo una lista vuota in cui salveremo le osservazioni
# nel formato (data, tasso di cambio).
data = []


# Analizziamo ogni osservazione presente nel file XML.
for obs in observations:

    # Estraiamo la data dell'osservazione.
    date = obs.find("{*}ObsDimension").attrib["value"]

    # Estraiamo il valore del tasso di cambio.
    value = obs.find("{*}ObsValue").attrib["value"]

    # Convertiamo il valore da testo (stringa) a numero decimale (float)
    # per poter effettuare successivamente calcoli e analisi.
    rate = float(value)

    # Aggiungiamo data e tasso alla lista.
    data.append((date, rate))


# TEST: Mostriamo a video le prime 5 osservazioni estratte
# per verificare che la lettura dei dati sia corretta.
print("Prime 5 osservazioni:")
print(data[:5])


#parte che aggiorna il database.
#diversamente dall'altro codice, non si sovrascrieve ma controlliamo le date già presenti e inseriamo solo quelle nuove.
# Creiamo la tabella se non esiste già.
# La tabella contiene la data dell'osservazione e il relativo tasso di cambio.
cursor.execute("""
CREATE TABLE IF NOT EXISTS exchange_rates (
    date TEXT,
    rate REAL
)
""")


# Recuperiamo dal database tutte le date già presenti.
# Servono per distinguere i dati già registrati dalle nuove osservazioni.
cursor.execute("SELECT date FROM exchange_rates")

existing_dates = {
    row[0] for row in cursor.fetchall()
}


# Selezioniamo solamente le osservazioni che non sono ancora presenti nel database.
new_data = [
    row for row in data
    if row[0] not in existing_dates
]


# Inseriamo nel database solamente le nuove osservazioni.
cursor.executemany(
    "INSERT INTO exchange_rates (date, rate) VALUES (?, ?)",
    new_data
)


# Salviamo definitivamente le modifiche al database.
conn.commit()


# Mostriamo quante nuove osservazioni sono state aggiunte.
print("Nuove osservazioni inserite:", len(new_data))


# Chiudiamo la connessione al database
# dopo aver completato l'aggiornamento.
conn.close()

print("Aggiornamento database completato.")


# Registriamo data e ora dell'esecuzione dello script.
# datetime.now() restituisce la data e l'ora locali del computer.
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Creiamo il messaggio che verrà salvato nel file di log.
log_message = (
    f"{update_time} - Aggiornamento completato | "
    f"Osservazioni scaricate: {len(observations)} | "
    f"Nuove osservazioni: {len(new_data)}\n"
)


# Apriamo il file di log in modalità append ("a").
# In questo modo non cancelliamo le esecuzioni precedenti:
# ogni nuovo aggiornamento viene aggiunto alla fine del file.
with open(LOG_PATH, "a", encoding="utf-8") as log_file:
    log_file.write(log_message)


# Mostriamo a video il messaggio appena registrato.
print("Log aggiornato.")


# datetime per registrare data e ora dell'aggiornamento fine

#per rendere automatico va impostato windows per eseguire lo script ogni giorno ad un orario specifico 
#start>utilità di pianificazione (wind+R)> taskschd.msc  > crea utilità di base > inserimento nome > trigger: ogni giorno, orario> 
# azione da eseguire: avvio programma > Nel campo Programma/script dobbiamo mettere il percorso dell'interprete Python
# (Per sapere qual è nel terminale di VS Code esegui:python -c "import sys; print(sys.executable)")

#cosa inserire in Campo	 e Valore
#Programma/script	C:\Users\ludov\AppData\Local\Python\pythoncore-3.14-64\python.exe
#Aggiungi argomenti	"C:\Users\ludov\OneDrive\Desktop\automated-data-monitoring\Python\ecb_automated_vers_data.py"
#Avvia in	C:\Users\ludov\OneDrive\Desktop\automated-data-monitoring\Python
