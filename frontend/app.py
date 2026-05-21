# =========================
# IMPORTS
# =========================

import os
import json
import time
import tempfile
import sqlite3
import bcrypt
import streamlit as st

from dotenv import load_dotenv

# =========================
# LANGGRAPH IMPORTS
# =========================

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

# =========================
# LANGCHAIN IMPORTS
# =========================

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_groq import ChatGroq

from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

# =========================
# LOAD ENV
# =========================

load_dotenv()

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Enterprise Multi-Agent RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================
# REMOVE TOP GAP
# =========================

st.markdown("""
<style>

.block-container {

    padding-top: 1.5rem;
    padding-bottom: 0rem;
    max-width: 100%;
}

</style>
""", unsafe_allow_html=True)

# =========================
# AUTH SESSION
# =========================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False

if "username" not in st.session_state:

    st.session_state.username = ""

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE,

    password BLOB
)

""")

conn.commit()

# =========================
# CREATE USER
# =========================

def create_user(username, password):

    username = username.strip()

    if len(username) < 3:

        return False

    if len(password) < 6:

        return False

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(
            """
            INSERT INTO users (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (
                username,
                hashed_password
            )
        )

        conn.commit()

        return True

    except:

        return False

# =========================
# LOGIN USER
# =========================

def login_user(username, password):

    cursor.execute(
        """
        SELECT password
        FROM users
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()

    if result:

        stored_password = result[0]

        if bcrypt.checkpw(
            password.encode(),
            stored_password
        ):

            return True

    return False

# =========================
# USER MEMORY FILE
# =========================

def get_memory_file():

    username = st.session_state.username

    return f"memory_{username}.json"

# =========================
# LOGIN PAGE
# =========================

if not st.session_state.authenticated:

    st.markdown("""

    <style>

    .stApp {

        background: linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #1e3a8a
        );
    }

    .auth-box {

        width: 450px;

        margin: auto;

        margin-top: 80px;

        padding: 40px;

        background: rgba(255,255,255,0.06);

        border: 1px solid rgba(255,255,255,0.08);

        border-radius: 24px;

        backdrop-filter: blur(16px);
    }

    .stSelectbox label,
    .stTextInput label {

        color: #facc15 !important;

        font-weight: 700 !important;

        font-size: 16px !important;
    }

    .stTextInput input {

        color: black !important;

        background: rgba(255,255,255,0.95) !important;

        border-radius: 12px !important;

        border: 1px solid rgba(255,255,255,0.12) !important;

        font-weight: 600 !important;
    }

    </style>

    """, unsafe_allow_html=True)

    st.markdown("""

    <div class="auth-box">

    <h1 style="
        text-align:center;
        color:white;
        margin-bottom:30px;
    ">
    🔐 Enterprise AI Platform
    </h1>

    </div>

    """, unsafe_allow_html=True)

    auth_option = st.selectbox(
        "Select Option",
        ["Login", "Signup"]
    )

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if auth_option == "Signup":

        if st.button("Create Account"):

            success = create_user(
                username,
                password
            )

            if success:

                st.success(
                    "Account created successfully!"
                )

            else:

                st.error(
                    "Username exists or password too short."
                )

    else:

        if st.button("Login"):

            success = login_user(
                username,
                password
            )

            if success:

                st.session_state.authenticated = True

                st.session_state.username = username

                st.success("Login successful!")

                st.rerun()

            else:

                st.error(
                    "Invalid username or password"
                )

    st.stop()

# =========================
# CUSTOM CSS
# =========================

st.markdown("""

<style>

.stApp {

    background: linear-gradient(
        135deg,
        #020617,
        #0f172a,
        #1e3a8a
    );

    color: white;
}

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #020617,
        #081028,
        #0f172a
    );

    border-right: 1px solid rgba(255,255,255,0.08);

    width: 320px !important;

    min-width: 320px !important;

    padding-top: 10px;
}

section[data-testid="stSidebar"] * {

    color: #ffffff !important;
}

