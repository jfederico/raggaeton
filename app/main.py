from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser

app = FastAPI()
vector_index = None  # store global reference

class IngestRequest(BaseModel):
    content: str
    metadata: dict = {}

class QueryRequest(BaseModel):
    question: str

@app.post("/ingest")
async def ingest(req: IngestRequest):
    global vector_index
    doc = Document(text=req.content, metadata=req.metadata)
    nodes = SimpleNodeParser().get_nodes_from_documents([doc])
    vector_index.insert_nodes(nodes)
    return {"status": "success", "chunks_added": len(nodes)}

@app.post("/query")
async def query(req: QueryRequest):
    global vector_index
    response = vector_index.as_query_engine().query(req.question)
    return {"answer": str(response)}
