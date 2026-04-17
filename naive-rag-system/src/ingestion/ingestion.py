#1. load the pdf from data folder
# 2. extract the text from the pdf
# 3. split the text into chunks
#     3.1 we can use a simple split method like splitting
#     3.2 follow proper chunking strategy
#     3.3 chunk size = x tokens
#     3.4 chunk overlap = y tokens
# 4. create embeddings for the chunks
#     4.1 choose the embedding model (gemini-embedding-2-preview or gemini-embedding-001)
#     4.2 choose the dimension of the embeddings
#     4.3 create the embeddings for each chunk
# 5. store the embeddings in a vector database
#     5.1 our preferred vector db is pgvector
#     5.2 we have to activate pgvector extension in our postgres db
#     5.3 we have to create a table to store the embeddings
#     5.4 we have to insert the embeddings into the table with metadata

from dotenv import load_dotenv
import os
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.core.db import get_vector_store

load_dotenv()
PG_CONNECTION = os.getenv("PG_CONNECTION_STRING")

def ingest_pdf(file_path):
    """Ingest a PDF file and save it in vector database"""
    #1. load the pdf from data folder and making them as langchain documents
    loader = UnstructuredPDFLoader(file_path,mode="paged")
    docs = loader.load()
    print("Pages: " + str(len(docs)))

    #2. enrich the document with metadata
    for doc in docs:
        #add the file path, page number, and other relevant metadata to the document
        doc.metadata.update({
            "source": file_path,
            "document_extension": "pdf",
            "page": doc.metadata.get("page,None"),
            "category": "hr_support_desk",
            "last_updated": os.path.getmtime(file_path)
        })

    #3. split the text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, #character based chunking
        chunk_overlap=100 #overlap of 100 characters between chunks
    )

    chunks = splitter.split_documents(docs)
    print("Chunks: "+str(len(chunks)))

    #4 + 5 Embeddings + store the embeddings in a vector database
    vector_store = get_vector_store(collection_name = "hr_support_desk")

    vector_store.add_documents(chunks)
    print("Ingestion completed successfully")

if __name__=="__main__":
    ingest_pdf("data/RIL-Media-Release-RIL-Q2-FY2024-25-Financial-and-Operational-Performance.pdf")