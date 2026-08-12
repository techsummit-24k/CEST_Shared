from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# 1. Load the physical file
loader = PyPDFLoader("Srinath_Jagannathan_Tech2.1.pdf")
raw_pdf_data = loader.load()

# 2. Split into multiple "Documents" (chunks)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
chunks = text_splitter.split_documents(raw_pdf_data)
OLLAMA_BASE_URL="http://localhost:11434"

# 3. Save to disk
vectorstore = Chroma.from_documents(
    documents=chunks, 
    embedding=OllamaEmbeddings(model="nomic-embed-text",base_url=OLLAMA_BASE_URL),
    persist_directory="./agent_db" # This folder is the "link"
)
print("Database created and saved to ./agent_db")