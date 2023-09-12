import os
import openai
import streamlit as st
from langchain.document_loaders import YoutubeLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
  ChatPromptTemplate,
  SystemMessagePromptTemplate,
  HumanMessagePromptTemplate
)

st.title("Youtube视频问答")
st.caption("示例: https://www.youtube.com/watch?v=jGwO_UgTS7I&list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU")

MESSAGE = "qa_youtube_message"
if MESSAGE not in st.session_state:
    st.session_state[MESSAGE] = []

QA_KEY = "qa_youtube_qa_chain"
if QA_KEY not in st.session_state:
    st.session_state[QA_KEY] = None

print("1...")

openai.api_key = st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else ''

qa = None

if openai.api_key == '':
    st.warning("请正确设置openai key")

# if 'OPENAI_API_KEY' not in st.session_state:
#     st.session_state['OPENAI_API_KEY'] = ""
#
# if st.session_state['OPENAI_API_KEY'] != "":
#     os.environ["OPENAI_API_KEY"] = st.session_state['OPENAI_API_KEY']
    # 加载 youtube 频道
else:
    with st.container():

        youtube_url = st.text_input("URL of YouTube Channel", key="youtube_url")
        clicked = st.button("提取视频信息")
        if clicked:
            print('begin to load youtube..., openKEY: ', openai.api_key [-5:])
            loader = YoutubeLoader.from_youtube_url(youtube_url)
            # 将数据转成 document
            documents = loader.load()
            print('documents: ', len(documents))

            # 初始化文本分割器
            text_splitter = RecursiveCharacterTextSplitter(
              chunk_size=1000,
              chunk_overlap=20
            )

            # 分割 youtube documents
            documents = text_splitter.split_documents(documents)

            # 初始化 openai embeddings
            embeddings = OpenAIEmbeddings()

            # 将数据存入向量存储
            vector_store = Chroma.from_documents(documents, embeddings)
            # 通过向量存储初始化检索器
            retriever = vector_store.as_retriever()

            system_template = """
            Use the following context to answer the user's question.
            If you don't know the answer, say you don't, don't try to make it up. And answer in Chinese.
            -----------
            {question}
            -----------
            {chat_history}
            """

            # 构建初始 messages 列表，这里可以理解为是 openai 传入的 messages 参数
            messages = [
              SystemMessagePromptTemplate.from_template(system_template),
              HumanMessagePromptTemplate.from_template('{question}')
            ]

            # 初始化 prompt 对象
            prompt = ChatPromptTemplate.from_messages(messages)


            # 初始化问答链
            st.session_state[QA_KEY] = ConversationalRetrievalChain.from_llm(
                ChatOpenAI(temperature=0.1,max_tokens=2048),
                retriever,
                condense_question_prompt=prompt
            )

            st.markdown("视频信息提取完成，您可以提问啦~~")


# 所有对话历史展示
for i, message in enumerate(st.session_state[MESSAGE]):
    with st.chat_message("user"):
        st.markdown(message[0])
    with st.chat_message("assistant"):
        st.markdown(message[1])

question = st.chat_input("Type something...")
if question:
    with st.chat_message("user"):
        st.markdown(question)

    print("question: ", question)
    print("chat_history: ", st.session_state[MESSAGE])
    print("qa: ", st.session_state[QA_KEY])
    if st.session_state[QA_KEY]:
        # 开始发送问题 chat_history 为必须参数,用于存储对话历史
        result = st.session_state[QA_KEY]({'question': question, 'chat_history': st.session_state[MESSAGE]})
        st.session_state[MESSAGE].append((question, result['answer']))
        st.write(result['answer'])