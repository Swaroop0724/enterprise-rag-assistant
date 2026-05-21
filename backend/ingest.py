import os

# PDF Loader
from langchain_community.document_loaders import PyPDFLoader

# Text Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# HuggingFace Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# FAISS Vector Store
from langchain_community.vectorstores import FAISS

# -----------------------------------
# DOCUMENTS PATH
# -----------------------------------

DOCUMENTS_PATH = "../documents"

# Store all loaded documents
all_docs = []

print("\nLoading PDF documents...\n")

# -----------------------------------
# LOAD PDFs
# -----------------------------------

for file in os.listdir(DOCUMENTS_PATH):

    # Process only PDF files
    if file.endswith(".pdf"):

        file_path = os.path.join(DOCUMENTS_PATH, file)

        print(f"Loading: {file}")

        # Load PDF
        loader = PyPDFLoader(file_path)

        docs = loader.load()

        # Store loaded pages
        all_docs.extend(docs)

print(f"\nTotal pages loaded: {len(all_docs)}")

# -----------------------------------
# TEXT CHUNKING
# -----------------------------------

print("\nChunking documents...\n")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(all_docs)

print(f"Total chunks created: {len(chunks)}")

# -----------------------------------
# GENERATE EMBEDDINGS
# -----------------------------------

print("\nGenerating embeddings...\n")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------------
# CREATE FAISS VECTOR DATABASE
# -----------------------------------

print("\nCreating FAISS vector database...\n")

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# -----------------------------------
# SAVE VECTOR DATABASE
# -----------------------------------

vectorstore.save_local("../vectorstore")

print("\nFAISS vector database created successfully!")