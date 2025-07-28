# RAG Document Query System

A Retrieval-Augmented Generation (RAG) system that allows you to query your markdown documents using semantic search.

## Features

- 📄 Process markdown documents
- 🔍 Semantic search using sentence transformers
- 💾 Persistent vector database with ChromaDB
- 🤖 Interactive query interface

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd RAG-mydoc
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. First, build the vector database from your markdown documents:
```bash
python build_vector_db.py
```

2. Start querying your documents:
```bash
python ask_md_rag.py
```

3. Ask questions about your documents and get relevant chunks as answers!

## Project Structure

```
RAG-mydoc/
├── ask_md_rag.py          # Main query interface
├── build_vector_db.py     # Vector database builder
├── chroma_db/             # Persistent vector database
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## How it works

1. **Document Processing**: Markdown files are chunked and embedded using SentenceTransformers
2. **Vector Storage**: Embeddings are stored in ChromaDB for fast retrieval
3. **Query Processing**: User questions are embedded and matched against stored chunks
4. **Results**: Most relevant document chunks are returned

## Requirements

- Python 3.7+
- See `requirements.txt` for package dependencies
