import pymilvus
from pymilvus import connections, Collection, utility
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_milvus import Milvus

ZILLIZ_URI = "https://in03-d6505f2f16714f9.serverless.gcp-us-west1.cloud.zilliz.com"
ZILLIZ_TOKEN = "b6b5e5e8736b326cf30be7f05abdd33baec8077d90f6d18cd72994ad0db17e7e9ece7436efa2a7152f9cc525f6397cddfb12aa4b"
COLLECTION_NAME = "math_aware_chunks"
EMB_MODEL = "BAAI/bge-large-en-v1.5"

query = "3-D Discrete Fracture Flow Simulations Using Monterey Formation Fracture Data"

try:
    # Connect to Zilliz
    connections.connect(
        alias="default",
        uri=ZILLIZ_URI,
        token=ZILLIZ_TOKEN
    )
    print("Successfully connected to Zilliz Cloud.")

    if utility.has_collection(COLLECTION_NAME):
        collection = Collection(COLLECTION_NAME)
        print(f"Collection '{COLLECTION_NAME}' exists.")
        # No need to load for just getting schema and count here, but needed for search
        collection.load()
        print("Collection loaded for searching.")
        
        # Initialize embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name=EMB_MODEL,
            model_kwargs={'device': 'cpu'}
        )

        # Initialize Milvus vector store
        vector_store = Milvus(
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
            connection_args={
                "uri": ZILLIZ_URI,
                "token": ZILLIZ_TOKEN
            }
        )

        # Perform similarity search
        print(f"Searching for: {query}")
        docs = vector_store.similarity_search(query, k=5) # Fetch top 5 results

        if docs:
            print(f"Found {len(docs)} relevant documents:")
            for i, doc in enumerate(docs):
                print(f"--- Document {i+1} ---")
                print(f"Content: {doc.page_content[:200]}...") # Print first 200 chars
                print(f"Source: {doc.metadata.get('rel_path', 'N/A')}")
        else:
            print("No relevant documents found for the query in the collection.")

        collection.release() # Release collection after search
        print("Collection released.")

    else:
        print(f"Collection '{COLLECTION_NAME}' does not exist.")

except Exception as e:
    print(f"Error during Zilliz query: {e}") 