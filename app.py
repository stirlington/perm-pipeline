import streamlit as st
import pandas as pd
import os  # Ensure the os module is imported

# File paths for data persistence
DATA_FILE = 'recruitment_data.csv'

# Load or initialize data
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        'Consultant', 'Client Name', 'Role', 'Candidates', 'Salary', 'Currency',
        'Fee %', 'Fee (£)', 'Probability %', 'Probability Fee (£)',
        'VAT', 'Est. Invoice Month', 'Status'
    ])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

# Function to calculate fees
def calculate_fees(row):
    fee = row['Salary'] * (row['Fee %'] / 100)
    probability_fee = fee * (row['Probability %'] / 100)
    return fee, probability_fee

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
page = st.sidebar.selectbox("Navigate", ["Pipeline", "Offered", "Invoiced"])

if page == "Pipeline":
    st.title('Manage Recruitment Pipeline')

    # Editable dataframe using st.experimental_data_editor
    edited_df = st.experimental_data_editor(
        df,
        num_rows="dynamic",
        column_config={
            "Consultant": st.column_config.SelectboxColumn(options=["Chris", "Max"]),
            "Currency": st.column_config.SelectboxColumn(options=["USD", "GBP", "EUR"]),
            "VAT": st.column_config.SelectboxColumn(options=["Yes", "No"]),
            "Est. Invoice Month": st.column_config.SelectboxColumn(options=month_options),
        }
    )

    # Calculate fees and update dataframe
    for idx in edited_df.index:
        fee, probability_fee = calculate_fees(edited_df.loc[idx])
        edited_df.at[idx, 'Fee (£)'] = fee
        edited_df.at[idx, 'Probability Fee (£)'] = probability_fee

    # Update CSV with changes
    if st.button("Save Changes"):
        edited_df.to_csv(DATA_FILE, index=False)
        st.success("Changes saved successfully!")

    # Display total fees
    total_fee = edited_df['Fee (£)'].sum()
    total_probability_fee = edited_df['Probability Fee (£)'].sum()
    
    st.write(f"Total Fee: £{total_fee:,.2f}")
    st.write(f"Total Probability Fee: £{total_probability_fee:,.2f}")

elif page == "Offered":
    st.title('Offered Candidates')
    
elif page == "Invoiced":
    st.title('Invoiced Candidates')

# Download button for the full dataset
st.sidebar.download_button(
    label="Download Full Dataset as CSV",
    data=edited_df.to_csv(index=False).encode('utf-8'),
    file_name='recruitment_pipeline.csv',
    mime='text/csv'
)
