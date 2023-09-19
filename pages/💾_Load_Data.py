import streamlit as st
from lib.pinetools import getNamespaces, deleteFile, uploadPdfFile

st.set_page_config(page_title="💾 Load data")


# functions
def handleButtonClick():
    st.toast(f"Verarbeite {newFile}")
    docSearch = uploadPdfFile(newFile)
    del st.session_state["namespaces"]
    st.session_state.textInputNamespace = ""


def handleButtonDelete():
    # wirklich löschen usw...
    deleteFile(optFileDelete)
    del st.session_state["namespaces"]
    st.toast(f"{optFileDelete} gelöscht.")


# init
if "namespaces" not in st.session_state:
    st.session_state["namespaces"] = getNamespaces()


# page
tabNew, tabDelete = st.tabs(tabs=["Neu", "Löschen"])

with tabNew:
    newFile = st.file_uploader(
        label="Pdf-Datei Upload",
        help="Die ausgewählte Datei wird in Pincone hochgeladen.",
        type="pdf",
    )

    if newFile is not None:
        st.button(label="Upload", on_click=handleButtonClick)

with tabDelete:
    st.markdown("### 🗑 Dateien aus Datenbank entfernen")
    st.warning(
        "Achtung: Daten werden entgültig aus der Datenbank entfert. Du kannst diesen Schritt nicht rückgängig machen."
    )
    optFileDelete = st.selectbox(
        "Bitte wähle ein Dokument",
        options=st.session_state["namespaces"],
        key="selectboxDelete",
    )
    if optFileDelete is not None:
        st.button(label="Datei löschen", on_click=handleButtonDelete)
