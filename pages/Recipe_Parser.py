from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    PromptTemplate
)
from langchain.schema import (
    HumanMessage
)
from langchain.chat_models import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List, Union, Any
from bs4 import BeautifulSoup
import requests
import streamlit as st


#菜谱网址：https://www.jamieoliver.com/recipes
# https://www.jamieoliver.com/recipes/chicken-recipes/lemon-tzatziki-chicken/

class Ingredient(BaseModel):
    name: str = Field(description="The name of the ingredient")
    quantity: str = Field(
        description="The specific unit of measurement corresponding to the quantity, such as grams, ounces, liters, etc.")
    unit: str = Field(
        description="The amount of the ingredient required for the recipe. This can be represented using various units such as grams, cups, teaspoons, etc.")


class Recipe(BaseModel):
    name: str = Field(description="The name of the recipe")
    ingredients: List[Ingredient] = Field(description="The list of ingredients for the recipe")

PAGE_TITLE = "🍳 Jamie Oliver's Recipe"
st.set_page_config(layout="centered", page_title=PAGE_TITLE)
st.title(PAGE_TITLE)


def get_recipe_html(url):
    response = requests.get(url)
    html_markup = ''
    if response.status_code == 200:
        html_markup = response.text
        soup = BeautifulSoup(html_markup, 'html.parser')

        # Find the element with id 'recipe-single'
        recipe_element = soup.find(id='recipe-single')

        if recipe_element:
            # Get the sanitized content within the 'recipe-single' element
            html_markup = str(recipe_element)

    return html_markup


def parse_by_chatgpt(openai_api_key, html_markup):
    parser = PydanticOutputParser(pydantic_object=Recipe)
    prompt = PromptTemplate(
        template="Extract the recipe ingredients from the following HTML markup:\n{html}.\n{format_instructions}\n",
        input_variables=["html"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    model = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0.0, openai_api_key=openai_api_key)
    output = model([HumanMessage(content=prompt.format_prompt(html=html_markup).to_string())])

    recipe = parser.parse(output.content)
    return recipe

with st.container():
    # if 'OPENAI_API_KEY' not in st.session_state:
    #     st.session_state['OPENAI_API_KEY'] = ""
    #
    # if "PINECONE_API_KEY" not in st.session_state:
    #     st.session_state["PINECONE_API_KEY"] = ""
    #
    # if "PINECONE_ENVIRONMENT" not in st.session_state:
    #     st.session_state["PINECONE_ENVIRONMENT"] = ""

    openai_api_key = st.session_state['OPENAI_API_KEY']

    recipe_url = st.text_input("URL of a Jamie Oliver Recipe. eg,  https://www.jamieoliver.com/recipes/soup-recipes/cheats-pea-soup/", key="recipe_url")
    clicked = st.button("提取菜谱")
    if clicked:
        html_markup = get_recipe_html(recipe_url)
        if html_markup:
            recipe: Union[BaseModel, Any] = parse_by_chatgpt(openai_api_key, html_markup)
            st.json(recipe.json())