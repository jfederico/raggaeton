import os
from dotenv import load_dotenv
import chromadb

load_dotenv()
chroma_db_path = os.environ.get("CHROMA_DB_PATH")
if not chroma_db_path:
    raise ValueError("CHROMA_DB_PATH not set in environment variables or .env file.")

client = chromadb.PersistentClient(path=chroma_db_path)
collection = client.get_or_create_collection("rag-index")

# List all documents/chunks
results = collection.get()
print("Document IDs:", results['ids'])
print("Metadatas:", results['metadatas'])
print("Documents:", results['documents'])

