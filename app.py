import streamlit as st
import pandas as pd

# Title and description
st.title("Recruitment Pipeline Tracker")
st.write("This app helps you track and manage your recruitment pipeline.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Candidate", "Pipeline Overview"])

# Placeholder data for the pipeline
if "pipeline_data" not in st.session_state:
    st.session_state.pipeline_data = pd.DataFrame({
        "Candidate Name": [],
        "Stage": [],
        "Source": [],
        "Date Added": []
    })

# Dashboard page
if page == "Dashboard":
    st.header("Dashboard")
    st.write("Overview of recruitment metrics will go here.")

# Add Candidate page
elif page == "Add Candidate":
    st.header("Add Candidate")
    with st.form("add_candidate_form"):
        name = st.text_input("Candidate Name")
        stage = st.selectbox("Stage", ["Sourced", "Screening", "Interviewing", "Offer Sent", "Hired", "Rejected"])
        source = st.text_input("Source")
        date_added = st.date_input("Date Added")
        submitted = st.form_submit_button("Add Candidate")

        if submitted:
            new_data = pd.DataFrame({
                "Candidate Name": [name],
                "Stage": [stage],
                "Source": [source],
                "Date Added": [date_added]
            })
            st.session_state.pipeline_data = pd.concat([st.session_state.pipeline_data, new_data], ignore_index=True)
            st.success("Candidate added successfully!")

# Pipeline Overview page
elif page == "Pipeline Overview":
    st.header("Pipeline Overview")
    st.write("Below is the current recruitment pipeline:")
    st.dataframe(st.session_state.pipeline_data)
