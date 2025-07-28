import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.query import QueryInspector

def main():
    inspector = QueryInspector()
    collections = inspector.list_collections()
    if not collections:
        print("No collections found in ChromaDB.")
        return
    for collection in collections:
        print(f"\nCollection: {collection.name}")
        info = inspector.get_collection_info(collection.name)
        print("IDs:", info["ids"], "\n")
        print("Metadatas:", info["metadatas"], "\n")
        print("Documents:", info["documents"], "\n")

if __name__ == "__main__":
    main()

