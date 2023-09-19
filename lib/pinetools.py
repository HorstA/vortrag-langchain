import os
import tempfile
import pinecone
import streamlit as st
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

load_dotenv()


def uploadPdfFile(newFile):
    # upload to Pinecone
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, newFile.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(newFile.read())

    # load text from file
    loader = PyPDFLoader(temp_file_path)
    data = loader.load()

    # split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    # create embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    metadatas = [
        {
            "mandant": "langchain-vortrag",
            "doctype": "pdf-file",
            "source": t.metadata["source"],
            "page": t.metadata["page"],
        }
        for t in texts
    ]

    # save in Pinecone (namespace = filename)
    Pinecone.from_texts(
        [t.page_content for t in texts],
        embeddings,
        index_name=os.environ["PINECONE_INDEX"],
        namespace=newFile.name,
        metadatas=metadatas,
    )


def deleteFile(fileName):
    pinecone.Index(os.environ["PINECONE_INDEX"]).delete(
        delete_all=True, namespace=fileName
    )


@st.cache_data
def initPinecone():
    print("running initPinecone...")
    pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment=os.environ["PINECONE_API_ENV"],
    )


def getNamespaces():
    initPinecone()
    print("running getNamespaces...")
    print(os.environ["PINECONE_INDEX"])
    myList = list(
        pinecone.Index(os.environ["PINECONE_INDEX"]).describe_index_stats().namespaces
    )
    return myList


def generateChatAnswer(question, namespace, messages):
    initPinecone()
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    docsearch = Pinecone.from_existing_index(
        index_name=os.environ["PINECONE_INDEX"],
        embedding=embeddings,
        namespace=namespace,
    )

    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model="gpt-3.5-turbo")
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    result = qa({"query": question})

    print(result["result"])
    print(result["source_documents"])

    return result["result"]
