import requests
from pymongo import MongoClient
from faker import Faker
import random

# Connetti a MongoDB
client = MongoClient('mongodb://localhost:27019/?directConnection=true')
db = client['lib-ita']
collection = db['libri']

# Generatore di dati fittizi
fake = Faker()

# Funzione per ottenere dati sui libri dall'API di Open Library
def get_books_data(isbn_list):
    base_url = "https://openlibrary.org/api/books"
    books_data = []

    for isbn in isbn_list:
        url = f"{base_url}?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            key = f"ISBN:{isbn}"
            if key in data:
                book_data = data[key]
                filtered_data = {
                    "titolo": book_data.get("title", "No title available"),
                    "autori": [author["name"] for author in book_data.get("authors", [])],
                    "copertina": book_data.get("cover", {}).get("large", "No cover available"),
                    "ISBN": isbn,
                    "prezzo": round(random.uniform(5.0, 50.0), 2),  # Prezzo casuale tra 5.0 e 50.0
                    "valutazione_media": round(random.uniform(1.0, 5.0), 1),  # Valutazione casuale tra 1.0 e 5.0
                    "disponibilità": random.randint(0, 100)  # Disponibilità casuale tra 0 e 100
                }
                books_data.append(filtered_data)
    
    return books_data

# Lista di ISBN per esempio
isbn_list = ["0451526538", "0451524934", "9780140328721", "9780439139595", "9780439064873", "9780439136365"]

books_data = get_books_data(isbn_list)

# Inserisci i dati in MongoDB
if books_data:
    collection.insert_many(books_data)
    print("Dati inseriti con successo.")
else:
    print("Nessun dato trovato.")

# Chiudi la connessione
client.close()
