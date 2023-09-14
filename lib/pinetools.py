import os
import tempfile
import pinecone
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def uploadPdfFile(newFile):
    # upload to Pinecone
    temp_file_path = os.getcwd()
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, newFile.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(newFile.read())

    # load text from file

    # split into chunks

    # create embeddings

    # save in Pinecone


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
    # return ("Musterpachtvertrag", "Datei 2", "Datei 3")
    return myList
