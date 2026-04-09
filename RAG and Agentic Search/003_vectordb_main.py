from utils import chunk_by_section, generate_embedding_v2
from vectorIndex_implement import VectorIndex

if __name__ == "__main__":
    with open("./report.md") as f:
        document_text = f.read()
    # 1. Chunk the text by section
    chunks = chunk_by_section(document_text)
    # 2. Generate embeddings for each chunk
    embeddings = generate_embedding_v2(chunks)
    # 3. Create a vector store and add each embedding to it
    # Note: converted to a bulk operation to avoid rate limiting errors from VoyageAI
    store = VectorIndex()
    for embedding, chunk in zip(embeddings, chunks):
        store.add_vector(embedding, {"content": chunk})
    # 4. Some time later, a user will ask a question. Generate an embedding for it
    user_embedding = generate_embedding_v2("What are the key findings of the report?")
    # 5. Search the store with the embedding, find the 2 most relevant chunks
    results = store.search(user_embedding, k=2)

    for doc, score in results:
        print(f"Score: {score:.4f}")
        print(f"Content: {doc['content']}\n")