.main-title {

    font-size: 46px;

    font-weight: 900;

    color: white;

    margin-bottom: 8px;
}

.subtitle {

    font-size: 22px;

    color: #cbd5e1;

    margin-bottom: 30px;
}

.stChatMessage {

    background: linear-gradient(
        145deg,
        rgba(255,255,255,0.05),
        rgba(255,255,255,0.03)
    );

    border: 1px solid rgba(255,255,255,0.08);

    padding: 18px;

    border-radius: 22px;

    margin-bottom: 18px;

    backdrop-filter: blur(12px);

    box-shadow:
        0 8px 30px rgba(0,0,0,0.25);

    color: white !important;
}

.stChatMessage p,
.stChatMessage div,
.stChatMessage span,
.stChatMessage li {

    color: white !important;
}

.stChatInput input {

    background: rgba(255,255,255,0.04) !important;

    color: white !important;

    border-radius: 20px !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    padding: 18px !important;

    font-size: 16px !important;

    backdrop-filter: blur(10px);

    box-shadow:
        0 4px 20px rgba(0,0,0,0.2);
}

section[data-testid="stFileUploader"] {

    background: rgba(255,255,255,0.03);

    padding: 18px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.08);
}

.history-box {

    background: rgba(255,255,255,0.06);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 14px;

    border-radius: 14px;

    margin-bottom: 12px;

    color: white;
}

.history-box:hover {

    background: rgba(59,130,246,0.18);

    border: 1px solid rgba(96,165,250,0.5);
}

.source-box {

    background: rgba(255,255,255,0.08);

    border: 1px solid rgba(255,255,255,0.10);

    padding: 12px;

    border-radius: 12px;

    margin-bottom: 10px;

    color: white !important;
}

.stButton button {

    width: 100%;

    border-radius: 14px;

    background: rgba(255,255,255,0.05);

    color: white;

    border: 1px solid rgba(255,255,255,0.08);

    padding: 10px;

    transition: 0.3s;
}

.stButton button:hover {

    background: rgba(59,130,246,0.25);

    border: 1px solid rgba(59,130,246,0.5);
}

</style>

