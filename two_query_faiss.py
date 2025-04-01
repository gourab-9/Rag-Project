# import os
# from dotenv import load_dotenv
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# # Load API key from .env file
# load_dotenv()

# def get_similar_chunks(query, top_k=5):
#     if not query.strip():
#         print("⚠️ Error: Query cannot be empty.")
#         return []

#     embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

#     # Ensure FAISS index exists before loading
#     if not os.path.exists("faiss_index"):
#         print("❌ Error: FAISS index not found. Please run the embedding script first.")
#         return []

#     # Load FAISS index
#     vector_db = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
    
#     # Perform similarity search
#     similar_chunks = vector_db.similarity_search(query, k=top_k)

#     if not similar_chunks:
#         print("\n⚠️ No relevant results found.")
#         return []

#     print("\n🔍 **Top Relevant Chunks:**\n")
#     for i, chunk in enumerate(similar_chunks, 1):
#         content = chunk.page_content.replace("\n", " ").strip()
#         print(f"🔹 **[{i}]** {content}...")  # Show first 300 characters
#         print("-" * 80)  # Separator for better readability

#     return [chunk.page_content for chunk in similar_chunks]

# if __name__ == "__main__":
#     query = input("Enter your query: ").strip()
#     results = get_similar_chunks(query)


import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI

# Load API key from .env file
load_dotenv()

def get_similar_chunks(query, top_k=5):
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    # Load FAISS index
    vector_db = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
    
    # Get the query embedding
    query_embedding = embedding_model.embed_query(query)

    # Perform similarity search
    similar_chunks = vector_db.similarity_search(query, k=top_k)

    if not similar_chunks:
        print("\n⚠️ No relevant results found.")
        return []

    # Extract chunk content for context
    retrieved_text = "\n".join([chunk.page_content.strip() for chunk in similar_chunks])

    return retrieved_text

def generate_response(query):
    """Generate an AI response based on retrieved chunks."""
    retrieved_chunks = get_similar_chunks(query)

    if not retrieved_chunks:
        return "No relevant information found."

    # Initialize LLM model
    llm = GoogleGenerativeAI(model="gemini-2.0-flash")  # Ensure you have access to Gemini-Pro

    # Construct prompt with query and retrieved content
    prompt = f"""
    You are an AI assistant answering user queries. Use the relevant context below to provide a meaningful response:
    
    Context:
    {retrieved_chunks}

    User Query: {query}

    Provide a concise and informative response.
    """

    response = llm.invoke(prompt)
    return response

if __name__ == "__main__":
    query = input("Enter your query: ")
    response = generate_response(query)
    
    print("\n🔹 **AI-Generated Response:**\n")
    print(response)
