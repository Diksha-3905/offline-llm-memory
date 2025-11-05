from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
import os

# Initialize Chroma client (local storage)
client = chromadb.Client()
collection = client.get_or_create_collection(name="org_memory")

# Path to your PDF folder
pdf_folder = "data_pdfs"

# Create the folder if it doesn't exist
os.makedirs(pdf_folder, exist_ok=True)

# Load embedding model (you can use 'all-MiniLM-L6-v2' which is small and fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Loop through all PDFs and add to Chroma
for file_name in os.listdir(pdf_folder):
    print("Files found:", os.listdir(pdf_folder))
    if file_name.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file_name)
        print(f"📄 Reading: {file_name}")

        # Extract text from PDF
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        # Split into chunks
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        # Embed each chunk
        embeddings = model.encode(chunks).tolist()

        # Add to Chroma
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"{file_name}_{i}" for i in range(len(chunks))]
        )

print("✅ All PDFs embedded and stored locally!")
