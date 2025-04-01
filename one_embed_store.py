import pdfplumber
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load API key from .env file
load_dotenv()

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File '{pdf_path}' not found.")
        return None
    
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    
    if not text.strip():
        print("⚠️ Warning: No text extracted from the PDF.")
        return None
    
    return text

def create_faiss_index(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        return  # Stop if no text is extracted
    
    # Chunking the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_text(text)

    if not chunks:
        print("⚠️ Warning: No chunks generated.")
        return

    print(f"✅ Total Chunks Generated: {len(chunks)}")

    # Initialize embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Debug: Print sample chunks before embedding
    print(f"🔹 Sample Chunk: {chunks[0]}...")  # Print first 300 chars of first chunk

    # Generate embeddings and store in FAISS
    vector_db = FAISS.from_texts(chunks, embedding_model)
    vector_db.save_local("faiss_index")

    print(f"✅ FAISS Index Created & Saved ({len(chunks)} Chunks)")

# Run script
if __name__ == "__main__":
    pdf_path = "science class 6.pdf"
    create_faiss_index(pdf_path)
