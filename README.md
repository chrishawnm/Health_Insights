# Health Insights Dashboard & Text to SQL Query Assistant

This project integrates a comprehensive Tableau Dashboard for visual analytics with an LLM Streamlit application for natural language data querying. The entire platform is unified and hosted via GitHub Pages, providing a seamless user experience for exploring Medicare Synthetic Data.

## Live Demo
**[Click here to view the project website via GitHub Pages](https://chrishawnm.github.io/Health_Insights/)** 

---

## Data Architecture & ETL

### Data Source
We utilized the **CMS 2008-2010 Data Entrepreneurs’ Synthetic Public Use File (DE-SynPUF)**. This data provides realistic Medicare claims data while protecting beneficiary privacy.
* **Source:** [CMS.gov DE-SynPUF](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf)
* **User Manual:** [DE-SynPUF User Manual Document](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf)

### Data Ingestion
The raw data consists of 20 sample folders. From each folder, we extracted:
1.  **2009 Beneficiary Summary File** (ZIP)
2.  **2010 Beneficiary Summary File** (ZIP)

**Additional Mapping Files:**
* **State/County Mapping:** [CMS Prevalence Rates](https://www.cms.gov/priorities/innovation/media/document/vit-prevalence-rates) (Tab: `ED_VS_STATE_CNTY`, Columns A-E).
* **Condition Mappings:** e.g., mapping `SP_COPD` to 'Chronic Obstructive Pulmonary Disease'.
* **Demographics:** Beneficiary Race and Sex mapping tables (derived from the User Manual).

> **Access Raw Files:** [View our Google Drive Repository](https://drive.google.com/drive/folders/1VaBE-QesTmFuwi0-ucZGoezF7MAJutH2?usp=sharing)

### ETL Process (Google BigQuery)
We used Google BigQuery to clean, join, and transform the raw datasets. 
* **SQL Script:** See `etl_process.sql` in this repository for the exact queries used.
* **Output:** The SQL process generates specific tables required for the visualization and the AI app.

---

## Tableau Dashboard

The dashboard visualizes key health metrics and patient profiles. It consumes the transformed data exported from BigQuery.

### Visualizations Included:
1.  **Condition Heatmap:** Visualizes correlations (comorbidities) to show the likelihood of Condition A being associated with Condition B.
2.  **Geographic Distribution:** A map displaying the number of patients per state with specific conditions.
3.  **Patient Counts:** Bar charts showing the total volume of patients with specific conditions.
4.  **Patient Profile:** A breakdown of demographics including Age Band, Race, Gender, and Number of Conditions.
5.  **General Insights:** Key metrics showing the scale of data (Total Patients, Conditions, States, and Counties represented).

### Replication Steps:
1.  Download the `new_final.twb` workbook from this repo.
2.  Ensure your data files match the names specified in `etl_process.sql`.
3.  Open the workbook in Tableau Desktop.
4.  Publish the dashboard to **Tableau Public** (Data extracts may be required).

---

## Streamlit Application

The Streamlit app allows users to ask questions about the data in plain English. It uses LangChain to interpret natural language and query the underlying dataframe.

### Key Features:
* **Natural Language Querying:** Users ask questions (e.g., "Top 5 states with Heart Failure"), and the app generates the answer.
* **Chart Generation:** Users can toggle an option to generate visual charts (bar graphs, histograms) based on their query.
* **Guardrails:** Input validation ensures questions are appropriate and safe.
* **User Guide & Data Overview:** To help users understand the available data columns.

### Technical Implementation:
* **Libraries:** `streamlit`, `pandas`, `langchain`, `openai` (See `requirements.txt`).
* **Data Source:** `data2.csv` (Output from the ETL process).
* **Hosting:** Streamlit Community Cloud.

---

## Web Integration (GitHub Pages)

The final product wraps the Tableau Dashboard and Streamlit App into a single website using GitHub Pages.

### Setup Instructions:

1.  **Tableau Integration:**
    * Publish your dashboard to Tableau Public.
    * Copy the embed link.
    * Open `index.html` in this repo and replace the Tableau link (make sure your link can be embedded):
       ```html
        https://public.tableau.com/views/Health_Insights_bigger/Dashboard1?:showVizHome=no&:embed=true
        ```

2.  **Streamlit Integration:**
    * Push `data2.csv` and `app.py` to this GitHub repo.
    * Connect your repo to [Streamlit Community Cloud](https://streamlit.io/).
    * Once deployed, copy your App URL.
    * Open `index.html` and replace the Streamlit link (make sure your link can be embedded):
        ```html
        https://healthinsights-z8ndwx47fkfqu8qwmnq7v5.streamlit.app/?embed=true
        ```

3.  **Deploying the Site:**
    * Go to your GitHub Repository **Settings**.
    * Select the **Pages** tab.
    * Select `main` branch as the source and save.
  
## Project Flow Screenshot
![Project Flow Diagram](Project%20Flow%20Diagram.png)
