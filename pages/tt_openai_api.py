import os
import openai
from langchain.chat_models import ChatOpenAI

# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv()) # read local .env file
# openai.api_key = os.environ['OPENAI_API_KEY']

openai.api_key = "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"

llm_model = "gpt-3.5-turbo-0301"

def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

print(get_completion("What is 1+1?"))