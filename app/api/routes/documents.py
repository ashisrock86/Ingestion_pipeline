import uuid
import io
import os

from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

router = APIRouter()

# -----------------------------
# Embeddings model
# -----------------------------
embeddings = HuggingFaceBgeEmbeddings()

INDEX_PATH = "./faiss_index"


# -----------------------------
# FAISS SAVE FUNCTION
# -----------------------------
def save_faiss(docs, metadatas):
    """
    docs: list[str]
    metadatas: list[dict]
    """

    if os.path.exists(INDEX_PATH):
        vectorstore = FAISS.load_local(
            INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        vectorstore.add_texts(
            texts=docs,
            metadatas=metadatas
        )
    else:
        vectorstore = FAISS.from_texts(
            texts=docs,
            embedding=embeddings,
            metadatas=metadatas
        )

    vectorstore.save_local(INDEX_PATH)


# -----------------------------
# UPLOAD ENDPOINT
# -----------------------------
@router.post("/upload", tags=["Upload"])
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # -----------------------------
        # 1. Extract text
        # -----------------------------
        reader = PdfReader(io.BytesIO(contents))

        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found")

        # -----------------------------
        # 2. Chunking
        # -----------------------------
        chunk_size = 500
        chunks = [
            text[i:i + chunk_size]
            for i in range(0, len(text), chunk_size)
        ]

        doc_id = uuid.uuid4().hex

        # -----------------------------
        # 3. Metadata
        # -----------------------------
        metadatas = [
            {
                "document_id": doc_id,
                "chunk_index": i,
                "filename": file.filename
            }
            for i in range(len(chunks))
        ]

        # -----------------------------
        # 4. Store in FAISS
        # -----------------------------
        save_faiss(chunks, metadatas)

        return {
            "document_id": doc_id,
            "filename": file.filename,
            "chunks_indexed": len(chunks)
        }
    
    

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    