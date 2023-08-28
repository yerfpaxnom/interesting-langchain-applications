import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage, HumanMessage, SystemMessage
)

chat = None

if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = ""
else:
    chat = ChatOpenAI(openai_api_key=st.session_state['OPENAI_API_KEY'])

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state["PINECONE_API_KEY"] = ""

if "PINECONE_ENVIRONMENT" not in st.session_state:
    st.session_state["PINECONE_ENVIRONMENT"] = ""

st.set_page_config(page_title="Welcome to interesting Langchain applications", layout='wide')

st.title('Welcome to interesting Langchain applications')

# with st.container():
#     st.header("OpenAI Settings")
#     st.markdown(f"""
#         | OpenAI API Key |
#         | -------------- |
#         | {st.session_state['OPENAI_API_KEY']} |
#         """)

# with st.container():
#     st.header("Pinecone Settings")
#     st.markdown(f"""
#         | Pinecone API Key | Environment |
#         | ---------------- | ----------- |
#         | {st.session_state['PINECONE_API_KEY']} | {st.session_state["PINECONE_ENVIRONMENT"]} |
#         """)

if chat:
    with st.container():
        st.header("Chat with GPT")
        prompt = st.text_input("Prompt",value="", max_chars=None, key=None, type="default")
        asked = st.button("Ask")
        if asked:
            ai_message = chat([HumanMessage(content=prompt)])
            st.write(ai_message.content)
else:
    with st.container():
        st.warning("Please set your OPENAI API KEY in the settings page!")















