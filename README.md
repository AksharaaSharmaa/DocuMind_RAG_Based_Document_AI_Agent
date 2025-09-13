<h1 align="center"><b>DocuMind - AI Document Intelligence System</b></h1>

<div align="center">

![DocuMind Logo](https://img.shields.io/badge/DocuMind-AI%20Document%20Intelligence-blue?style=for-the-badge)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-2.0-purple.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

A powerful Retrieval-Augmented Generation (RAG) system built with FastAPI and Google's Gemini API for intelligent document processing, analysis, and querying. DocuMind transforms your PDF documents into an interactive knowledge base that you can query using natural language.

## 🌟 Key Features

### 📄 Advanced Document Processing
- **Multi-Document Support**: Process up to 5 PDF documents simultaneously with intelligent error handling
- **Structured Content Extraction**: Automatically identifies and preserves document hierarchy including abstracts, sections, methodologies, results, and conclusions
- **Intelligent Section Classification**: Recognizes and categorizes different content types (titles, abstracts, tables, references) for better organization
- **Metadata Preservation**: Extracts and maintains document metadata including titles, page counts, timestamps, and source attribution
- **High-Fidelity Text Extraction**: Uses advanced PDF parsing to maintain formatting and content relationships

### 🧠 Intelligent Query System
- **Natural Language Processing**: Ask questions in plain English and receive contextually relevant answers
- **Semantic Search**: Advanced vector-based similarity matching finds relevant content even when exact keywords aren't present
- **Multi-Document Querying**: Search across your entire document collection or filter queries to specific documents
- **Context-Aware Responses**: Generates comprehensive answers by combining information from multiple relevant sections
- **Source Attribution**: Every response includes detailed citations with document names, section titles, and page numbers

### 🔍 Vector Database Technology
- **Persistent Storage**: ChromaDB integration ensures your processed documents remain available across sessions
- **High-Dimensional Embeddings**: 384-dimensional vector representations using state-of-the-art sentence transformers
- **Cosine Similarity Matching**: Optimized similarity search algorithms for fast and accurate content retrieval
- **Scalable Architecture**: Designed to handle growing document collections efficiently

### 📚 ArXiv Research Integration
- **Direct ArXiv Search**: Search scientific papers directly from the ArXiv database without leaving the application
- **Intelligent Query Formatting**: Optimized search queries using exact phrase matching for precise results
- **Comprehensive Metadata**: Access paper titles, authors, abstracts, categories, and direct PDF links
- **Seamless Integration**: Incorporate ArXiv papers into your conversation context for comparative analysis
- **Pagination Support**: Efficiently browse through large research result sets

### 🎨 Modern User Interface
- **Responsive Design**: Optimized experience across desktop, tablet, and mobile devices
- **Drag-and-Drop Upload**: Intuitive document upload with visual feedback and progress indicators
- **Interactive Chat Interface**: Clean, WhatsApp-style messaging interface for natural conversations
- **Document Management Sidebar**: Easy access to uploaded documents with quick delete and filter options
- **ArXiv Search Panel**: Dedicated research search interface with formatted result displays
- **Real-Time Updates**: Live updates for document processing status and query results

### 🔒 Enterprise-Grade Security
- **Secure API Key Management**: Environment variable-based configuration prevents credential exposure
- **Input Validation**: Comprehensive request validation using Pydantic models prevents injection attacks
- **File Type Validation**: Strict file type and size validation for secure document uploads
- **Error Handling**: Robust exception handling prevents information leakage through error messages
- **CORS Protection**: Properly configured cross-origin resource sharing for controlled access

### ⚡ Performance Optimizations
- **Asynchronous Processing**: Non-blocking I/O operations for improved responsiveness during document processing
- **Efficient Vector Operations**: Optimized similarity search algorithms handle large document collections
- **Resource Management**: Automatic cleanup of temporary files and memory resources
- **Lazy Loading**: Progressive loading of content reduces initial load times
- **Caching Strategy**: Smart caching of processed documents and search results

### 🔧 Developer-Friendly Architecture
- **Modular Design**: Clean separation of concerns across document processing, vector storage, and API layers
- **RESTful API**: Well-documented FastAPI endpoints for easy integration and extension
- **Comprehensive Error Handling**: Detailed error responses with appropriate HTTP status codes
- **Type Safety**: Full type hints throughout the codebase for better development experience
- **Extensible Framework**: Plugin-ready architecture for adding new document types and AI models

### 📊 Analytics and Insights
- **Document Statistics**: View processing metrics including section counts, word counts, and structure analysis
- **Query Performance**: Track search accuracy and response times for optimization
- **Usage Patterns**: Monitor most queried topics and frequently accessed documents
- **Source Tracking**: Detailed attribution showing which documents contribute to each response

### 🌐 API Capabilities
- **Document Upload API**: Programmatic document ingestion with batch processing support
- **Query Processing API**: RESTful query interface with filtering and pagination options
- **Document Management API**: Full CRUD operations for document lifecycle management
- **ArXiv Search API**: Direct integration with ArXiv's research database
- **Health Monitoring**: Built-in endpoints for system health checks and monitoring

### 🚀 Deployment Ready
- **Cross-Platform Support**: Runs on Windows, macOS, and Linux with included installation scripts
- **Docker Support**: Container-ready configuration for easy deployment and scaling
- **Environment Configuration**: Flexible configuration management through environment variables
- **Dependency Management**: Pinned dependencies ensure consistent deployment across environments
- **Production Optimized**: Built-in security headers, logging, and performance monitoring

## 🎯 Use Cases

- **Research Analysis**: Quickly extract insights from academic papers and research documents
- **Technical Documentation**: Query complex technical manuals and documentation sets
- **Legal Document Review**: Search through contracts, agreements, and legal documents
- **Educational Resources**: Create interactive study materials from textbooks and papers
- **Business Intelligence**: Extract insights from reports, presentations, and business documents
- **Literature Reviews**: Efficiently analyze and compare multiple research papers
- **Compliance Auditing**: Search through regulatory documents and compliance materials

## 🔮 Advanced Features

### Smart Document Understanding
DocuMind doesn't just extract text—it understands document structure and meaning. The system recognizes academic paper formats, identifies key sections, and maintains relationships between different parts of your documents.

### Contextual Response Generation
Unlike simple keyword matching, DocuMind uses advanced AI to understand the intent behind your questions and provides comprehensive answers that synthesize information from multiple sources.

### Research Integration
The ArXiv integration allows you to seamlessly incorporate external research into your analysis, making it perfect for literature reviews and comparative studies.

### Scalable Architecture
Built with enterprise needs in mind, DocuMind can handle growing document collections while maintaining fast query response times and efficient resource usage.

## 💡 Getting Started

DocuMind is designed for easy deployment with comprehensive installation scripts and clear documentation. Whether you're a researcher, student, or business professional, you can have your intelligent document system running in minutes.

Transform your document workflow today with DocuMind's powerful AI-driven document intelligence capabilities!

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- 4GB+ RAM recommended for document processing

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/DocuMind.git
cd DocuMind
```

### 2. Create a virtual environment (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
# Copy the example environment file
copy env_example.txt .env
```

Edit the `.env` file and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

> **Note**: You can obtain a Gemini API key from [Google AI Studio](https://ai.google.dev/).

## 🏃‍♂️ Running the Application

### Start the server

```bash
python main.py
```

This will start the FastAPI server on `http://localhost:8001`.

### Access the application

Open your browser and navigate to:
- Landing page: `http://localhost:8001/`
- Application interface: `http://localhost:8001/app`

## 🔧 Usage Guide

### Uploading Documents

1. Navigate to the application interface at `http://localhost:8001/app`
2. Click on the upload section in the sidebar or drag and drop PDF files
3. Upload up to 5 PDF documents at once
4. Documents are automatically processed, indexed, and made available for querying

### Searching ArXiv Papers

1. Click on the ArXiv search section in the sidebar
2. Enter your search query for scientific papers
3. Browse through the results and click "Add to Chat" to include papers in your conversation

### Querying Documents

1. Type your question in the chat input at the bottom of the screen
2. The AI will analyze your documents and provide relevant answers
3. Sources are automatically cited with links to the original content

### Example Queries

- "What is the main methodology described in Paper X?"
- "Summarize the key findings across all uploaded documents"
- "What evaluation metrics were used in these papers?"
- "Compare the approaches in Paper A and Paper B"
- "What are the limitations mentioned in the conclusion?"

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/app` | GET | Main application interface |
| `/upload` | POST | Upload PDF documents |
| `/query` | POST | Query the RAG system |
| `/documents` | GET | Get list of uploaded documents |
| `/documents/{file_id}` | DELETE | Delete a document |
| `/arxiv/search` | POST | Search for papers on ArXiv |

## 🏗️ Technical Architecture

- **Backend**: FastAPI with async support for high performance
- **AI Model**: Google Gemini Pro for advanced language understanding
- **Vector Database**: ChromaDB with sentence transformers for semantic search
- **Document Processing**: PyMuPDF for accurate PDF extraction
- **Frontend**: Vanilla JavaScript with modern CSS for a responsive UI

## 📁 Project Structure

```
DocuMind/
├── main.py                # FastAPI application entry point
├── document_processor.py  # PDF processing and text extraction
├── rag_system.py         # RAG implementation with Gemini integration
├── arxiv_api.py          # ArXiv API client
├── models.py             # Pydantic data models
├── app.html              # Main application interface
├── index.html            # Landing page
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create from env_example.txt)
├── uploads/              # Directory for uploaded documents
└── vector_db/           # ChromaDB vector database storage
```

## 🔄 Development Workflow

To run the application in development mode with auto-reload:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.

---

<div align="center">
Built with ❤️ using FastAPI and Google Gemini
</div>
