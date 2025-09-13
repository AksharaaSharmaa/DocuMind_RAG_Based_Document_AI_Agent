from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentSection(BaseModel):
    title: str
    content: str
    page_number: int
    section_type: str  # "title", "abstract", "section", "table", "reference"

class DocumentInfo(BaseModel):
    file_id: str
    filename: str
    file_path: str
    title: str
    abstract: Optional[str] = None
    sections: List[DocumentSection] = []
    page_count: int
    upload_time: datetime
    metadata: Dict[str, Any] = {}

class QueryRequest(BaseModel):
    query: str
    document_ids: Optional[List[str]] = None  # If None, search all documents

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    confidence: float

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    sources: Optional[List[Dict[str, Any]]] = None

class ArxivAuthor(BaseModel):
    name: str
    affiliation: Optional[str] = None

class ArxivPaper(BaseModel):
    title: str
    summary: str
    authors: List[str]
    published: str
    arxiv_id: str
    pdf_link: str
    html_link: str
    categories: List[str]
    journal_ref: Optional[str] = None

class ArxivSearchRequest(BaseModel):
    query: str
    start: Optional[int] = 0
    max_results: Optional[int] = 10

class ArxivSearchResponse(BaseModel):
    success: bool
    total_results: Optional[int] = 0
    papers: Optional[List[ArxivPaper]] = []
    error: Optional[str] = None
