from openai import OpenAI
import streamlit as st
import pandas as pd
import re
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

st.title("Dashboard + OpenAI Query")

CSV_URL = "https://raw.githubusercontent.com/chrishawnm/Health_Insights/main/data2.csv"

df = pd.read_csv(CSV_URL)
#llm_df = SmartDataframe(df, config={"llm": llm})

tab1, tab2= st.tabs(["Data Overview", "Questions"])

def question_validation(question):
     
    checks = [r"(?i)(union|insert|drop|delete|update|alter)", 
            r"(?i)(ignore|previous|forget|disregard)",
            r"(?i)(you are now|act as|pretend|prompt|role play|by pass)"]
     
    for case in checks:
          if re.search(case, question):
               return False
    return True
    
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
    if df is not None:
        question = st.text_input("Got a question about the dashboard board?:")

            
        
        if st.button("Submit") and question.strip():

            
            if question_validation(question):
                 
                with st.spinner("Processing..."):
                     #answer = llm_df.query(question)
                     llm = ChatOpenAI( model="gpt-3.5-turbo", temperature=0, api_key=st.secrets["OPENAI_API_KEY"] )

                     agent = create_pandas_dataframe_agent( llm,  df,  verbose=True, allow_dangerous_code=True, handle_parsing_errors=True )
                     response = agent.invoke(question)
                     st.write("Answer")
                     st.write(response['output'])
            else:
                st.error("Try asking a different question")
                
            
            
            
with st.sidebar:
        st.title("Quick User Guide")

        with st.expander("Getting Started", expanded=False):
            st.write("""
            Choose a page from above in order to explore available options within the application.
                     
            1. **Explore your data** in Data Overview Tab
            2. **Ask Questions** in Questions Tab
            
            """)
    
        with st.expander("Data Overview", expanded=False):
            st.write("""
            This shows the available data and a descripton of each parameter than can be explored.
                     
            This data can also be queried via the quick questions option.
            """)
            
        with st.expander("Questions", expanded=False):
            st.write(""" 
            Available Questions
            
            1. Histograms: Show data distribution for integer values
            2. Bar Charts: Compare categories
            3. Pie Charts: Visualize share of data
                     
            """)
