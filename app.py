import streamlit as st 
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
import os
 
load_dotenv()

def main():
    st.header("LLM-powered PDF Chatbot (local Ollama) 💬")

    pdf = st.file_uploader("Upload your PDF", type='pdf')
 
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100000,
            chunk_overlap=2000,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        store_name = pdf.name[:-4]
        st.write(f'{store_name}')

        if os.path.exists(f"{store_name}.pkl"):
            with open(f"{store_name}.pkl", "rb") as f:
                VectorStore = pickle.load(f)
        else:
            embeddings = HuggingFaceEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)

        query = st.text_input("Ask questions about your PDF file:")

        if query:
            docs = VectorStore.similarity_search(query=query, k=3)

            llm = Ollama(model="mistral")  # Puedes cambiar a "llama2", "gemma", "mistral" etc.
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=query)

            st.write(response)

if __name__ == '__main__':
    main()

# Mantiene el footer y fondo
def set_bg_from_url(url, opacity=1):
    footer = """..."""  # omito por espacio, pero tu mismo HTML
    st.markdown(footer, unsafe_allow_html=True)
    st.markdown(
        f"""
        <style>
            body {{
                background: url('{url}') no-repeat center center fixed;
                background-size: cover;
                opacity: {opacity};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_from_url("https://www.1access.com/wp-content/uploads/2019/10/GettyImages-1180389186.jpg", opacity=0.875)
