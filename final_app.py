import os
import streamlit as st
import pdfplumber
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import GoogleGenerativeAI

# Load API key
load_dotenv()

# Define paths
UPLOAD_FOLDER = "uploaded_docs"
FAISS_INDEX_PATH = "faiss_index"

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@st.cache_data  # Caches extracted text
def extract_text_from_pdf(pdf_path):
    """Extract text from PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])

@st.cache_data  # Caches FAISS index creation
def create_faiss_index(text):
    """Chunk text, generate embeddings, and store in FAISS."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_text(text)
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = FAISS.from_texts(chunks, embedding_model)
    vector_db.save_local(FAISS_INDEX_PATH)
    return len(chunks)

@st.cache_resource  # ✅ FAISS & embeddings must persist but are NOT serializable
def load_faiss_index():
    """Load FAISS index and embedding model (persists across app runs)."""
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_db = FAISS.load_local(FAISS_INDEX_PATH, embedding_model, allow_dangerous_deserialization=True)
    return vector_db, embedding_model

def get_similar_chunks(query, vector_db, embedding_model, top_k=5):
    """Retrieve relevant chunks using FAISS."""
    query_embedding = embedding_model.embed_query(query)
    similar_chunks = vector_db.similarity_search_by_vector(query_embedding, k=top_k)
    return [chunk.page_content for chunk in similar_chunks]

@st.cache_data  # Caches AI responses
def generate_response(query, retrieved_chunks, content_type):
    """Generate structured content using Gemini AI."""
    llm = GoogleGenerativeAI(model="gemini-2.0-flash")

    if content_type == "Topic Explanations":
        input_text = (
            f"User Query: {query}\n"
            f"Retrieved Content: {' '.join(retrieved_chunks)}\n"
            f"Generate a **detailed and structured explanation** for this topic."
        )
    else:
        input_text = f"User Query: {query}\nRetrieved Content: {' '.join(retrieved_chunks)}"
    
    return llm.invoke(input_text)

# Streamlit UI
st.title("📚 AI-Powered Educational Content Generator")

# File Upload
uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ File uploaded successfully!")
    extracted_text = extract_text_from_pdf(file_path)
    num_chunks = create_faiss_index(extracted_text)
    st.info(f"🔍 {num_chunks} chunks created and indexed.")

# Load FAISS (Only Runs Once)
vector_db, embedding_model = load_faiss_index()

# User Input Section
grade = st.selectbox("Select Grade", ["6th", "7th"])
chapter = st.text_input("Enter Chapter Name or Number")
content_type = st.selectbox("Select Content Type", ["Syllabus Plan", "Question Paper", "Assignments", "Topic Explanations"])

if content_type in ["Question Paper", "Assignments"]:
    difficulty = st.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"], horizontal=True)

query = st.text_area("Enter your query")
if st.button("Generate Content"):
    if query:
        retrieved_chunks = get_similar_chunks(query, vector_db, embedding_model)
        if retrieved_chunks:
            response = generate_response(query, retrieved_chunks, content_type)
            st.subheader("📌 Generated Content")
            st.write(response)
        else:
            st.warning("⚠️ No relevant content found in the database.")
    else:
        st.error("❌ Please enter a query.")
