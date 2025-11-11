from openai import OpenAI
import streamlit as st
import pandas as pd
import google.generativeai as genai
import re

def question_query(question):
        prompt = f"""
        You are a data assistant. A user has a pandas dataframe named 'df':

        {df.head(1000).to_string()}

        Columns:
        {list(df.columns)}

        Question: {question}

      
        return the actual result from the dataframe not just unique.
        like if they ask for unique count sure provide unique count 
        but if they ask for the unique list return the actual list 
        dont describe anything just give the value and that is it.
        dont show them the code
        """
        with st.spinner("Processing..."):
            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
            )

            #model = genai.GenerativeModel('gemini-2.5-flash')
            #response = model.generate_content(prompt)
            #answer=response.text

            answer = response.choices[0].message.content 
            st.write("Answer:")
            st.write(answer)

def question_validation(question):
     
    checks = [r"(?i)(union|insert|drop|delete|update|alter)", 
            r"(?i)(ignore|previous|forget|disregard)",
            r"(?i)(you are now|act as|pretend|prompt|role play|by pass)"]
     
    for case in checks:
          if re.search(case, question):
               return False
    return True
          


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#genai.configure(api_key="")

st.title("Dashboard + OpenAI Query")

CSV_URL = "https://raw.githubusercontent.com/chrishawnm/Health_Insights/main/data2.csv"

df = pd.read_csv(CSV_URL)
st.dataframe(df.dtypes)


# Ask a question about the data
if df is not None:
    st.subheader("Quick Questions")
    
    question = st.text_input("Got a question about the dashboard board?:")
    
    if st.button("Submit") and question.strip():
        if question_validation(question):
            question_query(question)
        else:
            st.error("Try asking a different question")
