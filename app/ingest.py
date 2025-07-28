
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SimpleNodeParser
from sentence_transformers import SentenceTransformer
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import chromadb
import os
from dotenv import load_dotenv

class RAGIngestionPipeline:
    def __init__(self, db_path=None):
        load_dotenv()
        env_db_path = os.environ.get("CHROMA_DB_PATH")
        self.db_path = db_path or env_db_path
        if not self.db_path:
            raise ValueError("CHROMA_DB_PATH must be set in the environment or passed to RAGIngestionPipeline.")
        self.client = self._init_chroma_client()
        self.vector_store = self._init_vector_store()
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

    def _init_chroma_client(self):
        os.makedirs(self.db_path, exist_ok=True)
        return chromadb.PersistentClient(path=self.db_path)

    def _init_vector_store(self):
        return ChromaVectorStore(
            chroma_collection=self.client.get_or_create_collection("rag-index")
        )

    def load_pdf(self, pdf_path, metadata=None):
        reader = PDFReader()
        docs = reader.load_data(pdf_path)
        # Attach metadata to each document if provided
        if metadata:
            for doc in docs:
                doc.metadata = metadata
        return docs

    def preprocess(self, docs):
        parser = SimpleNodeParser()
        return parser.get_nodes_from_documents(docs)

    def embed(self, nodes):
        model = OllamaEmbedding(
            model_name="nomic-embed-text",  # or another embedding model available in your Ollama
            base_url="http://10.0.0.170:11434"  # default Ollama endpoint
        )
        for node in nodes:
            node.embedding = model.get_text_embedding(node.get_content())
        return nodes
        # model = SentenceTransformer("all-MiniLM-L6-v2")
        # for node in nodes:
        #     node.embedding = model.encode(node.get_content()).tolist()
        # return nodes

    def persist(self, nodes):
        # Create the embedding model instance
        embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",  # or your preferred embedding model
            base_url="http://10.0.0.170:11434"
        )
        # Pass embed_model to VectorStoreIndex
        index = VectorStoreIndex(
            nodes,
            storage_context=self.storage_context,
            embed_model=embed_model
        )
        index.storage_context.persist(persist_dir=self.db_path)
        return index
        # index = VectorStoreIndex(nodes, storage_context=self.storage_context)
        # index.storage_context.persist(persist_dir=self.db_path)
        # return index

    def ingest(self, pdf_path, metadata=None):
        docs = self.load_pdf(pdf_path, metadata)
        nodes = self.preprocess(docs)
        nodes = self.embed(nodes)
        index = self.persist(nodes)
        return index

# Example usage:
# pipeline = RAGIngestionPipeline()
# index = pipeline.ingest("/path/to/file.pdf", metadata={"course": "math101"})
