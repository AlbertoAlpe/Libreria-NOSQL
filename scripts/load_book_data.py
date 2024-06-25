import requests
from pymongo import MongoClient

# Connessione a MongoDB
client = MongoClient('mongodb://localhost:27019/?directConnection=true')
db = client['lib-ita']
collection = db['libri']

# Funzione per ottenere dati sui libri dall'API di Open Library
def get_books_data(isbn_list):
    base_url = "https://openlibrary.org/api/books"
    books_data = [ ]

    for isbn in isbn_list:
        url = f"{base_url}?bibkeys=ISBN:{isbn}&jscmd=data&format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            key = f"ISBN:{isbn}"
            if key in data:
                books_data.append(data[key])
    
    return books_data

# Lista di ISBN per esempio
isbn_list = ["0451526538", "0451524934", "9780140328721", "9780439139595", "9780439064873", "9780439136365"]

# Ottieni i dati
books_data = get_books_data(isbn_list)

# Inserisci i dati in MongoDB
if books_data:
    collection.insert_many(books_data)
    print("Dati inseriti con successo.")
else:
    print("Nessun dato trovato.")

# Chiudi la connessione
client.close()


