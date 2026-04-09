from utils import chunk_by_char, chunk_by_section, chunk_by_sentence

if __name__ == "__main__":
    with open("./report.md") as f:
        document_text = f.read()

    # print("Chunking by character:")
    # char_chunks = chunk_by_char(document_text, 300, 30)
    # for i, chunk in enumerate(char_chunks):
    #     print(f"Chunk {i+1}:\n{chunk}\n")

    # print("Chunking by sentence:")
    # sentence_chunks = chunk_by_sentence(document_text)
    # for i, chunk in enumerate(sentence_chunks):
    #     print(f"Chunk {i+1}:\n{chunk}\n")

    # print("Chunking by section:")
    # section_chunks = chunk_by_section(document_text)
    # for i, chunk in enumerate(section_chunks):
    #     print(f"Chunk {i+1}:\n{chunk}\n")