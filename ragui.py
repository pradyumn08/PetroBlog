import os
import streamlit as st
import requests
from datetime import datetime
import asyncio
import nest_asyncio
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Get API tokens from environment variables
ZILLIZ_URI = os.getenv('ZILLIZ_URI')
ZILLIZ_TOKEN = os.getenv('ZILLIZ_TOKEN')
HF_TOKEN = os.getenv('HF_TOKEN')
HF_INFERENCE_MODEL_ID = os.getenv('HF_INFERENCE_MODEL_ID', 'mistralai/Mistral-7B-Instruct-v0.1')

# Validate Zilliz token
def validate_zilliz_token():
    try:
        from pymilvus import connections
        connections.connect(
            alias="default",
            uri=ZILLIZ_URI,
            token=ZILLIZ_TOKEN
        )
        return True
    except Exception as e:
        st.error(f"Zilliz connection error: {str(e)}")
        return False

# Validate Hugging Face token
def validate_hf_token():
    try:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        response = requests.get("https://huggingface.co/api/models", headers=headers)
        return response.status_code == 200
    except Exception as e:
        st.error(f"Hugging Face API error: {str(e)}")
        return False

# Set page config
st.set_page_config(
    page_title="PetroBlog RAG",
    page_icon="🛢️",
    layout="wide"
)

# Initialize session state
if 'zilliz_valid' not in st.session_state:
    st.session_state.zilliz_valid = validate_zilliz_token()
if 'hf_valid' not in st.session_state:
    st.session_state.hf_valid = validate_hf_token()

# Sidebar
with st.sidebar:
    st.title("🛢️ PetroBlog RAG")
    st.markdown("---")
    
    # Display token validation status
    st.subheader("API Status")
    zilliz_status = "✅ Connected" if st.session_state.zilliz_valid else "❌ Not Connected"
    hf_status = "✅ Connected" if st.session_state.hf_valid else "❌ Not Connected"
    st.write(f"Zilliz: {zilliz_status}")
    st.write(f"Hugging Face: {hf_status}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This RAG application uses:
    - Zilliz Cloud for vector storage
    - Mistral-7B for question answering
    - PetroBlog content as knowledge base
    """)

# Main content
st.title("PetroBlog RAG Question Answering")
st.markdown("Ask questions about petroleum engineering topics based on PetroBlog content.")

# Query input
query = st.text_input("Enter your question:", placeholder="e.g., How does a sucker rod pump work?")

if query:
    if not (st.session_state.zilliz_valid and st.session_state.hf_valid):
        st.error("Please ensure both Zilliz and Hugging Face connections are valid.")
    else:
        try:
            with st.spinner("Searching for relevant content..."):
                # Initialize embeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )

                # Connect to Zilliz
                vector_store = Milvus(
                    embedding_function=embeddings,
                    collection_name="petroblog",
                    connection_args={
                        "uri": ZILLIZ_URI,
                        "token": ZILLIZ_TOKEN
                    }
                )

                # Create retriever
                retriever = vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                )

                # Get relevant documents
                docs = retriever.get_relevant_documents(query)
                
                if not docs:
                    st.warning("No relevant content found. Try rephrasing your question.")
                else:
                    # Display context
                    with st.expander("Relevant Content", expanded=True):
                        for i, doc in enumerate(docs, 1):
                            st.markdown(f"**Source {i}:**")
                            st.markdown(doc.page_content)
                            st.markdown("---")

                    # Initialize LLM
                    llm = HuggingFaceHub(
                        repo_id=HF_INFERENCE_MODEL_ID,
                        huggingfacehub_api_token=HF_TOKEN,
                        model_kwargs={
                            "temperature": 0.1,
                            "max_new_tokens": 512
                        }
                    )

                    # Create prompt template
                    template = """Use the following pieces of context to answer the question at the end. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.
                    Use three sentences maximum and keep the answer concise.

                    Context: {context}

                    Question: {question}
                    Answer:"""

                    prompt = PromptTemplate(
                        template=template,
                        input_variables=["context", "question"]
                    )

                    # Create QA chain
                    qa_chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=retriever,
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": prompt}
                    )

                    # Get answer
                    with st.spinner("Generating answer..."):
                        result = qa_chain({"query": query})
                        
                        st.markdown("### Answer")
                        st.markdown(result["result"])

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your API tokens and try again.") 