from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
import json
import uuid
from typing import List, Dict, Any
import asyncio
from pathlib import Path

from document_processor import DocumentProcessor
from rag_system import RAGSystem
from models import QueryRequest, QueryResponse, DocumentInfo, ArxivSearchRequest, ArxivSearchResponse

app = FastAPI(title="DocuMind RAG System", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="."), name="static")

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_db", exist_ok=True)

# Initialize components
try:
    print("Initializing document processor...")
    doc_processor = DocumentProcessor()
    print("Document processor initialized successfully")
    
    print("Initializing RAG system...")
    rag_system = RAGSystem()
    print("RAG system initialized successfully")
except Exception as e:
    print(f"Error initializing components: {str(e)}")
    raise e

# Global state for uploaded documents
uploaded_documents: Dict[str, DocumentInfo] = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/app", response_class=HTMLResponse)
async def read_app():
    with open("app.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload and process multiple PDF documents"""
    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 files allowed")
    
    processed_docs = []
    
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Save file
        file_id = str(uuid.uuid4())
        file_path = f"uploads/{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document
        try:
            print(f"Processing document: {file.filename}")
            doc_info = await doc_processor.process_document(file_path, file.filename)
            doc_info.file_id = file_id
            doc_info.file_path = file_path
            
            print(f"Document processed - Title: {doc_info.title}, Sections: {len(doc_info.sections)}")
            
            # Add to vector database
            print("Adding document to vector database...")
            await rag_system.add_document(doc_info)
            print("Document added to vector database successfully")
            
            uploaded_documents[file_id] = doc_info
            processed_docs.append({
                "file_id": file_id,
                "filename": file.filename,
                "title": doc_info.title,
                "sections": len(doc_info.sections),
                "pages": doc_info.page_count
            })
            
        except Exception as e:
            print(f"Error processing document {file.filename}: {str(e)}")
            # Clean up file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
    
    return {"message": f"Successfully processed {len(processed_docs)} documents", "documents": processed_docs}

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the RAG system"""
    try:
        print(f"Query received: {request.query}")
        print(f"Document IDs: {request.document_ids}")
        print(f"Uploaded documents count: {len(uploaded_documents)}")
        
        # Check if the query might be related to ArXiv papers
        arxiv_keywords = ["arxiv", "paper", "research paper", "scientific paper", "publication"]
        is_arxiv_query = any(keyword in request.query.lower() for keyword in arxiv_keywords)
        
        # Check if we have any documents
        if not uploaded_documents and not is_arxiv_query:
            return QueryResponse(
                answer="No documents have been uploaded yet. Please upload some PDF documents first.",
                sources=[],
                confidence=0.0
            )
        
        response = await rag_system.query(request.query, request.document_ids)
        print(f"RAG response: {response}")
        
        # Check if there are ArXiv sources in the result
        has_arxiv_sources = any("arxiv_id" in source for source in response["sources"] if isinstance(source, dict))
        
        # Enhance the answer if ArXiv sources are present
        if has_arxiv_sources:
            answer = response["answer"]
            if not answer.endswith("."):
                answer += "."
            answer += "\n\nI've also found some relevant papers on ArXiv that might be helpful. You can check the sources below for links to these papers."
            response["answer"] = answer
            
        return QueryResponse(
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"]
        )
    except Exception as e:
        print(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.get("/documents")
async def get_documents():
    """Get list of uploaded documents"""
    return {"documents": list(uploaded_documents.values())}

@app.delete("/documents/{file_id}")
async def delete_document(file_id: str):
    """Delete a document"""
    if file_id not in uploaded_documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc_info = uploaded_documents[file_id]
    
    # Remove from vector database
    await rag_system.remove_document(file_id)
    
    # Delete file
    if os.path.exists(doc_info.file_path):
        os.remove(doc_info.file_path)
    
    # Remove from memory
    del uploaded_documents[file_id]
    
    return {"message": "Document deleted successfully"}

@app.post("/arxiv/search", response_model=ArxivSearchResponse)
async def search_arxiv(request: ArxivSearchRequest):
    """Search for papers on Arxiv"""
    try:
        print(f"Arxiv search query received: {request.query}")
        
        # Call the RAG system's Arxiv search method
        response = await rag_system.search_arxiv(
            query=request.query,
            start=request.start,
            max_results=request.max_results
        )
        
        print(f"Arxiv search response: {response}")
        return ArxivSearchResponse(
            success=response.get("success", False),
            total_results=response.get("total_results", 0),
            papers=response.get("papers", []),
            error=response.get("error")
        )
    except Exception as e:
        print(f"Arxiv search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Arxiv search failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
