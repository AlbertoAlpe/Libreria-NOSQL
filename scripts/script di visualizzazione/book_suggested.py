import requests

# Funzione per ottenere gli ISBN associati da Riak per una parola
def get_keywords_and_isbns(word):
    url = f"http://localhost:32768/riak/InvertedIndex/{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        document_data = response.json()

        # Verifica se il documento ha il formato atteso (lista di ISBN)
        if isinstance(document_data, list):
            return document_data  # Ritorna direttamente la lista di ISBN

        print(f"Unexpected response format for word '{word}': {response.text}")
        return []

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []

    except ValueError as e:
        print(f'ValueError: {e}')
        return []

# URL per la richiesta MapReduce
url = "http://localhost:32768/mapred"

# Corpo della richiesta per il MapReduce
payload = {
  "inputs": "InvertedIndex",
  "query": [
    {
      "map": {
        "language": "javascript",
        "source": "function(value) { return [value.key]; }"
      }
    }
  ]
}

# Invio della richiesta MapReduce
headers = {'Content-Type': 'application/json'}
try:
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    # Elaborazione della risposta MapReduce
    result = response.json()

    isbn_count_map = {}
    isbn_to_check = "9780316769488"  # Sostituire con l'ISBN desiderato da verificare

    for word in result:
        # Per ogni parola chiave, otteniamo la lista di ISBN associati
        try:
            isbns = get_keywords_and_isbns(word)

            # Controlla se l'ISBN da verificare è presente nella lista di ISBN
            if isbn_to_check in isbns:
                # Aggiorna la mappa isbn_count_map con gli ISBN associati
                for isbn in isbns:
                    if isbn != isbn_to_check:
                        if isbn not in isbn_count_map:
                            isbn_count_map[isbn] = 0
                        isbn_count_map[isbn] += 1

        except Exception as e:
            print(f"Error processing word '{word}': {e}")

except requests.exceptions.RequestException as e:
    print(f'Request error: {e}')
    exit()

except ValueError as e:
    print(f'ValueError: {e}')
    exit()

# Trova i 5 ISBN che compaiono più frequentemente
top_isbns = sorted(isbn_count_map.items(), key=lambda item: item[1], reverse=True)[:5]

print("Mappa completa delle parole chiave e degli ISBN associati:")
for isbn, count in isbn_count_map.items():
    print(f"ISBN '{isbn}': {count} volte")

print("\nTop 5 ISBN che compaiono più frequentemente (escluso l'ISBN originale):")
for isbn, count in top_isbns:
    print(f"ISBN '{isbn}': {count} volte")
