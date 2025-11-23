from openai import OpenAI
import streamlit as st
import pandas as pd

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("Dashboard + OpenAI Query")

CSV_URL = "https://raw.githubusercontent.com/chrishawnm/Health_Insights/main/data2.csv"

df = pd.read_csv(CSV_URL)

tab1, tab2= st.tabs(["Data Overview", "Visualizations"])


#Dict to give user descriptions on possible data to query from
column_descriptions = {
    "condition" : "Patient's disease",
    "county_name" : "The county of the state of the patient's origin",
    "state_name" : "Patient's State of origin",
    "race" : "Patient's Race or Ethnicity",
    "sex_label" : "Male or Female",
    "avg_age" : "Average age of person with that condition",
    "cnt" : "Unique count of patients",
}

#making and printing dataframe to UI
description_df = pd.DataFrame({
    'Parameters': df.columns,
    'Description' : [column_descriptions.get(column) for column in df.columns]
})
with tab1:
    st.subheader("Available Data")
    st.dataframe(description_df, hide_index=True)

with tab2:
    # Ask a question about the data
    if df is not None:
        question = st.text_input("Got a question about the dashboard board?:")
        
        if st.button("Submit") and question.strip():
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
    
            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
            )
                
            answer = response.choices[0].message.content 
            st.write("Answer")
        st.write(answer)
