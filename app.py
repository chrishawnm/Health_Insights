from openai import OpenAI
import streamlit as st
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Dashboard + OpenAI Query")

CSV_URL = "https://raw.githubusercontent.com/chrishawnm/Health_Insights/main/data2.csv"

df = pd.read_csv(CSV_URL)
st.dataframe(df.dtypes)


# Ask a question about the data
if df is not None:
    question = st.text_input("Got a question about the dashboard board?:")
    
    if st.button("Submit") and question.strip():
        prompt = f"""
        You are a data assistant. A user has a pandas dataframe named `df`:

        {df.head(1000).to_string()}

        Columns:
        {list(df.columns)}

        Question: {question}

      
        return the actual result from the dataframe not just unique.
        like if they ask for unique count sure provide unique count 
        but if they ask for the unique list return the actual list and not just the code
        """

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
        )
            
        answer = response.choices[0].message.content  # ✅ THIS LINE
        st.write("Answer")
        st.write(answer)
