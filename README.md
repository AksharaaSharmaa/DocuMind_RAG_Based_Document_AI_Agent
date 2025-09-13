<div align="center">
  # DocuMind - AI Document Intelligence System
</div>

<div align="center">

![DocuMind Logo](https://img.shields.io/badge/DocuMind-AI%20Document%20Intelligence-blue?style=for-the-badge)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-2.0-purple.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

A powerful Retrieval-Augmented Generation (RAG) system built with FastAPI and Google's Gemini API for intelligent document processing, analysis, and querying. DocuMind transforms your PDF documents into an interactive knowledge base that you can query using natural language.

## 🌟 Features

- **📄 Multi-Modal Document Processing**: Process multiple PDF documents simultaneously with advanced text extraction
- **💬 Intelligent Q&A Interface**: Ask direct questions about your documents and receive contextual answers
- **📊 Key Insights Extraction**: Automatically summarize methodologies and extract evaluation results
- **🔍 Advanced Search**: Find specific information across multiple documents with semantic search
- **🔒 Enterprise Security**: Built with enterprise-grade security protocols for document handling
- **🔗 ArXiv Integration**: Search and retrieve scientific papers directly from ArXiv
- **🚀 Modern UI**: Clean, responsive interface with intuitive document management

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
