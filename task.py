import streamlit as st
import PyPDF2
import google.generativeai as genai
import os

# Configure Gemini API
GOOGLE_API_KEY = "Your API KEY"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to extract text from uploaded PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        extracted_text = page.extract_text()
        if extracted_text:
            text += extracted_text + "\n"
    return text.strip()

# Function to generate AI-based educational content using Gemini
def generate_content(textbook_text, grade, chapter, content_type, difficulty):
    prompt = f"""
    You are an AI assistant helping to generate structured educational content for Grade {grade} Science.
    
    Given the following chapter text, create the requested content:
    
    **Chapter Name:** {chapter}
    **Content Type:** {content_type}
    **Difficulty Level:** {difficulty}
    
    **Textbook Content:** 
    {textbook_text[:2000]}  # Limiting input text to prevent token overflow

    Generate well-structured and age-appropriate content following the Karnataka State Board Science syllabus.
    """
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating content: {str(e)}"

# Streamlit App UI
st.set_page_config(page_title="Educational Content Generator", layout="wide")
st.title("📚 AI-Powered Educational Content Generator")
st.sidebar.header("Upload Textbook & Settings")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload Karnataka Board Science Textbook (PDF)", type=["pdf"])

# User Selections
grade = st.sidebar.selectbox("Select Grade", ["6th", "7th"])
chapter = st.sidebar.text_input("Enter Chapter Name or Number")
content_type = st.sidebar.selectbox("Select Content Type", ["Syllabus Plan", "Question Paper", "Assignments", "Topic Explanations"])
difficulty = st.sidebar.radio("Select Difficulty Level", ["Easy", "Medium", "Hard"])

if uploaded_file is not None:
    with st.spinner("Extracting Text..."):
        textbook_text = extract_text_from_pdf(uploaded_file)

    # Display extracted text (for debugging)
    st.subheader("Extracted Text Preview")
    st.text_area("Textbook Content", textbook_text, height=200)

    # Generate Content Button
    if st.button("Generate Content"):
        with st.spinner("Generating AI-based content..."):
            generated_content = generate_content(textbook_text, grade, chapter, content_type, difficulty)

        st.subheader("Generated Content")
        st.write(generated_content)

# Footer
st.markdown("---")
st.markdown("Developed by Mr. Singh | Powered by Gemini AI 🤖")
