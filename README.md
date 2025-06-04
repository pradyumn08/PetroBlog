# PetroBlog RAG Application

A Retrieval-Augmented Generation (RAG) application built with Streamlit that provides intelligent question answering about petroleum engineering topics using the PetroBlog content.

## Features

- Semantic search over PetroBlog content using Zilliz vector database
- Question answering powered by Mistral-7B-Instruct model via Hugging Face
- Clean and intuitive Streamlit interface
- Token validation for API connections
- Asynchronous processing for better performance

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/petroblog-rag.git
cd petroblog-rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run ragui.py
```

## Configuration

The application uses the following configuration:

- Zilliz Cloud for vector storage
- Hugging Face API for inference
- Streamlit for the web interface

API tokens are configured in the application code since this is a private repository.

## Usage

1. Enter your question in the text input field
2. The application will:
   - Search for relevant content in the PetroBlog database
   - Generate a comprehensive answer using the Mistral model
   - Display both the answer and the source content

## Development

The application is built with:
- Streamlit for the web interface
- LangChain for RAG implementation
- Zilliz/Milvus for vector storage
- Hugging Face for model inference

## License

Private repository - All rights reserved 