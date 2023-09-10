import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage, HumanMessage, SystemMessage
)

if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = ""

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state["PINECONE_API_KEY"] = ""

if "PINECONE_ENVIRONMENT" not in st.session_state:
    st.session_state["PINECONE_ENVIRONMENT"] = ""

st.set_page_config(page_title="Welcome to interesting Langchain applications", layout='wide')

st.title('欢迎来到任宇林的 LangChain 频道~')

if "message" not in st.session_state:
    st.session_state['message'] = []

# openAI setting
openai_api_key = st.text_input("OPENAI API Key", value=st.session_state['OPENAI_API_KEY'], max_chars=None, key=None, type='password')

# pinecone setting
pinecone_api_key = st.text_input("PINECONE API Key", value=st.session_state["PINECONE_API_KEY"],
                                 max_chars=None, key=None, type='default')

environment = st.text_input("PINECONE Environment", value=st.session_state["PINECONE_ENVIRONMENT"],
                            max_chars=None, key=None, type='default')

saved = st.button("Save")
if saved:
    st.session_state['OPENAI_API_KEY'] = openai_api_key
    st.session_state['PINECONE_API_KEY'] = pinecone_api_key
    st.session_state['PINECONE_ENVIRONMENT'] = environment

    # print(f"openai_api_key:{st.session_state['OPENAI_API_KEY']}")
    # print(f"pinecone_api_key:{st.session_state['PINECONE_API_KEY']}")
    # print(f"environment:{st.session_state['PINECONE_ENVIRONMENT']}")


if st.session_state['OPENAI_API_KEY'] == "":
    with st.container():
        st.warning("Please set your OPENAI API KEY in the settings page!")




















