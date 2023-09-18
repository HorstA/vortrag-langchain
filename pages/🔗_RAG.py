import streamlit as st
from lib.pinetools import generateChatAnswer, getNamespaces

# init
if "namespaces" not in st.session_state:
    st.session_state["namespaces"] = getNamespaces()


st.title("💬 Ragtime!")
st.caption("🚀 LangChain Chat mit Embedding")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]


namespace_file = st.selectbox(
    "Bitte wählen Sie ein Dokument",
    options=st.session_state["namespaces"],
    key="selectboxDelete",
)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    answer = generateChatAnswer(
        question=prompt, namespace=namespace_file, messages=st.session_state.messages
    )
    msg = {"role": "assistant", "content": answer}
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])
