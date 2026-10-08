#Codice con righe di controllo 

print("ECB Data Monitoring Project")

import requests
import sqlite3
import xml.etree.ElementTree as ET


# Connessione al database
conn = sqlite3.connect("ecb_data.db")
cursor = conn.cursor()


# URL API ECB
url = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"

response = requests.get(url)

print("Status code:", response.status_code)


# Salvataggio della risposta XML
with open("ecb_data.xml", "w", encoding="utf-8") as file:
    file.write(response.text)

print("Dati salvati in ecb_data.xml")
print("Dimensione file:", len(response.text), "caratteri")


# Lettura XML
root = ET.fromstring(response.text)

observations = root.findall(".//{*}Obs")

print("Numero osservazioni:", len(observations))


# Controllo delle prime 5 osservazioni
for obs in observations[:5]:
    date = obs.find("{*}ObsDimension").attrib["value"]
    value = obs.find("{*}ObsValue").attrib["value"]

    print(date, value)


# Ricerca della data più recente
dates = [
    obs.find("{*}ObsDimension").attrib["value"]
    for obs in observations
]

latest_date = max(dates)

print("Data più recente:", latest_date)


# Ricerca dell'ultima osservazione
latest_obs = next(
    obs for obs in observations
    if obs.find("{*}ObsDimension").attrib["value"] == latest_date
)

last_date = latest_obs.find("{*}ObsDimension").attrib["value"]
last_value = latest_obs.find("{*}ObsValue").attrib["value"]

print("Ultima osservazione:", last_date, last_value)


# Creazione della tabella SQLite
cursor.execute("""
CREATE TABLE IF NOT EXISTS exchange_rates (
    date TEXT,
    rate REAL
)
""")


# Creazione della lista con tutte le osservazioni
data = []

for obs in observations:
    date = obs.find("{*}ObsDimension").attrib["value"]
    value = float(obs.find("{*}ObsValue").attrib["value"])

    data.append((date, value))


# Aggiornamento del database
cursor.execute("DELETE FROM exchange_rates")

for row in data:
    cursor.execute(
        "INSERT INTO exchange_rates (date, rate) VALUES (?, ?)",
        row
    )

conn.commit()


# Controllo del numero di righe nel database
cursor.execute("SELECT COUNT(*) FROM exchange_rates")

print("Righe nel database:", cursor.fetchone()[0])


# Query SQL: ultime 5 osservazioni
cursor.execute("""
SELECT *
FROM exchange_rates
ORDER BY date DESC
LIMIT 5
""")

print("Ultime 5 righe dal database:")
print(cursor.fetchall())


# Query SQL: ultime 2 osservazioni
cursor.execute("""
SELECT date, rate
FROM exchange_rates
ORDER BY date DESC
LIMIT 2
""")

last_two = cursor.fetchall()

print("Ultime 2 osservazioni:", last_two)


# Calcolo della variazione
last_date, last_value = last_two[0]
previous_date, previous_value = last_two[1]

variation_sql = last_value - previous_value

print("Variazione calcolata con SQL:", round(variation_sql, 4))


# Calcolo della variazione percentuale
variation_pct_sql = (
    (last_value - previous_value)
    / previous_value
    * 100
)

print(
    "Variazione percentuale calcolata con SQL:",
    round(variation_pct_sql, 2),
    "%"
)


# Chiusura della connessione
conn.close()


# La serie utilizzata è EUR/USD:
# 1 euro = quanti dollari statunitensi
