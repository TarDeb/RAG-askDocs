# RAG Document Query System

A Retrieval-Augmented Generation (RAG) system that allows you to query your markdown documents using semantic search with both command-line and web interfaces.

## Features

-  Process markdown documents
-  Semantic search using sentence transformers
-  Persistent vector database with ChromaDB
-  Interactive query interface (CLI and Web UI)
-  Modern web interface with Streamlit
-  Visual relevance scoring
## Usage

1. Start the web application:
2. Open your browser to the displayed URL (usually http://localhost:8501)
3. Upload a markdown file or process your existing PLAN.md
. Ask questions about your documents and get relevant chunks as answers!

## Project Structure

```
RAG-mydoc/
├── app.py                 # Streamlit interface
├── ask_md_rag.py          # 
├── build_vector_db.py     # Vd builder
├── prepare_md_data.py    
├── run_ui.bat            
├── chroma_db/             #vector database
├── requirements.txt       
└── README.md             

## How it works
1. **Document Processing**: Markdown files are chunked and embedded using SentenceTransformers
2. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
3. **Query Processing**: User questions are embedded and matched against stored chunks
4. **Results**: Most relevant document chunks are returned
