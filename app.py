import os
from openai import OpenAI
import streamlit as st
import pandas as pd
import re
#these two libraries are for us to have chatgpt takes it own answer and apply it back to the dataframe we gave it
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
#these are the files we need to have the visualization work on streamlit so when you have a question it can actually create a visual using these libraries
import matplotlib
import seaborn
import tabulate

st.title("Dashboard + OpenAI Query")

#this is where we are importing the dataframe and connecting it to the llm
CSV_URL = "https://raw.githubusercontent.com/chrishawnm/Health_Insights/main/data2.csv"

df = pd.read_csv(CSV_URL)
#llm_df = SmartDataframe(df, config={"llm": llm})

#this is the beginning of where we make the app more aesthestically pleasing
tab1, tab2= st.tabs(["Data Overview", "Questions"])

#this is how we stop bad actors from doing something we dont want it to do lik
#deleted , ignore or pretend as examples 
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

#this is the questions tab where most of our code is 
with tab2:

     col1, col2 = st.columns([3, 1])

     #this is just setting up our question text box and generate chart check box
     with col1:
            question = st.text_input("Got a question about the dashboard?:")
     with col2:
            generate_chart = st.checkbox("Generate Chart", value=False)
       
     #submit button
     if st.button("Submit") and question.strip():
     
          # so the questio first goes through the hack function to make sure its not a bad question
          #then we run the llm and make it known of our dataframe
          #then we take the question and if the generate chart button has been set to true then we add on a viz prompt
          # then finally we have the llm agent read the final question 
          #and in that it will also create a dataframe function that will then run it on the dataframe we gave it 
          #then itll post the answer
          # itll also generate a chart if the button is checked and the agent generated it
          if question_validation(question):
                 
               with st.spinner("Processing..."):
                     #answer = llm_df.query(question)
                    llm = ChatOpenAI( model="gpt-3.5-turbo", temperature=0, api_key=st.secrets["OPENAI_API_KEY"] )
                    
                   
                         
                    agent = create_pandas_dataframe_agent( llm,  df,  verbose=True, allow_dangerous_code=True, handle_parsing_errors=True )

                    final_question = question
                    if generate_chart:
                         final_question += ". If you plot data, save the figure as 'viz.png' and do not show it interactively."

                    response = agent.invoke(final_question)
                    
                    st.write("Answer")
                    st.write(response['output'])

                    if generate_chart and os.path.exists("viz.png"):
                            st.image("viz.png")
                            os.remove("viz.png") 
                    elif generate_chart:
                            st.warning("The agent didn't generate a chart file. Try explicitly asking for a 'plot' in your text prompt.")
          else:
               st.error("Try asking a different question")

     #just wanted to add a common questions section for the user to know some questions they can ask if they are drawing a blank
     st.markdown("---")
     st.subheader("Common Questions")
    
     st.markdown("""
     * *What are the top 5 states with the highest patient count?*
     * *Show me the breakdown of patients by race for Diabetes. [Visualization]*
     * *What is the average age for patients with Heart Failure?*
     * *Compare the number of Male vs Female patients overall.*
     * *Which county in California has the highest unique count?*
     * *Plot the total number of patients per condition. [Visualization]*
     """)            
            
 #we added a sidebar because we wanted to be a bit organized and have people know what tabs are doing what and the intention and purpose of the app           
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
                     
            This data can be queried via the quick questions option.
            """)
            
        with st.expander("Questions", expanded=False):
            st.write(""" 
            You can ask any more granular question pertaining to the dashboard (excluding condition matrix).
            
            If you want a visual of your answer please click the check box (Generate Chart) and it will create a chart for you.
            
            If you ask it to perform any change to the dataframe it will not and ask you to ask another question.
                     
            """)
