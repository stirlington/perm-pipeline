import streamlit as st
import pandas as pd
import os

# File paths for data persistence
DATA_FILE = 'recruitment_data.csv'

# Load or initialize data
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=['Type', 'Name', 'Client', 'Vacancy', 'Terms %', 'Probability %', 'Salary', 'Fee £', 'Probability Fee £', 'Projected Month', 'Start Month', 'Status', 'Interview Stage'])
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

# Define month options globally to avoid NameError
month_options = [f"{month} {year}" for year in range(2024, 2027) for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]

# Main navigation
page = st.sidebar.selectbox("Navigate", ["Home", "Pipeline", "Offered", "Invoiced"])

if page == "Home":
    st.title('Recruitment Pipeline Overview')
    
    # Calculate total pipeline value
    total_value = df['Probability Fee £'].sum()
    st.metric("Total Pipeline Value (£)", f"{total_value:,.2f}")

    # Monthly projection dropdown
    selected_month = st.selectbox("Select Month for Projection", month_options)
    
    # Show projected value for selected month
    projected_value = df[df['Projected Month'] == selected_month]['Probability Fee £'].sum()
    st.metric(f"Projected Value for {selected_month} (£)", f"{projected_value:,.2f}")

elif page == "Pipeline":
    st.title('Manage Recruitment Pipeline')
    
    # Form to add new entries
    with st.form(key='add_entry'):
        type_ = st.selectbox('Type', ['Permanent', 'Contract'])
        name = st.text_input('Candidate Name')
        client = st.text_input('Client Name')
        vacancy = st.text_input('Vacancy')
        terms = st.number_input('Terms %', min_value=0.0, max_value=100.0, step=0.1)
        probability = st.number_input('Probability %', min_value=0.0, max_value=100.0, step=0.1)
        salary = st.number_input('Salary (£)', min_value=0.0, step=1000.0)
        projected_month = st.selectbox("Projected Offer Month", month_options)
        start_month = st.selectbox("Start/Invoice Month", month_options)
        status = st.selectbox('Status', ['Active', 'Offered', 'Accepted', 'Rejected'])
        interview_stage = st.selectbox('Interview Stage', ['1st Stage', '2nd Stage', '3rd Stage', 'Final Stage'])
        
        # Submit button for the form
        submit_entry = st.form_submit_button('Add Entry')

        if submit_entry:
            new_entry = pd.DataFrame([{
                'Type': type_,
                'Name': name,
                'Client': client,
                'Vacancy': vacancy,
                'Terms %': terms,
                'Probability %': probability,
                'Salary': salary,
                'Fee £': salary * (terms / 100),
                'Probability Fee £': salary * (terms / 100) * (probability / 100),
                'Projected Month': projected_month,
                'Start Month': start_month,
                'Status': status,
                'Interview Stage': interview_stage
            }])
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Entry added successfully!")

    # Display current pipeline data with deletion option
    if not df.empty:
        df_display = calculate_fees(df.copy())
        
        # Create a list to track rows marked for deletion or update
        rows_to_delete = []
        
        # Display the table with buttons for each row
        for i in range(len(df_display)):
            row_data = df_display.iloc[i]
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write(row_data.to_dict())
            with col2:
                if st.button(f'Delete {i}', key=f'del_{i}'):
                    rows_to_delete.append(i)
            with col3:
                if st.button(f'Mark Failed {i}', key=f'fail_{i}'):
                    df_display.at[i, 'Status'] = 'Failed/Pulled Out'
                    df_display.to_csv(DATA_FILE, index=False)
                    st.success(f"Entry {i} marked as Failed/Pulled Out!")
        
        # Delete rows after confirmation
        if rows_to_delete:
            confirm_delete = st.button("Confirm Deletion")
            if confirm_delete:
                df_display.drop(rows_to_delete, inplace=True)
                df_display.reset_index(drop=True, inplace=True)
                df_display.to_csv(DATA_FILE, index=False)
                st.success("Selected entries deleted successfully!")
        
        # Refresh the dataframe display after modifications
        if not df_display.empty:
            st.dataframe(df_display)

elif page == "Offered":
    st.title('Offered Candidates')
    
    offered_candidates = df[df['Status'].isin(['Offered', 'Accepted', 'Rejected'])]
    
    if not offered_candidates.empty:
        offered_stats = offered_candidates.groupby('Status').size()
        st.write(offered_stats)
        st.dataframe(offered_candidates)

elif page == "Invoiced":
    st.title('Invoiced Candidates')
    
    invoiced_candidates = df[df['Status'] == 'Accepted']
    
    if not invoiced_candidates.empty:
        invoiced_by_month = invoiced_candidates.groupby('Start Month')['Probability Fee £'].sum()
        st.write(invoiced_by_month)
        st.dataframe(invoiced_candidates)

# Download button for the full dataset
st.sidebar.download_button(
    label="Download Full Dataset as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name='recruitment_pipeline.csv',
    mime='text/csv'
)
