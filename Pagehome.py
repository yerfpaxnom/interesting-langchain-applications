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

if "message" not in st.session_state:
    st.session_state['message'] = []



if chat:
    with st.container():
        st.header("Chat with GPT")

        for message in st.session_state['message']:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)
                    
        prompt = st.chat_input("Type something...")
        if prompt:
            st.session_state['message'].append(HumanMessage(content=prompt))
            with st.chat_message("user"):
                st.markdown(prompt)
            ai_message = chat([HumanMessage(content=prompt)])
            st.session_state['message'].append(ai_message)
            with st.chat_message("assistant"):
                st.markdown(ai_message.content)
            st.write(ai_message.content)
else:
    with st.container():
        st.warning("Please set your OPENAI API KEY in the settings page!")















