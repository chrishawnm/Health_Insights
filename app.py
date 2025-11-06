from openai import OpenAI
import streamlit as st
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Dashboard + OpenAI Query")

CSV_URL = "https://raw.githubusercontent.com/chrishawnm/Health_Insights/refs/heads/main/data2.csv"

df = pd.read_csv(CSV_URL)
st.dataframe(df.head())


# Ask a question about the data
if df is not None:
    question = st.text_input("Got a question about the dashboard board?:")
    
    if st.button("Submit") and question.strip():
        prompt = f"""
        You are a data assistant. A user has a pandas dataframe named `df`:

        {df.head(5).to_string()}

        Columns:
        {list(df.columns)}

        Question: {question}

        Return:
        1) A short and clear answer.
        2) If needed, also provide Python code that uses pandas to compute the answer.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write("Answer")
        st.write(answer)
