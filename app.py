import streamlit as st
import os
import re
from sentence_transformers import SentenceTransformer
import chromadb
import time

# Page configuration
st.set_page_config(
    page_title="RAG Document Query System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'vector_db_built' not in st.session_state:
    st.session_state.vector_db_built = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'collection' not in st.session_state:
    st.session_state.collection = None

def load_model():
    """Load the sentence transformer model"""
    if st.session_state.model is None:
        with st.spinner("Loading AI model..."):
            st.session_state.model = SentenceTransformer("all-MiniLM-L6-v2")
    return st.session_state.model

def check_vector_db():
    """Check if vector database exists"""
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection("md_chunks")
        st.session_state.collection = collection
        st.session_state.vector_db_built = True
        return True
    except:
        st.session_state.vector_db_built = False
        return False

def process_markdown_file(uploaded_file, chunk_method="headings"):
    """Process uploaded markdown file and create chunks"""
    # Read the file content
    content = uploaded_file.read().decode("utf-8")
    
    # Save the uploaded file temporarily
    with open("temp_document.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    # Create chunks based on selected method
    if chunk_method == "headings":
        # Split by headings
        chunks = re.split(r'\n#{1,6} ', content)
    else:
        # Split by paragraphs (double newlines)
        chunks = content.split('\n\n')
    
    # Clean and filter chunks
    chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]
    
    # Save chunks to file
    with open("chunks.txt", "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(c + "\n---\n")
    
    return chunks

def build_vector_database(chunks):
    """Build vector database from chunks"""
    model = load_model()
    
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection if it exists and create new one
    try:
        client.delete_collection("md_chunks")
    except:
        pass
    
    collection = client.create_collection("md_chunks")
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Add each chunk as a document with its embedding
    for i, chunk in enumerate(chunks):
        progress = (i + 1) / len(chunks)
        progress_bar.progress(progress)
        status_text.text(f"Processing chunk {i+1}/{len(chunks)}")
        
        emb = model.encode(chunk).tolist()
        collection.add(documents=[chunk], embeddings=[emb], ids=[str(i)])
    
    progress_bar.empty()
    status_text.empty()
    
    st.session_state.collection = collection
    st.session_state.vector_db_built = True
    
    return collection

def query_documents(question, n_results=3):
    """Query the vector database"""
    if not st.session_state.vector_db_built or st.session_state.collection is None:
        return None
    
    model = load_model()
    
    # Encode the question
    q_emb = model.encode(question).tolist()
    
    # Query the collection
    results = st.session_state.collection.query(
        query_embeddings=[q_emb], 
        n_results=n_results
    )
    
    return results

# Main UI
def main():
    st.title("🤖 RAG Document Query System")
    st.markdown("Upload your markdown documents and ask questions about them!")
    
    # Sidebar for document processing
    with st.sidebar:
        st.header("📄 Document Processing")
        
        # Check if vector DB exists
        db_exists = check_vector_db()
        if db_exists:
            st.success("✅ Vector database loaded!")
        else:
            st.warning("⚠️ No vector database found")
        
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a markdown file",
            type=['md', 'txt'],
            help="Upload a .md or .txt file to process"
        )
        
        if uploaded_file is not None:
            st.success(f"📁 File uploaded: {uploaded_file.name}")
            
            # Chunking method selection
            chunk_method = st.selectbox(
                "Chunking method:",
                ["headings", "paragraphs"],
                help="Choose how to split your document"
            )
            
            if st.button("🔨 Process Document", type="primary"):
                with st.spinner("Processing document..."):
                    try:
                        # Process the markdown file
                        chunks = process_markdown_file(uploaded_file, chunk_method)
                        st.success(f"✅ Document split into {len(chunks)} chunks")
                        
                        # Build vector database
                        st.info("Building vector database...")
                        build_vector_database(chunks)
                        st.success("✅ Vector database built successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error processing document: {str(e)}")
        
        # Alternative: Process existing plan.md
        st.subheader("Process Existing Files")
        if os.path.exists("PLAN.md"):
            if st.button("🔨 Process PLAN.md"):
                with st.spinner("Processing PLAN.md..."):
                    try:
                        with open("PLAN.md", encoding="utf-8") as f:
                            content = f.read()
                        
                        chunks = re.split(r'\n#{1,6} ', content)
                        chunks = [chunk.strip() for chunk in chunks if len(chunk.strip()) > 20]
                        
                        with open("chunks.txt", "w", encoding="utf-8") as f:
                            for c in chunks:
                                f.write(c + "\n---\n")
                        
                        build_vector_database(chunks)
                        st.success("✅ PLAN.md processed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    # Main content area
    if st.session_state.vector_db_built:
        st.header("💬 Ask Questions")
        
        # Query interface
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question = st.text_input(
                "Your question:",
                placeholder="What would you like to know about your document?",
                key="question_input"
            )
        
        with col2:
            n_results = st.selectbox("Results:", [1, 2, 3, 4, 5], index=2)
        
        if st.button("🔍 Search", type="primary") or question:
            if question.strip():
                with st.spinner("Searching for relevant information..."):
                    try:
                        results = query_documents(question, n_results)
                        
                        if results and results['documents'][0]:
                            st.success(f"✅ Found {len(results['documents'][0])} relevant chunks:")
                            
                            # Display results in tabs
                            tabs = st.tabs([f"Result {i+1}" for i in range(len(results['documents'][0]))])
                            
                            for i, (tab, doc) in enumerate(zip(tabs, results['documents'][0])):
                                with tab:
                                    st.markdown("### 📝 Content")
                                    st.markdown(doc)
                                    
                                    # Show relevance score if available
                                    if 'distances' in results and results['distances'][0]:
                                        score = 1 - results['distances'][0][i]  # Convert distance to similarity
                                        st.progress(score)
                                        st.caption(f"Relevance: {score:.2%}")
                        else:
                            st.warning("❌ No relevant documents found. Try rephrasing your question.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during search: {str(e)}")
            else:
                st.warning("❓ Please enter a question.")
    
    else:
        # Welcome screen
        st.header("🚀 Welcome!")
        st.markdown("""
        ### Get started in 2 easy steps:
        
        1. **📄 Upload a document** (or process existing PLAN.md) using the sidebar
        2. **💬 Ask questions** about your document content
        
        This system uses advanced AI to understand your questions and find relevant information from your documents.
        """)
        
        # Show sample questions
        st.subheader("💡 Sample Questions")
        sample_questions = [
            "What is the main topic of this document?",
            "Can you summarize the key points?",
            "What are the important steps mentioned?",
            "Tell me about the implementation details",
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(sample_questions):
            with cols[i % 2]:
                st.markdown(f"• {question}")

if __name__ == "__main__":
    main()
