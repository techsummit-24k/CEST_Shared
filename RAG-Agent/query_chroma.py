# from langchain_chroma import Chroma

# # 1. Connect to your existing local folder
# db = Chroma(persist_directory="./agend_db")
# print(db._client.list_collections())

# # 2. Get the specific collection you want to search
# # Replace "your_collection_name" with the actual name of your collection
# collection = db._client.get_collection(name="langchain")

# # 3. Run your semantic query
# results = collection.query(
#     query_texts=["Srinath?"],
#     n_results=3
# )

# print(results)

import chromadb

# 1. Connect to your local persistent directory
client = chromadb.PersistentClient(path="./agent_db")

# 2. Get your collection
# (Change "your_collection_name" to match your actual collection name)
collection = client.get_collection(name="langchain")

# 3. Fetch the data and explicitly include embeddings and documents
storage_view = collection.get(
    include=["documents", "embeddings", "metadatas"]
)

# 4. Loop through and view the chunks and their vectors
# We use min() to prevent errors if the lists are empty
num_records = len(storage_view["ids"])

if num_records == 0:
    print("The collection is completely empty!")
else:
    print(f"Found {num_records} total chunks in this collection.\n")
    
    for i in range(min(5, num_records)):  # Showing first 5 chunks as a sample
        print(f"--- Record {i+1} ---")
        print(f"ID: {storage_view['ids'][i]}")
        print(f"Chunk Text: {storage_view['documents'][i]}")
        # Printing only the first 5 dimensions of the vector so it doesn't flood your screen
        vector_sample = storage_view['embeddings'][i][:5] 
        vector_len = len(storage_view['embeddings'][i])
        print(f"Embedding Vector (First 5 dimensions of {vector_len}): {vector_sample}...")
        print(f"Metadata: {storage_view['metadatas'][i]}\n")
