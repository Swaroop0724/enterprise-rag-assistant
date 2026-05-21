import os
from dotenv import load_dotenv

# FAISS Vector Store
from langchain_community.vectorstores import FAISS

# HuggingFace Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

# Groq LLM
from langchain_groq import ChatGroq

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

print("\nLoading embedding model...\n")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------------
# LOAD FAISS VECTOR DATABASE
# -----------------------------------

print("Loading FAISS vector database...\n")

vectorstore = FAISS.load_local(
    "../vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

print("FAISS database loaded successfully!\n")

# -----------------------------------
# CREATE RETRIEVER
# -----------------------------------

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# -----------------------------------
# LOAD LLM
# -----------------------------------

print("Loading LLM...\n")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)

print("LLM loaded successfully!\n")

# -----------------------------------
# QUESTION LOOP
# -----------------------------------

while True:

    query = input("\nAsk a question (type 'exit' to quit): ")

    if query.lower() == "exit":
        break

    # -----------------------------------
    # RETRIEVE RELEVANT DOCUMENTS
    # -----------------------------------

    docs = retriever.invoke(query)

    print("\nTop Retrieved Chunks:\n")

    context = ""

    for i, doc in enumerate(docs):

        print(f"\nChunk {i+1}:\n")

        print(doc.page_content[:500])

        context += doc.page_content + "\n"

    # -----------------------------------
    # CREATE PROMPT
    # -----------------------------------

    prompt = f"""
    You are an AI assistant.

    Answer the question ONLY using the provided context.

    Context:
    {context}

    Question:
    {query}
    """

    # -----------------------------------
    # GENERATE RESPONSE
    # -----------------------------------

    response = llm.invoke(prompt)

    print("\nAI Response:\n")

    print(response.content)