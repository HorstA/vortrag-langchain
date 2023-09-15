import streamlit as st
from lib.pinetools import generateChatAnswer

st.title("💬 Ragtime!")
st.caption("🚀 LangChain Chat mit Embedding")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # msg = response.choices[0].message

    msg = generateChatAnswer(messages=st.session_state.messages)
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg["content"])
