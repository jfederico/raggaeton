
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
import tempfile
import shutil
from .ingest import RAGIngestionPipeline

app = FastAPI()
vector_index = None  # store global reference



class QueryRequest(BaseModel):
    question: str


# Accept PDF file upload and optional metadata
@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None)
):
    # Save uploaded file to a temp location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Parse metadata if provided
    meta_dict = {}
    if metadata:
        import json
        try:
            meta_dict = json.loads(metadata)
        except Exception:
            return JSONResponse(status_code=400, content={"error": "Invalid metadata JSON"})

    # Run RAG pipeline up to persist
    pipeline = RAGIngestionPipeline()
    try:
        index = pipeline.ingest(tmp_path, metadata=meta_dict)
        return {"status": "success", "message": "PDF ingested and persisted."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    finally:
        try:
            file.file.close()
        except Exception:
            pass
        try:
            import os
            os.remove(tmp_path)
        except Exception:
            pass

@app.post("/query")
async def query(req: QueryRequest):
    global vector_index
    response = vector_index.as_query_engine().query(req.question)
    return {"answer": str(response)}
