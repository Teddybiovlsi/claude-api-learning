from utils import chunk_by_char, chunk_by_section, chunk_by_sentence, generate_embedding

if __name__ == "__main__":
    with open("./report.md") as f:
        document_text = f.read()

    chunks = chunk_by_section(document_text)

    embedding_chunk = generate_embedding(chunks[0])
    print("Embedding for the first chunk:")
    print(embedding_chunk)



