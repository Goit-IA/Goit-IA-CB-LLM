import streamlit as st 
from dotenv import load_dotenv
import pickle
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
#from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain.llms import Ollama
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document

load_dotenv()

def load_pdfs_from_folder(folder_path):
    all_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            pdf_reader = PdfReader(pdf_path)
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    all_text += text
    return all_text

def main():
    st.header("LLM-powered PDF Chatbot (folder mode + strict answers) 💬")

    folder_path = "./pdfs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        st.warning(f"La carpeta '{folder_path}' ha sido creada. Añade archivos PDF allí.")
        return

    # Leer todos los PDFs
    all_text = load_pdfs_from_folder(folder_path)
    if not all_text.strip():
        st.warning("No se encontró texto en los PDFs de la carpeta.")
        return

    # Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(all_text)

    store_name = "vectorstore_pdfs"
    if os.path.exists(f"{store_name}.pkl"):
        with open(f"{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:
        embeddings = HuggingFaceEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        with open(f"{store_name}.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

    query = st.text_input("Haz una pregunta sobre el contenido de los PDFs:")

    if query:
        docs = VectorStore.similarity_search(query=query, k=3)

        # Verifica si los documentos encontrados contienen algo relevante
        combined_content = " ".join([doc.page_content for doc in docs]).strip()
        if not combined_content:
            st.info("No encontré una respuesta a tu pregunta en los documentos proporcionados.")
            return

        llm = Ollama(model="mistral")  # Puedes usar otro modelo
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=query)
        #response = chain.invoke(input_documents=docs, question=query)

        # Si el modelo no responde nada útil
        if not response.strip() or response.lower().startswith("i don't know") or "lo siento" in response.lower():
            st.info("No encontré una respuesta a tu pregunta en los documentos proporcionados.")
        else:
            st.write(response)

if __name__ == '__main__':
    main()