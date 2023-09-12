import streamlit as st
import os
import openai

openai.api_key = st.session_state['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.session_state else ''

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.to_dict()


# Streamlit app layout
st.title("欢迎来到我的披萨店👨‍🍳")
st.write("您可以在这里直接下单哦~")

system_message = {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""}

MESSAGE = 'pizza_order_bot_message'

if MESSAGE not in st.session_state or len(st.session_state[MESSAGE]) == 0:
    st.session_state[MESSAGE] = [system_message]

with st.container():
    # st.header("Chat with GPT")

    # 所有对话历史展示
    for message in st.session_state[MESSAGE]:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.markdown(message['content'])
        elif message['role'] == 'assistant':
            with st.chat_message("assistant"):
                st.markdown(message['content'])

    prompt = st.chat_input("有哪些口味的披萨")

    if prompt:
        st.session_state[MESSAGE].append({'role': 'user', 'content': prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        print("context", st.session_state[MESSAGE])

        ai_message = get_completion_from_messages(st.session_state[MESSAGE])
        st.session_state[MESSAGE].append(ai_message)

        with st.chat_message("assistant"):
            st.markdown(ai_message['content'])
        st.write(ai_message['content'])
