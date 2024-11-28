import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
import os

# Define file paths for persistence
DATA_FILE = 'recruitment_data.csv'

# Load existing data or create a new DataFrame
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=['Type', 'Name', 'Position', 'Company', 'Status', 'Amount', 'Currency', 'Probability', 'Start Date', 'Due Date'])

# Streamlit app layout
st.set_page_config(page_title="Recruitment Pipeline Tracker", layout="wide")
st.title('Recruitment Pipeline Tracker')

# Display logo
st.sidebar.image("logo.png", use_column_width=True)

# Home page with spreadsheet view
st.header("Recruitment Pipeline Overview")

# Use Mito's spreadsheet to display and edit the data
final_dfs, code = spreadsheet(df)

# Save changes back to CSV
if st.button('Save Changes'):
    final_dfs['dataframe'].to_csv(DATA_FILE, index=False)
    st.success('Changes saved!')

# Download the current dataset as CSV
st.download_button(
    label="Download Data as CSV",
    data=final_dfs['dataframe'].to_csv(index=False).encode('utf-8'),
    file_name='recruitment_pipeline.csv',
    mime='text/csv'
)

# Instructions for users
st.info("Use the spreadsheet above to add, edit, or remove entries. Click 'Save Changes' to persist your edits.")
