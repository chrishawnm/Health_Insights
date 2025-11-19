from openai import OpenAI
import streamlit as st
import pandas as pd
import google.generativeai as genai
import re
import seaborn as sns
import matplotlib.pyplot as plt

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

#tab for data overview
with tab1:
    #st.dataframe(df.dtypes)
    st.subheader("Available Data")
    st.dataframe(description_df, hide_index=True)

    # Ask a question about the data
    if df is not None:
        st.subheader("Quick Questions")
        
        question = st.text_input("Got a question about the dashboard?:")
        
        if st.button("Submit") and question.strip():
            if question_validation(question):
                question_query(question)
            else:
                st.error("Try asking a different question")

#tab for basic data visualizations
with tab2:
    st.subheader("Data Visualizations")

    col = st.selectbox("Select a data parameter for visualization:", df.columns)
    visualization = st.selectbox("Choose a visualization:", ["Histogram", "Bar Chart", "Pie Chart"])

    #using integers in histograms for now
    if st.button("Generate Visualization"):
        if df[col].dtype == 'int64':
            if visualization == "Histogram":
                fig, ax = plt.subplots(figsize=(10,5))

                ax.set_title(f'Histogram for {col}')

                sns.histplot(df[col], ax=ax)
                st.pyplot(fig)
            else:
                st.error("Invalid visualization parameters")

        #objects are categorical data
        elif df[col].dtype == 'object':
                if visualization == "Bar Chart":
                    fig, ax = plt.subplots(figsize=(10, 5))

                    ax.set_title(f'Counts in {col}')
                    ax.set_xlabel(col)
                    ax.set_ylabel('Count')

                    df[col].value_counts().plot(kind='bar', ax=ax)

                    st.pyplot(fig)
                
                elif visualization == "Pie Chart":
                    fig, ax = plt.subplots(figsize=(8, 8))

                    ax.set_title(f'Distribution of {col}')
                    ax.pie(df[col].value_counts().values, labels=df[col].value_counts().index, autopct='%1.1f%%')

                    st.pyplot(fig)
                else:
                    st.error("Invalid visualization parameters")


with st.sidebar:
        st.title("Quick User Guide")

        with st.expander("Getting Started", expanded=False):
            st.write("""
            Choose a page from above in order to explore available options within the application.
                     
            1. **Explore your data** in Data Overview
            2. **Create visualizations** in Visualizations
            
            """)
    
        with st.expander("Data Overview", expanded=False):
            st.write("""
            This shows the available data and a descripton of each parameter than can be explored.
                     
            This data can also be queried via the quick questions option.
            """)
            
        with st.expander("Visualizations", expanded=False):
            st.write(""" 
            Available Visulizations
            
            1. Histograms: Show data distribution for integer values
            2. Bar Charts: Compare categories
            3. Pie Charts: Visualize share of data
                     
            """)
