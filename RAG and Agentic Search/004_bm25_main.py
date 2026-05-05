from bm25Index_implement import BM25Index
from utils import chunk_by_section

with open("./report.md", "r") as f:
    text = f.read()

# 1. Chunk the text by section
chunks = chunk_by_section(text)

# 2. Create a BM25 store and add each chunk to it
bm25 = BM25Index()

for chunk in chunks:
    bm25.add_document({"content": chunk})

# 2. Create a BM25 store and add each chunk to it
query = "What happened with INC-2023-Q4-011?"

# 3. Search the store
results = bm25.search(query, k=3)

for doc, distance in results:
    print(f"Distance: {distance:.4f}")
    print(f"Content: {doc['content']}\n")