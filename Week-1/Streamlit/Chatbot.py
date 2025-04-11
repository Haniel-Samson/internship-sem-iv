from openai import OpenAI
import streamlit as st

st.title("Bot-Chat")
client = OpenAI(base_url="https://api.aimlapi.com/v1", api_key="Insert-Key-Here")

if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

if prompt := st.chat_input("Enter a message"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(model = "gpt-4o", messages=[{"role": "user", "content": prompt}])
    st.chat_message("assistant").markdown(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
