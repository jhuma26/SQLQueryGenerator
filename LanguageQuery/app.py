from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import sqlite3
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')
# Function to load Google gemini model and provide sql query as response
def get_gemini_response(prompt,question):
    response = model.generate_content([prompt[0],question])
    return response.text

# Function to retrieve query from SQL database
def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

# define prompt
prompt=[
    """
    You are an expert in converting English questions to SQL query
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS,
    SECTION \n\n For example, \nExample 1 - How many entries of records are present?,
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
    \n Example 2 - Tell me all the students studying in Data Science class?,
    the SQL command will be something like this SELECT * FROM STUDENT where CLASS = "Data Science";
    also the sql code should not have ``` in beginning or end and aql word in output
    """
]
st.set_page_config(page_title="Retrieve SQL query")
st.header("Gemini App to Retrieve SQL Data")
question = st.text_input("Input: ",key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(prompt,question)
    print(response)
    data = read_sql_query(response,"student.db")
    st.subheader("The response is")
    for row in data:
        print(row)
        st.header(row)
