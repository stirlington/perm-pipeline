import streamlit as st
import pandas as pd
import os

# File paths for data persistence
DATA_FILE = 'recruitment_data.csv'

# Load or initialize data
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Candidate Name', 'Client', 'Vacancy', 'Salary', 'Terms %', 'Probability %', 'Fee £', 'Probability Fee £', 'Projected Month', 'Status'])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

# Function to calculate fees
def calculate_fees(df):
    df['Fee £'] = df['Salary'] * (df['Terms %'] / 100)
    df['Probability Fee £'] = df['Fee £'] * (df['Probability %'] / 100)
    return df

# Streamlit app layout
st.set_page_config(page_title="Recruitment Pipeline Tracker", layout="wide")

# Sidebar logo
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.warning("Logo file not found. Please ensure 'logo.png' is in the root directory.")

# Define month options globally
month_options = [f"{month} {year}" for year in range(2024, 2027) for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]

# Main navigation
page = st.sidebar.selectbox("Navigate", ["Pipeline"])

if page == "Pipeline":
    st.title('Manage Recruitment Pipeline')
    
    # Form to add new entries
    with st.form(key='add_entry'):
        name = st.text_input('Candidate Name')
        client = st.text_input('Client')
        vacancy = st.text_input('Vacancy')
        salary = st.number_input('Salary (£)', min_value=0.0, step=1000.0)
        terms = st.number_input('Terms %', min_value=0.0, max_value=100.0, step=0.1)
        probability = st.number_input('Probability %', min_value=0.0, max_value=100.0, step=0.1)
        projected_month = st.selectbox("Projected Month (optional)", [""] + month_options)
        
        # Submit button for the form
        submit_entry = st.form_submit_button('Add Entry')

        if submit_entry and name and client and vacancy:
            new_entry = pd.DataFrame([{
                'Candidate Name': name,
                'Client': client,
                'Vacancy': vacancy,
                'Salary': salary,
                'Terms %': terms,
                'Probability %': probability,
                'Fee £': salary * (terms / 100),
                'Probability Fee £': salary * (terms / 100) * (probability / 100),
                'Projected Month': projected_month if projected_month else None,
                'Status': 'Active'
            }])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Entry added successfully!")

    # Display current pipeline data with deletion option
    if not df.empty:
        df_display = calculate_fees(df.copy())
        
        # Display the table with options to delete or mark as failed
        for i in range(len(df_display)):
            row_data = df_display.iloc[i]
            col1, col2, col3 = st.columns([8, 1, 1])
            with col1:
                st.write(row_data.to_frame().T.style.hide(axis='index'))
            with col2:
                if st.button(f'Delete {i}', key=f'del_{i}'):
                    df_display.drop(i, inplace=True)
                    df_display.reset_index(drop=True, inplace=True)
                    df_display.to_csv(DATA_FILE, index=False)
                    st.success(f"Entry {i} deleted successfully!")
            with col3:
                if st.button(f'Mark Failed {i}', key=f'fail_{i}'):
                    df_display.at[i, 'Status'] = 'Failed/Pulled Out'
                    df_display.to_csv
