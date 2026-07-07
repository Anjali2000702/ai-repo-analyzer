import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# The folder where our database will be saved locally
CHROMA_PATH = "chroma_db"

def create_vector_db(extracted_folder_path: str):
    """
    Reads text files, splits them into chunks, and saves them to ChromaDB.
    """
    print(f"Scanning files in: {extracted_folder_path}...")
    documents = []

    # 1. Read all files in the extracted folder
    for root, _, files in os.walk(extracted_folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Read the file's text content
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    
                    # Store it as a LangChain Document with metadata (so the AI knows the file name later)
                    doc = Document(
                        page_content=text, 
                        metadata={"source": file_path, "filename": file}
                    )
                    documents.append(doc)
            except Exception as e:
                # If a file is unreadable (e.g., weird encoding), just skip it safely
                print(f"Skipping {file} due to read error: {e}")

    if not documents:
        raise ValueError("No readable text files found to index.")

    print(f"Loaded {len(documents)} files. Chunking them now...")

    # 2. Split the documents into smaller chunks
    # We chunk at 1000 characters. The 200 character overlap ensures we don't accidentally 
    # cut a function definition or important sentence in half!
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split files into {len(chunks)} chunks.")

    # 3. Create the Embeddings Model (100% Free via HuggingFace)
    # This translates human words/code into vectors (arrays of numbers)
    print("Initializing Embedding Model (this may take a moment to download the first time)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Save the chunks and embeddings into ChromaDB
    print("Saving to Chroma Vector Database...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    print(f"Successfully saved vector database to backend/{CHROMA_PATH}!")
    return db

# 4th file 