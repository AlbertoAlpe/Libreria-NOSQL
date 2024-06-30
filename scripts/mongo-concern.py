from pymongo import MongoClient, WriteConcern

# Connessione con write concern
uri = "mongodb://localhost:27023/?directConnection=true"
client = MongoClient(uri, w=2)

db = client['lib-ger']
collection = db['libri']