import streamlit as st
import pandas as pd
import os

# File paths for data persistence
DATA_FILE = 'recruitment_data.csv'

# Load or initialize data
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Vacancy', 'Candidates', 'Client', 'Lowest Salary', 'Terms %', 'Probability %', 'Projected Fee £', 'Projected Month', 'Status'])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

# Function to calculate fees
def calculate_fees(df):
    df['Projected Fee £'] = df['Lowest Salary'] * (df['Terms %'] / 100) * (df['Probability %'] / 100)
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
page = st.sidebar.selectbox("Navigate", ["Home", "Pipeline", "Offered", "Invoiced"])

if page == "Home":
    st.title('Recruitment Pipeline Overview')
    
    # Calculate total pipeline value
    total_value = df['Projected Fee £'].sum()
    st.metric("Total Pipeline Value (£)", f"{total_value:,.2f}")

    # Monthly projection dropdown
    selected_month = st.selectbox("Select Month for Projection", month_options)
    
    # Show projected value for selected month
    projected_value = df[df['Projected Month'] == selected_month]['Projected Fee £'].sum()
    st.metric(f"Projected Value for {selected_month} (£)", f"{projected_value:,.2f}")

elif page == "Pipeline":
    st.title('Manage Recruitment Pipeline')
    
    # Form to add new entries in a row format
    with st.form(key='add_entry'):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        with col1:
            vacancy = st.text_input('Vacancy')
        with col2:
            candidate_name = st.text_input('Candidate Name')
        with col3:
            client = st.text_input('Client')
        with col4:
            salary = st.number_input('Salary (£)', min_value=0.0, step=1000.0)
        with col5:
            terms = st.number_input('Terms %', min_value=0.0, max_value=100.0, step=0.1)
        with col6:
            probability = st.number_input('Probability %', min_value=0.0, max_value=100.0, step=0.1)
        with col7:
            projected_month = st.selectbox("Projected Month (optional)", [""] + month_options)
        
        # Submit button for the form
        submit_entry = st.form_submit_button('Add Entry')

        if submit_entry and vacancy and candidate_name and client:
            if vacancy in df['Vacancy'].values:
                idx = df[df['Vacancy'] == vacancy].index[0]
                current_candidates = df.at[idx, 'Candidates']
                current_salaries = df.at[idx, 'Lowest Salary']
                
                updated_candidates = f"{current_candidates}, {candidate_name}" if current_candidates else candidate_name
                updated_salaries = min(current_salaries, salary) if current_salaries else salary
                
                df.at[idx, 'Candidates'] = updated_candidates
                df.at[idx, 'Lowest Salary'] = updated_salaries
                df.at[idx, 'Terms %'] = terms
                df.at[idx, 'Probability %'] = probability
                df.at[idx, 'Projected Fee £'] = updated_salaries * (terms / 100) * (probability / 100)
                df.at[idx, 'Projected Month'] = projected_month if projected_month else None

            else:
                new_entry = pd.DataFrame([{
                    'Vacancy': vacancy,
                    'Candidates': candidate_name,
                    'Client': client,
                    'Lowest Salary': salary,
                    'Terms %': terms,
                    'Probability %': probability,
                    'Projected Fee £': salary * (terms / 100) * (probability / 100),
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
                    df_display.to_csv(DATA_FILE, index=False)
                    st.success(f"Entry {i} marked as Failed/Pulled Out!")
        
        # Refresh the dataframe display after modifications
        if not df_display.empty:
            st.dataframe(df_display)

elif page == "Offered":
    st.title('Offered Candidates')
    
    offered_candidates = df[df['Status'].isin(['Offered', 'Accepted'])]
    
    if not offered_candidates.empty:
        offered_stats = offered_candidates.groupby('Status').size()
        st.write(offered_stats)
        st.dataframe(offered_candidates)

elif page == "Invoiced":
    st.title('Invoiced Candidates')
    
    invoiced_candidates = df[df['Status'] == 'Accepted']
    
    if not invoiced_candidates.empty:
        invoiced_by_month = invoiced_candidates.groupby('Projected Month')['Projected Fee £'].sum()
        st.write(invoiced_by_month)
        st.dataframe(invoiced_candidates)

# Download button for the full dataset
st.sidebar.download_button(
    label="Download Full Dataset as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='recruitment_pipeline.csv',
    mime='text/csv'
)