""", unsafe_allow_html=True)

# =========================
# LOAD MEMORY
# =========================

def load_memory():

    try:

        with open(get_memory_file(), "r") as f:

            data = json.load(f)

            return (
                data.get("messages", []),
                data.get("summary", "")
            )

    except:

        return [], ""

# =========================
# SAVE MEMORY
# =========================

def save_memory(messages, summary):

    data = {
        "messages": messages,
        "summary": summary
    }

    with open(get_memory_file(), "w") as f:

        json.dump(data, f)

# =========================
# SESSION MEMORY
# =========================

if "messages" not in st.session_state:

    messages, summary = load_memory()

    st.session_state.messages = messages

    st.session_state.conversation_summary = summary

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(f"""

    <div style="
        font-size:24px;
        font-weight:800;
        margin-bottom:20px;
        color:white;
    ">

    👤 {st.session_state.username}

    </div>

    """, unsafe_allow_html=True)

    st.markdown("""

    <div style="
        font-size:34px;
        font-weight:800;
        margin-bottom:25px;
        color:white;
    ">

    💬 Conversation History

    </div>

    """, unsafe_allow_html=True)

    user_messages = [

        msg["content"]

        for msg in st.session_state.messages

        if msg["role"] == "user"
    ]

    recent_messages = user_messages[-10:]

    if len(recent_messages) == 0:

        st.markdown("""

        <div class="history-box">
        No conversations yet
        </div>

        """, unsafe_allow_html=True)

    for msg in reversed(recent_messages):

        st.markdown(
            f"""

            <div class="history-box">
            🗨️ {msg[:35]}
            </div>

            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""

    <div style="
        font-size:24px;
        font-weight:700;
        margin-top:20px;
        margin-bottom:20px;
        color:white;
    ">

    ⚡ Tech Stack

    </div>

    """, unsafe_allow_html=True)

    tech_stack = [

        "LangChain",
        "LangGraph",
        "FAISS Vector DB",
        "Groq LLM",
        "HuggingFace Embeddings",
        "Streamlit",
        "Persistent AI Memory",
        "Streaming AI",
        "Multi-Agent AI"
    ]

    for tech in tech_stack:

        st.markdown(f"• {tech}")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.session_state.conversation_summary = ""

        save_memory([], "")

        st.rerun()

    if st.button("🚪 Logout"):

        st.session_state.authenticated = False

        st.session_state.username = ""

        st.rerun()

# =========================
# TITLE
# =========================

st.markdown(
    '<div class="main-title">Enterprise Multi-Agent RAG Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Enterprise Knowledge Intelligence System</div>',
    unsafe_allow_html=True
)

# =========================
# PDF UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload Enterprise PDFs",
    type=["pdf"]
)

# =========================
# EMBEDDINGS
# =========================

@st.cache_resource
def load_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

embeddings = load_embeddings()

# =========================
# LOAD VECTORSTORE
# =========================

@st.cache_resource
def load_vectorstore(_embeddings):

    vectorstore = FAISS.load_local(
        "vectorstore",
        _embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore

# =========================
# INITIALIZE VECTORSTORE
# =========================

base_vectorstore = load_vectorstore(embeddings)

vectorstore = base_vectorstore

# =========================
# HANDLE PDF UPLOAD
# =========================

if uploaded_file:

    with st.spinner("Processing PDF..."):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as tmp_file:

            tmp_file.write(uploaded_file.read())

            temp_pdf_path = tmp_file.name

        loader = PyPDFLoader(temp_pdf_path)

        documents = loader.load()

        for doc in documents:

            doc.metadata["source"] = uploaded_file.name

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.split_documents(documents)

        uploaded_vectorstore = FAISS.from_documents(
            docs,
            embeddings
        )

        vectorstore = uploaded_vectorstore

    st.success("PDF Uploaded Successfully!")

# =========================
# LLM
# =========================

@st.cache_resource
def load_llm():

    return ChatGroq(
        groq_api_key=st.secrets["GROQ_API_KEY"],
        model_name="llama-3.3-70b-versatile"
    )

llm = load_llm()

# =========================
# LANGGRAPH STATE
# =========================

class GraphState(TypedDict):

    question: str

    context: str

    answer: str

    agent_type: str

    chat_history: str

# =========================
# ROUTER NODE
# =========================

def router_node(state):

    question = state["question"].lower()

    if (
        "summary" in question
        or "summarize" in question
    ):

        return {
            "agent_type": "summary"
        }

    elif (
        "explain" in question
        or "simple" in question
    ):

        return {
            "agent_type": "explain"
        }

    else:

        return {
            "agent_type": "qa"
        }

# =========================
# QA NODE
# =========================

def qa_node(state):

    prompt = f"""

    You are a professional enterprise QA assistant.

    Use ONLY provided context.

    Chat History:
    {state['chat_history']}

    Context:
    {state['context']}

    Question:
    {state['question']}

    """

    return {
        "answer": prompt
    }

# =========================
# SUMMARY NODE
# =========================

def summary_node(state):

    prompt = f"""

    Summarize clearly in bullet points.

    Context:
    {state['context']}

    """

    return {
        "answer": prompt
    }

# =========================
# EXPLAIN NODE
# =========================

def explain_node(state):

    prompt = f"""

    Explain in beginner-friendly language.

    Context:
    {state['context']}

    """

    return {
        "answer": prompt
    }

# =========================
# BUILD LANGGRAPH
# =========================

workflow = StateGraph(GraphState)

workflow.add_node(
    "router",
    router_node
)

workflow.add_node(
    "qa",
    qa_node
)

workflow.add_node(
    "summary",
    summary_node
)

workflow.add_node(
    "explain",
    explain_node
)

# =========================
# ROUTING
# =========================

def route_decision(state):

    if state["agent_type"] == "summary":

        return "summary"

    elif state["agent_type"] == "explain":

        return "explain"

    else:

        return "qa"

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    route_decision,
    {
        "qa": "qa",
        "summary": "summary",
        "explain": "explain"
    }
)

workflow.add_edge("qa", END)

workflow.add_edge("summary", END)

workflow.add_edge("explain", END)

graph = workflow.compile()

# =========================
# MEMORY SUMMARIZER
# =========================

def summarize_conversation(messages):

    conversation_text = ""

    for msg in messages:

        conversation_text += f"""

        {msg['role']}:
        {msg['content']}

        """

    summary_prompt = f"""

    Summarize this conversation briefly.

    Focus on:
    - important topics
    - user intent
    - discussed concepts

    Conversation:
    {conversation_text}

    """

    summary_response = llm.invoke(
        summary_prompt
    )

    return summary_response.content

# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if "sources" in message:

            st.markdown("### 📚 Sources")

            for source in message["sources"]:

                st.markdown(
                    f"""

                    <div class="source-box">
                    📄 {source}
                    </div>

                    """,
                    unsafe_allow_html=True
                )

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input(
    "Ask your enterprise documents..."
)

# =========================
# CHAT FLOW
# =========================

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    save_memory(
        st.session_state.messages,
        st.session_state.conversation_summary
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    # =========================
    # ADVANCED MEMORY
    # =========================

    if len(st.session_state.messages) > 8:

        old_messages = st.session_state.messages[:-4]

        summary = summarize_conversation(
            old_messages
        )

        st.session_state.conversation_summary = summary

        st.session_state.messages = (
            st.session_state.messages[-4:]
        )

        save_memory(
            st.session_state.messages,
            st.session_state.conversation_summary
        )

    # =========================
    # CHAT HISTORY
    # =========================

    chat_history = f"""

    Conversation Summary:
    {st.session_state.conversation_summary}

    """

    for message in st.session_state.messages:

        chat_history += f"""

        {message['role']}:
        {message['content']}

        """

    # =========================
    # RETRIEVAL
    # =========================

    docs = vectorstore.similarity_search_with_score(
        prompt,
        k=4
    )

    context = ""

    sources = []

    for doc, score in docs:

        try:

            context += (
                doc.page_content + "\n\n"
            )

            source = doc.metadata.get(
                "source",
                "Enterprise Knowledge Base"
            )

            page = doc.metadata.get(
                "page",
                0
            )

            sources.append(
                f"{source} | Page {page+1}"
            )

        except:

            continue

    # =========================
    # GRAPH EXECUTION
    # =========================

    result = graph.invoke({

        "question": prompt,

        "context": context,

        "answer": "",

        "agent_type": "",

        "chat_history": chat_history

    })

    prompt_for_llm = result["answer"]

    # =========================
    # STREAMING RESPONSE
    # =========================

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""

        stream = llm.stream(
            prompt_for_llm
        )

        for chunk in stream:

            try:

                content = chunk.content

                if content:

                    full_response += content

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

                    time.sleep(0.01)

            except:

                continue

        response_placeholder.markdown(
            full_response
        )

        # =========================
        # SOURCES
        # =========================

        if sources:

            st.markdown("### 📚 Sources")

            unique_sources = list(set(sources))

            for src in unique_sources:

                st.markdown(
                    f"""

                    <div class="source-box">
                    📄 {src}
                    </div>

                    """,
                    unsafe_allow_html=True
                )

        # =========================
        # MEMORY SUMMARY
        # =========================

        with st.expander(
            "🧠 Conversation Memory Summary"
        ):

            st.write(
                st.session_state.conversation_summary
            )

    # =========================
    # STORE AI RESPONSE
    # =========================

    st.session_state.messages.append({

        "role": "assistant",

        "content": full_response,

        "sources": sources

    })

    save_memory(
        st.session_state.messages,
        st.session_state.conversation_summary
    )
