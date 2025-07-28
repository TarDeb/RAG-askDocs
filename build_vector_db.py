from sentence_transformers import SentenceTransformer
import chromadb

# Load your chunks
with open("chunks.txt", encoding="utf-8") as f:
    raw_chunks = f.read().split("\n---\n")
chunks = [c.strip() for c in raw_chunks if c.strip()]

# Initialize model and database with persistent storage
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")

# Delete existing collection if it exists and create new one
try:
    client.delete_collection("md_chunks")
    print("🗑️ Deleted existing collection")
except:
    pass

collection = client.create_collection("md_chunks")

# Add each chunk as a document with its embedding
for i, chunk in enumerate(chunks):
    emb = model.encode(chunk).tolist()
    collection.add(documents=[chunk], embeddings=[emb], ids=[str(i)])

print(f"\nVector database built and ready! {len(chunks)} chunks processed.")

# Show embedding for first few chunks
# if i < 3:  # Show first 3 chunks
#     print(f"\n--- Chunk {i} ---")
#     print(f"Text: {chunk[:100]}...")  # First 100 characters
#     print(f"Embedding shape: {len(emb)} dimensions")
#     print(f"First 10 values: {emb[:10]}")
#     print(f"Embedding type: {type(emb[0])}")
