🤖 Enterprise Multi-Agent RAG Assistant

An intelligent, multi-agent Retrieval-Augmented Generation (RAG) system built with LangChain, LangGraph, FAISS, Groq LLM, and Streamlit. Upload your enterprise PDFs and chat with them using AI — with persistent memory, smart routing, and a beautiful dark UI.

<img width="1920" height="982" alt="image" src="https://github.com/user-attachments/assets/0da3f477-149a-4fdd-ba5d-a166ba75619d" />
<img width="1920" height="979" alt="image" src="https://github.com/user-attachments/assets/d5c61641-9a8a-47ed-80c4-3fa3928d55a3" />
Preview

A stunning dark-themed enterprise AI assistant with login, PDF upload, intelligent multi-agent routing, streaming responses, and persistent memory per user.


✨ Features

🔐 User Authentication — Secure signup/login with bcrypt password hashing and SQLite database
📄 PDF Upload & Ingestion — Upload multiple enterprise PDFs at runtime, auto-chunked and embedded
🧠 Multi-Agent Routing — LangGraph-powered intelligent router that picks the right agent:

QA Agent — Answers specific questions from documents
Summary Agent — Summarizes content in bullet points
Explain Agent — Explains concepts in beginner-friendly language


🔍 FAISS Vector Search — Lightning-fast semantic similarity search across all document chunks
💬 Streaming Responses — Real-time token-by-token output like ChatGPT
🧩 Persistent Memory — Per-user conversation memory saved as JSON, survives page refresh
📚 Source Citations — Every answer shows which document and page it came from
🎨 Beautiful Dark UI — Custom CSS with glassmorphism design, gradient backgrounds
📊 Conversation Summary — Auto-summarizes long conversations to maintain context

🏗️ Project Structure
<img width="667" height="764" alt="image" src="https://github.com/user-attachments/assets/e7451ecf-3b90-41ca-a531-c7a9efff12dd" />

🧠 Architecture
<img width="447" height="685" alt="image" src="https://github.com/user-attachments/assets/78de45f3-179b-43cf-b99a-a6dce9929df5" />

    🛠️ Tech Stack
    <img width="663" height="460" alt="image" src="https://github.com/user-attachments/assets/f3ce3494-ccb8-4c9d-923a-e09a219007d1" />

    🚀 Getting Started Locally
1. Clone the repository
   git clone https://github.com/Swaroop0724/enterprise-rag-assistant.git
   cd enterprise-rag-assistant

2. Create and activate virtual environment
   python -m venv venv

  # Windows
  venv\Scripts\activate
  
  # Mac/Linux
  source venv/bin/activate

3. Install dependencies
   pip install -r requirements.txt

4. Set up environment variables
    Create frontend/.env:
    GROQ_API_KEY=your_groq_api_key_here
    Create backend/.env:
    GROQ_API_KEY=your_groq_api_key_here
    Get your free Groq API key at console.groq.com

5. Build the vector database (optional — already pre-built)
   cd backend
   python ingest.py

   This loads all PDFs from the documents/ folder, creates embeddings, and saves to vectorstore/.

6. Run the app
   cd frontend
   streamlit run app.py

   Open http://localhost:8501 in your browser.

☁️ Streamlit Cloud Deployment
1. Push to GitHub
Make sure your repo is on GitHub without .env files or venv/.
2. Deploy on Streamlit Cloud

Go to share.streamlit.io
Click New App
Select your repo: Swaroop0724/enterprise-rag-assistant
Set Main file path to: frontend/app.py
Click Advanced Settings → Secrets and add:

GROQ_API_KEY = "your_groq_api_key_here"

3. Click Deploy!
🔐 Authentication System
The app uses a secure login/signup system:

Passwords are hashed using bcrypt before storage
Users are stored in a local SQLite database (users.db)
Each user gets their own memory file (memory_<username>.json)
Session state tracks login across page interactions

🧩 How the Multi-Agent System Works
The LangGraph workflow routes every question to the most appropriate agent:
<img width="562" height="173" alt="image" src="https://github.com/user-attachments/assets/6d8507e8-b59d-4ac2-9a09-9a0d642fa5b0" />

Each agent builds a specialized prompt injected with:

Retrieved FAISS context (top 4 chunks)
Full conversation history
Running conversation summary

💾 Memory System
Each user has persistent memory that survives page refreshes:

Messages are saved in memory_<username>.json
When conversation exceeds 8 messages, older messages are auto-summarized using the LLM
The summary is injected into every future prompt for contextual awareness
Memory is loaded on login and saved after every message

📄 Documents Included
The pre-built vector store contains content from:

Chapter 1.1 — Introduction to Big Data
Chapter 1.2 — Big Data Processing Systems (Hadoop, Spark, Storm, Dryad, Pregel)
Chapter 5.1 — Data Learning Methods (Bayes Rule, Naïve Bayes)
Chapter 5.2 — More Data Learning Methods
Chapter 5.3 — Advanced Learning Concepts
Chapter 6.1 & 6.2 — Additional Data Science Topics

All from CSCE 5300: Introduction to Big Data and Data Science

📦 Key Dependencies
streamlit
langchain
langchain-community
langchain-groq
langchain-huggingface
langgraph
faiss-cpu
sentence-transformers
bcrypt
python-dotenv
pypdf

🙋‍♂️ Author
Jyothi Swaroop Ganapavarapu

GitHub: @Swaroop0724
Project: Enterprise Multi-Agent RAG Assistant

🌟 If you found this useful, give it a star on GitHub!


