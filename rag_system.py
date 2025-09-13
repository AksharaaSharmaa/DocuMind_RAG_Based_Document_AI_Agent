import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import json
import asyncio
import re
from arxiv_api import ArxivAPI

load_dotenv()

class RAGSystem:
    def __init__(self):
        # Initialize Gemini API
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path="./vector_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.chroma_client.get_collection("documents")
        except:
            self.collection = self.chroma_client.create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine"}
            )
    
    async def add_document(self, doc_info):
        """Add document to vector database"""
        try:
            # Prepare documents for embedding
            documents = []
            metadatas = []
            ids = []
            
            # Add document sections
            for i, section in enumerate(doc_info.sections):
                if section.content.strip():
                    doc_id = f"{doc_info.file_id}_section_{i}"
                    documents.append(section.content)
                    metadatas.append({
                        "file_id": doc_info.file_id,
                        "filename": doc_info.filename,
                        "title": doc_info.title,
                        "section_title": section.title,
                        "section_type": section.section_type,
                        "page_number": section.page_number,
                        "document_title": doc_info.title
                    })
                    ids.append(doc_id)
            
            # Add abstract if available
            if doc_info.abstract:
                abstract_id = f"{doc_info.file_id}_abstract"
                documents.append(doc_info.abstract)
                metadatas.append({
                    "file_id": doc_info.file_id,
                    "filename": doc_info.filename,
                    "title": doc_info.title,
                    "section_title": "Abstract",
                    "section_type": "abstract",
                    "page_number": 1,
                    "document_title": doc_info.title
                })
                ids.append(abstract_id)
            
            # Generate embeddings
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # Add to ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            
        except Exception as e:
            raise Exception(f"Error adding document to vector database: {str(e)}")
    
    async def remove_document(self, file_id: str):
        """Remove document from vector database"""
        try:
            # Get all documents with this file_id
            results = self.collection.get(where={"file_id": file_id})
            if results['ids']:
                self.collection.delete(ids=results['ids'])
        except Exception as e:
            print(f"Error removing document: {str(e)}")
    
    async def query(self, query: str, document_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Query the RAG system"""
        try:
            # Check if the query is about Arxiv papers
            arxiv_keywords = ["arxiv", "paper", "research paper", "scientific paper", "publication"]
            is_arxiv_query = any(keyword in query.lower() for keyword in arxiv_keywords)
            
            # If it's an Arxiv query, search Arxiv first
            arxiv_context = ""
            arxiv_sources = []
            
            if is_arxiv_query:
                # Extract potential search terms
                search_terms = query.lower()
                for prefix in ["find papers about", "search for papers on", "arxiv papers about", "research papers on"]:
                    if prefix in search_terms:
                        search_terms = search_terms.split(prefix)[1].strip()
                        break
                
                # Search Arxiv
                arxiv_results = await self.search_arxiv(search_terms, max_results=3)
                
                if arxiv_results.get("success", False) and arxiv_results.get("papers", []):
                    papers = arxiv_results["papers"]
                    
                    # Add Arxiv results to context
                    arxiv_context_parts = []
                    for i, paper in enumerate(papers):
                        paper_context = f"Arxiv Paper {i+1}: {paper['title']}\n"
                        paper_context += f"Authors: {', '.join(paper['authors'])}\n"
                        paper_context += f"Summary: {paper['summary']}\n"
                        paper_context += f"Links: {paper['html_link']} | PDF: {paper['pdf_link']}\n"
                        
                        arxiv_context_parts.append(paper_context)
                        
                        arxiv_sources.append({
                            "filename": f"Arxiv: {paper['title']}",
                            "section_title": "Summary",
                            "page_number": 1,
                            "relevance_score": 0.95 - (i * 0.05),  # Slightly decrease relevance for each paper
                            "arxiv_id": paper['arxiv_id'],
                            "html_link": paper['html_link'],
                            "pdf_link": paper['pdf_link']
                        })
                    
                    arxiv_context = "\n\n".join(arxiv_context_parts)
            
            # Generate query embedding for local documents
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            
            # Prepare where clause for filtering
            where_clause = None
            if document_ids:
                where_clause = {"file_id": {"$in": document_ids}}
            
            # Search for relevant documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
                where=where_clause
            )
            
            # Prepare context for Gemini
            context_parts = []
            sources = []
            
            # Add local document results if available
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0], 
                    results['metadatas'][0], 
                    results['distances'][0]
                )):
                    context_parts.append(f"Source {i+1} (from {metadata['filename']}, {metadata['section_title']}):\n{doc}")
                    sources.append({
                        "filename": metadata['filename'],
                        "section_title": metadata['section_title'],
                        "page_number": metadata['page_number'],
                        "relevance_score": 1 - distance  # Convert distance to similarity
                    })
            
            # Combine Arxiv and local document contexts
            if arxiv_context:
                context_parts.insert(0, "Arxiv Papers:\n" + arxiv_context)
                sources = arxiv_sources + sources
            
            # If no context available, return empty response
            if not context_parts:
                return {
                    "answer": "I couldn't find any relevant information in the uploaded documents or Arxiv papers.",
                    "sources": [],
                    "confidence": 0.0
                }
            
            context = "\n\n".join(context_parts)
            
            # Create prompt for Gemini
            prompt = f"""Based on the following context from uploaded documents, please answer the user's question. 
            If the information is not available in the context, please say so clearly and explicitly.
            
            Context:
            {context}
            
            Question: {query}
            
            Instructions:
            1. If the information is not found in the context, start your response with "I cannot find information about [topic] in the provided documents." Be specific about what information is missing.
            2. If you find relevant information, provide a comprehensive answer based on the context.
            3. If you reference specific information, mention which document and section it came from.
            4. Do not make up or infer information that is not explicitly stated in the context.
            5. If the question is about a topic that is completely unrelated to the documents, clearly state that the documents do not contain information on that topic.
            """
            
            # Generate response using Gemini
            response = await asyncio.to_thread(
                self.model.generate_content, 
                prompt
            )
            
            answer = response.text if response.text else "I couldn't generate a response."
            
            # Calculate confidence based on relevance scores
            confidence = np.mean([source['relevance_score'] for source in sources]) if sources else 0.0
            
            return {
                "answer": answer,
                "sources": sources,
                "confidence": float(confidence)
            }
            
        except Exception as e:
            raise Exception(f"Error querying RAG system: {str(e)}")
    
    async def summarize_document(self, file_id: str) -> str:
        """Generate a summary of a specific document"""
        try:
            # Get all sections for this document
            results = self.collection.get(where={"file_id": file_id})
            
            if not results['documents']:
                return "Document not found or has no content."
            
            # Combine all content
            full_content = "\n\n".join(results['documents'])
            
            prompt = f"""Please provide a comprehensive summary of the following document:
            
            {full_content}
            
            Include:
            1. Main topic and purpose
            2. Key findings or results
            3. Methodology (if applicable)
            4. Conclusions
            5. Important figures or data points mentioned"""
            
            response = await asyncio.to_thread(
                self.model.generate_content, 
                prompt
            )
            
            return response.text if response.text else "Could not generate summary."
            
        except Exception as e:
            raise Exception(f"Error summarizing document: {str(e)}")
    
    async def extract_evaluation_metrics(self, query: str) -> Dict[str, Any]:
        """Extract specific evaluation metrics from documents"""
        try:
            # Search for relevant content
            query_embedding = self.embedding_model.encode([query]).tolist()[0]
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=10
            )
            
            if not results['documents'] or not results['documents'][0]:
                return {"metrics": [], "sources": []}
            
            # Look for numerical data and metrics
            metrics = []
            sources = []
            
            for doc, metadata, distance in zip(
                results['documents'][0], 
                results['metadatas'][0], 
                results['distances'][0]
            ):
                # Look for common metric patterns
                metric_patterns = [
                    r'accuracy[:\s]*([0-9.]+%?)',
                    r'f1[-\s]?score[:\s]*([0-9.]+%?)',
                    r'precision[:\s]*([0-9.]+%?)',
                    r'recall[:\s]*([0-9.]+%?)',
                    r'auc[:\s]*([0-9.]+%?)',
                    r'rmse[:\s]*([0-9.]+%?)',
                    r'mae[:\s]*([0-9.]+%?)',
                ]
                
                for pattern in metric_patterns:
                    matches = re.findall(pattern, doc, re.IGNORECASE)
                    for match in matches:
                        metrics.append({
                            "metric": pattern.split('[')[0],
                            "value": match,
                            "context": doc[:200] + "..." if len(doc) > 200 else doc
                        })
                        sources.append({
                            "filename": metadata['filename'],
                            "section_title": metadata['section_title'],
                            "page_number": metadata['page_number']
                        })
            
            return {
                "metrics": metrics,
                "sources": sources
            }
            
        except Exception as e:
            raise Exception(f"Error extracting metrics: {str(e)}")
    
    async def search_arxiv(self, query: str, start: int = 0, max_results: int = 10) -> Dict[str, Any]:
        """Search for papers on Arxiv
        
        Args:
            query: The search query
            start: The index of the first result to return (0-based)
            max_results: The maximum number of results to return (max 2000)
            
        Returns:
            Dictionary containing search results
        """
        try:
            # Call the Arxiv API
            result = await ArxivAPI.search(query, start, max_results)
            
            if not result.get("success", False):
                return {
                    "success": False,
                    "error": result.get("error", "Unknown error occurred")
                }
            
            # Process the results to make them more user-friendly
            papers = result.get("papers", [])
            processed_papers = []
            
            for paper in papers:
                processed_papers.append({
                    "title": paper.get("title", "").strip(),
                    "summary": paper.get("summary", "").strip(),
                    "authors": [author.get("name", "") for author in paper.get("authors", [])],
                    "published": paper.get("published", ""),
                    "arxiv_id": paper.get("arxiv_id", ""),
                    "pdf_link": paper.get("links", {}).get("pdf", ""),
                    "html_link": paper.get("links", {}).get("html", ""),
                    "categories": paper.get("categories", []),
                    "journal_ref": paper.get("journal_ref", "")
                })
            
            return {
                "success": True,
                "total_results": result.get("total_results", 0),
                "papers": processed_papers
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error searching Arxiv: {str(e)}"
            }
