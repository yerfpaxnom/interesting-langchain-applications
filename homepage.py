import os
import openai
import streamlit as st
from langchain.schema import (
    AIMessage, HumanMessage, SystemMessage
)

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
# openai.api_key  = os.environ['OPENAI_API_KEY']
st.session_state["PINECONE_API_KEY"] = os.environ['PINECONE_API_KEY']
st.session_state["PINECONE_ENVIRONMENT"] = os.environ['PINECONE_ENVIRONMENT']


if 'OPENAI_API_KEY' not in st.session_state:
    st.session_state['OPENAI_API_KEY'] = ""

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state["PINECONE_API_KEY"] = ""

if "PINECONE_ENVIRONMENT" not in st.session_state:
    st.session_state["PINECONE_ENVIRONMENT"] = ""

st.set_page_config(page_title="Welcome to interesting Langchain applications", layout='wide')

st.title('📣欢迎来到任宇林的 LangChain 频道🎼 ')

if "message" not in st.session_state:
    st.session_state['message'] = []

#
st.session_state['OPENAI_API_KEY'] = os.environ['OPENAI_API_KEY']

# openAI setting
openai_api_key = st.text_input("OPENAI API Key", value=st.session_state['OPENAI_API_KEY'],
                               max_chars=None, key=None, type='password')

# pinecone setting
pinecone_api_key = st.text_input("PINECONE API Key", value=st.session_state["PINECONE_API_KEY"],
                                 max_chars=None, key=None, type='password')

environment = st.text_input("PINECONE Environment", value=st.session_state["PINECONE_ENVIRONMENT"],
                            max_chars=None, key=None, type='password')

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




















