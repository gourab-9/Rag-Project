# 📚 AI-Powered Educational Content Generator

## Overview
This project is an AI-powered web application that processes educational content from uploaded documents and generates structured responses using Google Generative AI (Gemini). The application performs the following steps:

1. **Document Upload**: Users upload a PDF containing educational material.
2. **Text Extraction**: Extracts text from the uploaded document.
3. **Chunking & Embedding**: Splits text into manageable chunks and generates embeddings.
4. **Storage**: Stores both the raw document and its embeddings for retrieval.
5. **Query Processing**: Users enter queries related to syllabus plans, question papers, assignments, or topic explanations.
6. **Retrieval & Response Generation**: Relevant content is retrieved using FAISS and processed by Gemini AI to generate structured responses.

---
## 🛠 Installation & Setup

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Streamlit
- `pip` (Python package manager)
- Google Generative AI API key

### Installation Steps

1. **Clone the Repository**
   ```sh
   git clone https://github.com/gourab-9/Rag-Project.git
   cd edu-content-gen
   ```

2. **Create a Virtual Environment (Optional but Recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   - Create a `.env` file in the root directory.
   - Add your API key:
     ```sh
     GOOGLE_API_KEY=your_api_key_here
     ```

5. **Run the Application**
   ```sh
   streamlit run app.py
   ```

---
## 📖 Usage

1. **Upload a PDF file** containing educational content.
2. **Select Grade & Content Type** (Syllabus Plan, Question Paper, Assignments, Topic Explanations).
3. **Enter Query** related to the selected content type.
4. **Generate Response** – The AI will process and display relevant content.

---
## 📌 Features
- 📄 PDF Upload & Text Extraction
- 🔍 Semantic Search using FAISS
- 🤖 AI-Powered Content Generation (Gemini)
- 📂 Local Embedding Storage
- 📊 Query-Based Content Retrieval

---
## 🚀 Future Improvements
- **Multi-Document Processing**
- **Fine-Tuning for Specific Subjects**
- **Support for Additional Content Types**
- **Cloud-Based Embedding Storage (e.g., Pinecone, Chroma)**

---
## 🤝 Contributing
Feel free to fork, modify, and submit a pull request to enhance the project!

---
## 📜 License
This project is licensed under the MIT License.
