import streamlit as st
import pandas as pd
from datetime import date

# Define RecruitmentPipeline class with candidates, deals, and invoices management
class RecruitmentPipeline:
    def __init__(self):
        self.candidates = []  # List to store candidate details
        self.deals = []  # List to store deal details
        self.invoices = []  # List to store invoice details

    def add_candidate(self, name, position, status, start_date):
        self.candidates.append({
            'Name': name,
            'Position': position,
            'Status': status,
            'Start Date': start_date
        })

    def add_deal(self, company, amount, currency, probability):
        self.deals.append({
            'Company': company,
            'Amount': amount,
            'Currency': currency,
            'Probability': probability
        })

    def add_invoice(self, client_name, amount, due_date):
        self.invoices.append({
            'Client Name': client_name,
            'Amount': amount,
            'Due Date': due_date,
            'Status': 'Pending'
        })

    def get_candidates_report(self):
        total_candidates = len(self.candidates)
        started_candidates = [cand for cand in self.candidates if cand['Status'] == 'Started']
        return total_candidates, len(started_candidates)

    def get_deals_report(self):
        total_deals = len(self.deals)
        closed_deals = [deal for deal in self.deals if deal['Probability'] == 1.0]
        average_deal_size = sum(deal['Amount'] for deal in self.deals) / total_deals if total_deals > 0 else 0
        return total_deals, len(closed_deals), average_deal_size

    def get_invoices_report(self):
        pending_invoices = [inv for inv in self.invoices if inv['Status'] == 'Pending']
        return len(pending_invoices), sum(inv['Amount'] for inv in pending_invoices)

# Instantiate the recruitment pipeline
pipeline = RecruitmentPipeline()

# Streamlit app layout with tabs
st.set_page_config(page_title="Recruitment Pipeline Tracker", layout="wide")
st.title('Recruitment Pipeline Tracker')

tabs = st.tabs(["Current Pipeline", "Active Deals", "Offered Deals", "Started Candidates", "Invoices"])

# Current Pipeline Tab
with tabs[0]:
    st.header("Current Pipeline")
    with st.form(key='add_candidate'):
        candidate_name = st.text_input('Candidate Name')
        candidate_position = st.text_input('Position')
        candidate_status = st.selectbox('Status', ['Active', 'Rejected', 'Hired', 'Started'])
        candidate_start_date = st.date_input('Start Date', value=date.today())
        submit_candidate = st.form_submit_button('Add Candidate')

        if submit_candidate:
            pipeline.add_candidate(candidate_name, candidate_position, candidate_status, candidate_start_date)
            st.success('Candidate added!')

    total_candidates, started_candidates_count = pipeline.get_candidates_report()
    st.write(f"Total Candidates: {total_candidates}")
    st.write(f"Started Candidates: {started_candidates_count}")

# Active Deals Tab
with tabs[1]:
    st.header("Active Deals")
    with st.form(key='add_deal'):
        deal_company = st.text_input('Company')
        deal_amount = st.number_input('Amount', min_value=0.0)
        deal_currency = st.selectbox('Currency', ['GBP', 'USD', 'EUR'])
        deal_probability = st.slider('Probability of Deal Closing', 0.0, 1.0)
        submit_deal = st.form_submit_button('Add Deal')

        if submit_deal:
            pipeline.add_deal(deal_company, deal_amount, deal_currency, deal_probability)
            st.success('Deal added!')

    total_deals, closed_deals_count, average_deal_size = pipeline.get_deals_report()
    st.write(f"Total Deals: {total_deals}")
    st.write(f"Closed Deals: {closed_deals_count}")
    st.write(f"Average Deal Size: {average_deal_size:.2f} GBP")

# Offered Deals Tab
with tabs[2]:
    st.header("Offered Deals")
    # Display offered deals (assuming all deals are offered initially)
    if pipeline.deals:
        df_offered_deals = pd.DataFrame(pipeline.deals)
        df_offered_deals['Expected Value (GBP)'] = df_offered_deals.apply(
            lambda row: row['Amount'] * row['Probability'], axis=1)
        
        # Convert currencies to GBP (simplified; you would use an API for real rates)
        conversion_rates = {'USD': 0.75, 'EUR': 0.85}  # Example rates
        df_offered_deals['Amount (GBP)'] = df_offered_deals.apply(
            lambda row: row['Amount'] * conversion_rates.get(row['Currency'], 1), axis=1)

        st.dataframe(df_offered_deals[['Company', 'Amount (GBP)', 'Probability', 'Expected Value (GBP)']])
    else:
        st.write("No offered deals available.")

# Started Candidates Tab
with tabs[3]:
    st.header("Started Candidates")
    started_candidates = [cand for cand in pipeline.candidates if cand['Status'] == 'Started']
    
    if started_candidates:
        df_started_candidates = pd.DataFrame(started_candidates)
        st.dataframe(df_started_candidates[['Name', 'Position', 'Start Date']])
    else:
        st.write("No candidates have started yet.")

# Invoices Tab
with tabs[4]:
    st.header("Invoices")
    with st.form(key='add_invoice'):
        invoice_client_name = st.text_input('Client Name')
        invoice_amount = st.number_input('Invoice Amount', min_value=0.0)
        invoice_due_date = st.date_input('Due Date', value=date.today())
        submit_invoice = st.form_submit_button('Add Invoice')

        if submit_invoice:
            pipeline.add_invoice(invoice_client_name, invoice_amount, invoice_due_date)
            st.success('Invoice added!')

    pending_invoices_count, pending_amount_total = pipeline.get_invoices_report()
    st.write(f"Pending Invoices: {pending_invoices_count}")
    st.write(f"Total Pending Amount: {pending_amount_total:.2f} GBP")

# Display logo in the sidebar
st.sidebar.image("logo.png", use_column_width=True)
