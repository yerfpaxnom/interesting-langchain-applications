import streamlit as st
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.utilities import WikipediaAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import YouTubeSearchTool
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from youtubesearchpython import VideosSearch
from langchain.chains import VectorDBQA
from langchain.retrievers import SelfQueryRetriever
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.tools import PubmedQueryRun
from langchain import LLMMathChain
import sqlite3
import pandas as pd
import os

os.environ['OPENAI_API_KEY'] = st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else ''


# TODO: Allow users to upload their own files

def create_research_db():
    with sqlite3.connect('MASTER.db') as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Research (
                research_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                introduction TEXT,
                quant_facts TEXT,
                publications TEXT,
                books TEXT,
                ytlinks TEXT
            )
        """)


def create_messages_db():
    pass


def read_research_table():
    with sqlite3.connect('MASTER.db') as conn:
        query = "SELECT * FROM Research"
        df = pd.read_sql_query(query, conn)
    return df


def insert_research(user_input, introduction, quant_facts, publications, books, ytlinks):
    with sqlite3.connect('MASTER.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Research (user_input, introduction, quant_facts, publications, books, ytlinks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_input, introduction, quant_facts, publications, books, ytlinks))


def generate_research(userInput):
    global tools
    llm = OpenAI(temperature=0.7)
    wiki = WikipediaAPIWrapper()
    DDGsearch = DuckDuckGoSearchRun()
    YTsearch = YouTubeSearchTool()
    pubmed = PubmedQueryRun()
    llm_math_chain = LLMMathChain(llm=llm, verbose=True)

    tools = [
        Tool(
            name="Wikipedia Research Tool",
            func=wiki.run,
            description="Useful for researching information on wikipedia"
        ),
        Tool(
            name="Duck Duck Go Search Results Tool",
            func=DDGsearch.run,
            description="Useful for search for information on the internet"
        ),
        Tool(
            name="YouTube Search Tool",
            func=YTsearch.run,
            description="Useful for gathering links on YouTube"
        ),
        Tool(
            name='Calculator and Math Tool',
            func=llm_math_chain.run,
            description='Useful for mathematical questions and operations'
        ),
        Tool(
            name='Pubmed Science and Medical Journal Research Tool',
            func=pubmed.run,
            description='Useful for Pubmed science and medical research\nPubMed comprises more than 35 million citations for biomedical literature from MEDLINE, life science journals, and online books. Citations may include links to full text content from PubMed Central and publisher web sites.'

        )
    ]
    # if st.session_state.embeddings_db:
    #     qa = VectorDBQA.from_chain_type(llm=llm, vectorstore=st.session_state.embeddings_db)
    #     tools.append(
    #         Tool(
    #             name='Vector-Based Previous Resarch Database Tool',
    #             func=qa.run,
    #             description='Provides access to previous research results'
    #         )
    #     )

    memory = ConversationBufferMemory(memory_key="chat_history")
    runAgent = initialize_agent(tools,
                                llm,
                                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                verbose=True,
                                memory=memory,
                                )

    with st.expander("检索结果", expanded=True):
        st.subheader("检索主题:")
        st.write(userInput)

        st.subheader("介绍:")
        with st.spinner("努力搬运中..."):
            intro = runAgent(f'Write an academic introduction about {userInput}')
            st.write(intro['output'])

        st.subheader("话题摘录:")
        with st.spinner("努力搬运中..."):
            quantFacts = runAgent(f'''
                Considering user input: {userInput} and the intro paragraph: {intro} 
                \nGenerate a list of 3 to 5 quantitative facts about: {userInput}
                \nOnly return the list of quantitative facts
            ''')
            st.write(quantFacts['output'])

        # prev_ai_research = ""
        # if st.session_state.embeddings_db:
        #     st.subheader("Previous Related AI Research:")
        #     with st.spinner("Researching Pevious Research"):
        #         qa = VectorDBQA.from_chain_type(llm=llm, vectorstore=st.session_state.embeddings_db)
        #         prev_ai_research = qa.run(f'''
        #             \nReferring to previous results and information, write about: {userInput}
        #         ''')
        #         st.write(prev_ai_research)

        st.subheader("最新论文:")
        with st.spinner("努力搬运中..."):
            papers = runAgent(f'''
                Consider user input: "{userInput}".
                \nConsider the intro paragraph: "{intro}",
                \nConsider these quantitative facts "{quantFacts}"
                \nNow Generate a list of 2 to 3 recent academic papers relating to {userInput}.
                \nInclude Titles, Links, Abstracts. 
            ''')
            st.write(papers['output'])

        st.subheader("推荐书籍:")
        with st.spinner("努力搬运中..."):
            readings = runAgent(f'''
                Consider user input: "{userInput}".
                \nConsider the intro paragraph: "{intro}",
                \nConsider these quantitative facts "{quantFacts}"
                \nNow Generate a list of 5 relevant books to read relating to {userInput}.
            ''')
            st.write(readings['output'])

        st.subheader("相关视频:")
        with st.spinner("努力搬运中..."):
            search = VideosSearch(userInput)
            ytlinks = ""
            for i in range(1, 6):
                ytlinks += (str(i) + ". Title: " + search.result()['result'][0][
                    'title'] + "Link: https://www.youtube.com/watch?v=" + search.result()['result'][0]['id'] + "\n")
                search.next()
            st.write(ytlinks)

        # TODO: Influential Figures

        # TODO: AI Scientists Perscpective

        # TODO: AI Philosophers Perspective

        # TODO: Possible Routes for Original Research

        insert_research(userInput, intro['output'], quantFacts['output'], papers['output'], readings['output'], ytlinks)
        # research_text = [userInput, intro['output'], quantFacts['output'], papers['output'], readings['output'],
        #                  ytlinks]
        # embedding_function = OpenAIEmbeddings()
        # vectordb = Chroma.from_texts(research_text, embedding_function, persist_directory="./chroma_db")
        # vectordb.persist()
        # st.session_state.embeddings_db = vectordb


class Document:
    def __init__(self, content, topic):
        self.page_content = content
        self.metadata = {"Topic": topic}


def init_ses_states():
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("prev_chat_history", [])
    st.session_state.setdefault("embeddings_db", None)
    st.session_state.setdefault('research', None)
    st.session_state.setdefault("prev_research", None)
    st.session_state.setdefault("books", None)
    st.session_state.setdefault("prev_books", None)


def main():
    # st.set_page_config(page_title="Research Bot👨‍🎓")
    create_research_db()
    init_ses_states()
    # llm = OpenAI(temperature=0.7)
    # embedding_function = OpenAIEmbeddings()
    # if os.path.exists("./chroma_db"):
    #     st.session_state.embeddings_db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    st.title("学术查询👨‍🎓")
    deploy_tab, prev_tab = st.tabs(["开始检索", "历史检索"])
    with deploy_tab:
        userInput = st.text_area(label="检索主题")
        if st.button("生成报告") and userInput:
            generate_research(userInput)

        # st.subheader("Chat with Data")
        # user_message = st.text_input(label="User Message", key="um1")
        # if st.button("Submit Message") and user_message:
        #     memory = ConversationBufferMemory(memory_key="chat_history")
        #     chatAgent = initialize_agent(tools,
        #                                  llm,
        #                                  agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        #                                  verbose=True,
        #                                  memory=memory,
        #                                  )
    with prev_tab:
        st.dataframe(read_research_table())
        selected_input = st.selectbox(label="历史检索主题",
                                      options=[i for i in read_research_table().user_input])
        # if st.button("检索") and selected_input:
        if selected_input:
            selected_df = read_research_table()
            selected_df = selected_df[selected_df.user_input == selected_input].reset_index(drop=True)

            st.subheader("检索主题:")
            st.write(selected_df.user_input[0])

            st.subheader("介绍:")
            st.write(selected_df.introduction[0])

            st.subheader("话题摘录:")
            st.write(selected_df.quant_facts[0])

            st.subheader("最新论文::")
            st.write(selected_df.publications[0])

            st.subheader("推荐书籍:")
            st.write(selected_df.books[0])

            st.subheader("相关视频:")
            st.write(selected_df.ytlinks[0])

            # st.subheader("Chat with Data")
            # prev_user_message = st.text_input(label="User Message", key="um2")


if __name__ == '__main__':
    # load_dotenv()
    main()

