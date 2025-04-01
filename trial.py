import os
import time
from one_embed_store import create_faiss_index
from two_query_faiss import get_similar_chunks

def check_working():
    print("\n🔍 Checking module functionality...\n")

    # Test 1: FAISS Index Creation (Dummy PDF File Check)
    pdf_path = "science class 6.pdf"  # Change this to an actual PDF path
    if os.path.exists(pdf_path):
        print(f"📂 PDF Found: {pdf_path} - Proceeding with indexing...\n")
        create_faiss_index(pdf_path)
        print("✅ FAISS Index Created Successfully!\n")
    else:
        print(f"⚠️ Warning: PDF '{pdf_path}' not found. Skipping index creation.\n")

    time.sleep(2)

    # Test 2: Query FAISS Index (Dummy Query)
    test_query = "unit of length"
    print(f"🔎 Testing FAISS Query with: {test_query}\n")
    results = get_similar_chunks(test_query, top_k=3)

    if results:
        print("\n✅ FAISS Query Successful! Sample Results:\n")
        for i, chunk in enumerate(results, 1):
            print(f"🔹 **[{i}]** {chunk[:300]}...")  # Display first 300 chars
            print("-" * 80)
    else:
        print("⚠️ No results found. Please check the FAISS index or try another query.")

    print("\n✅ All tests completed!")

if __name__ == "__main__":
    check_working()
