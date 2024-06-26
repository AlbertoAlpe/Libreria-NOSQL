import requests
from pymongo import MongoClient

def get_book_data_from_api(isbn):
    base_url = "https://openlibrary.org/api/books"
    params = {
        'bibkeys': f'ISBN:{isbn}',
        'format': 'json',
        'jscmd': 'data'
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        key = f'ISBN:{isbn}'
        if key in data:
            book_data = data[key]
            title = book_data.get('title', 'N/A')
            authors = [author['name'] for author in book_data.get('authors', [])]
            cover = book_data.get('cover', {}).get('large', 'N/A')
            return title, authors, cover
        else:
            print(f"No data found for ISBN {isbn}")
            return None
    else:
        print(f"Error fetching data from API: {response.status_code}")
        return None

def get_book_data_from_mongodb(isbn):
    client = MongoClient('mongodb://localhost:27017/?directConnection=true')
    db = client['lib-ita']  # Sostituisci con il nome del tuo database
    collection = db['libri']
    
    # Trova il libro con l'ISBN specificato all'interno di identifiers.isbn_10
    book_data = collection.find_one({'ISBN': isbn})
    if book_data:
        price = book_data.get('prezzo', 'N/A')
        average_rating = book_data.get('valutazione_media', 'N/A')
        availability = book_data.get('disponibilità', 'N/A')
        return price, average_rating, availability
    else:
        print(f"No data found in MongoDB for ISBN {isbn}")
        return None

def main(isbn):
    api_data = get_book_data_from_api(isbn)
    if api_data:
        title, authors, cover = api_data
        print(f"Title: {title}")
        print(f"Authors: {', '.join(authors)}")
        print(f"Cover: {cover}")
    
    db_data = get_book_data_from_mongodb(isbn)
    if db_data:
        price, average_rating, availability = db_data
        print(f"Price: {price}")
        print(f"Average Rating: {average_rating}")
        print(f"Availability: {availability}")

if __name__ == "__main__":
    isbn = "9780140328721"
    main(isbn)
