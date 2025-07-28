import os
from dotenv import load_dotenv
import chromadb

class QueryInspector:
    def __init__(self, db_path=None):
        load_dotenv()
        env_db_path = os.environ.get("CHROMA_DB_PATH")
        self.db_path = db_path or env_db_path
        if not self.db_path:
            raise ValueError("CHROMA_DB_PATH must be set in the environment or passed to QueryInspector.")
        self.client = chromadb.PersistentClient(path=self.db_path)

    def list_collections(self):
        return self.client.list_collections()

    def get_collection_info(self, collection_name):
        col = self.client.get_collection(collection_name)
        results = col.get()
        return {
            "ids": results.get("ids"),
            "metadatas": results.get("metadatas"),
            "documents": results.get("documents")
        }

    def print_all_collections(self):
        collections = self.list_collections()
        if not collections:
            print(f"No collections found in ChromaDB at {self.db_path}")
            return
        for collection in collections:
            print(f"\nCollection: {collection.name}")
            info = self.get_collection_info(collection.name)
            print("IDs:", info["ids"])
            print("Metadatas:", info["metadatas"])
            print("Documents:", info["documents"])

if __name__ == "__main__":
    inspector = QueryInspector()
    inspector.print_all_collections()
