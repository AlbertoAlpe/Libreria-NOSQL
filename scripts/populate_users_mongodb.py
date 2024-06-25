from pymongo import MongoClient
from faker import Faker
import random

# Configurazione MongoDB
uri = "mongodb://localhost:27023/?directConnection=true"  #stringa di connessione di MongoDBCompass
client = MongoClient(uri)
db = client['lib-fra']  # modificare il database: lib-ita, lib-ger, lib-fra
collection = db['utenti']

# Generatore di dati fittizi
fake = Faker()

# Funzione per generare un utente fittizio
def generate_fake_user():
    return {
        "nome": fake.first_name(),
        "cognome": fake.last_name(),
        "email": fake.email(),
        "indirizzo": fake.address(),
        "telefono": fake.phone_number(),
        "data_nascita": fake.date_of_birth(minimum_age=14, maximum_age=90).isoformat(),
        "sesso": random.choice(['M', 'F']),
        "username": fake.user_name(),
        "password": fake.password(),
        "creato_il": fake.date_time_this_decade().isoformat()
    }

# Numero di utenti da generare
num_utenti = 100

# Genera e inserisci gli utenti nel database
fake_users = [generate_fake_user() for _ in range(num_utenti)]
collection.insert_many(fake_users)

print(f"Inseriti {num_utenti} utenti fittizi nel database 'utenti_db'.")
