import os
from dotenv import load_dotenv
import chromadb

def inspect_chromadb():
    load_dotenv()
    chroma_db_path = os.environ.get("CHROMA_DB_PATH")
    if not chroma_db_path:
        raise ValueError("CHROMA_DB_PATH not set in environment variables.")

    client = chromadb.PersistentClient(path=chroma_db_path)
    collections = client.list_collections()
    if not collections:
        print(f"No collections found in ChromaDB at {chroma_db_path}")
        return

    for collection in collections:
        print(f"\nCollection: {collection.name}")
        col = client.get_collection(collection.name)
        results = col.get()
        print("IDs:", results.get("ids"))
        print("Metadatas:", results.get("metadatas"))
        print("Documents:", results.get("documents"))

if __name__ == "__main__":
    inspect_chromadb()
