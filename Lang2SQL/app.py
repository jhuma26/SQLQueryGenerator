from dotenv import load_dotenv
load_dotenv()
import os

import streamlit as st
import openai as ai
OpenAI =  os.getenv("OPENAI_API_KEY")

def natural_language_to_sql(nl_query):
    messages = [
        {"role": "system", "content": "You are a helpful assistant that translates natural language to SQL queries."},
        {"role": "user", "content": f"Translate the following natural language query into an SQL command: '{nl_query}'"}
    ]
    
    response = ai.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the appropriate engine
        messages=messages,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    sql_query = response.choices[0].message.content.strip()
    return sql_query

st.set_page_config(page_title="Retrieve SQL query")
st.header("Gemini App to Retrieve SQL Query")
question = st.text_input("Input: ",key="input")
submit = st.button("Ask the question")

if submit:
    response = natural_language_to_sql(question)
    print(response)
    st.header(response)