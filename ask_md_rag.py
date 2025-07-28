from sentence_transformers import SentenceTransformer
import chromadb

# Load model and vector DB from persistent storage
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")

# Try to get existing collection
try:
    collection = client.get_collection("md_chunks")
    print("✅ Connected to vector database!")
except:
    print("❌ Vector database not found. Please run 'python build_vector_db.py' first!")
    exit()

print("🤖 RAG Query System - Ask questions about your document!")
print("Type 'exit' to quit\n")

while True:
    try:
        question = input("📝 Your question: ")
        if question.lower() == "exit":
            print("👋 Goodbye!")
            break
        
        if not question.strip():
            print("❓ Please enter a valid question.")
            continue
        
        print("🔍 Searching...")
        q_emb = model.encode(question).tolist()
        results = collection.query(query_embeddings=[q_emb], n_results=3)
        
        if not results['documents'][0]:
            print("❌ No relevant documents found.")
            continue
        
        print(f"\n✅ Found {len(results['documents'][0])} relevant chunks:\n")
        for i, doc in enumerate(results["documents"][0], 1):
            print(f"--- Result {i} ---")
            print(f"{doc[:300]}...")
            print()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error: {e}")
        continue
