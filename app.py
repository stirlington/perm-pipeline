import streamlit as st
import pandas as pd
from datetime import date

# Define RecruitmentPipeline class with candidates, deals, and invoices management
class RecruitmentPipeline:
    def __init__(self):
        self.candidates = []  # List to store candidate details
        self.deals = []  # List to store deal details
        self.invoices = []  # List to store invoice details

    def add_candidate(self, name, position, status, probability):
        self.candidates.append({
            'Name': name,
            'Position': position,
            'Status': status,
            'Probability': probability
        })

    def remove_candidate(self, name):
        self.candidates = [cand for cand in self.candidates if cand['Name'] != name]

    def add_deal(self, company, amount, currency, probability):
        self.deals.append({
            'Company': company,
            'Amount': amount,
            'Currency': currency,
            'Probability': probability
        })

    def remove_deal(self, company):
        self.deals = [deal for deal in self.deals if deal['Company'] != company]

    def add_invoice(self, client_name, amount, due_date):
        self.invoices.append({
            'Client Name': client_name,
            'Amount': amount,
            'Due Date': due_date,
            'Status': 'Pending'
        })

    def get_candidates_report(self):
        total_candidates = len(self.candidates)
        rejected_candidates = [cand for cand in self.candidates if cand['Status'] == 'Rejected']
        return total_candidates, len(rejected_candidates)

    def get_deals_report(self):
        total_deals = len(self.deals)
        closed_deals = [deal for deal in self.deals if deal['Probability'] == 1.0]
        average_deal_size = sum(deal['Amount'] for deal in self.deals) / total_deals if total_deals > 0 else 0
        return total_deals, len(closed_deals), average_deal_size

# Instantiate the recruitment pipeline
pipeline = RecruitmentPipeline()

# Streamlit app layout
st.title('Recruitment Pipeline Tracker')

# Add candidate form
with st.form(key='add_candidate'):
    candidate_name = st.text_input('Candidate Name')
    candidate_position = st.text_input('Position')
    candidate_status = st.selectbox('Status', ['Active', 'Rejected', 'Hired'])
    candidate_probability = st.slider('Probability of Success', 0.0, 1.0)
    submit_candidate = st.form_submit_button('Add Candidate')

    if submit_candidate:
        pipeline.add_candidate(candidate_name, candidate_position, candidate_status, candidate_probability)
        st.success('Candidate added!')

# Add deal form
with st.form(key='add_deal'):
    deal_company = st.text_input('Company')
    deal_amount = st.number_input('Amount', min_value=0.0)
    deal_currency = st.selectbox('Currency', ['GBP', 'USD', 'EUR'])
    deal_probability = st.slider('Probability of Deal Closing', 0.0, 1.0)
    submit_deal = st.form_submit_button('Add Deal')

    if submit_deal:
        pipeline.add_deal(deal_company, deal_amount, deal_currency, deal_probability)
        st.success('Deal added!')

# Add invoice form
with st.form(key='add_invoice'):
    invoice_client_name = st.text_input('Client Name')
    invoice_amount = st.number_input('Invoice Amount', min_value=0.0)
    invoice_due_date = st.date_input('Due Date', value=date.today())
    submit_invoice = st.form_submit_button('Add Invoice')

    if submit_invoice:
        pipeline.add_invoice(invoice_client_name, invoice_amount, invoice_due_date)
        st.success('Invoice added!')

# Display reports
st.write("## Candidates Report")
total_candidates, rejected_candidates_count = pipeline.get_candidates_report()
st.write(f"Total Candidates: {total_candidates}")
st.write(f"Rejected Candidates: {rejected_candidates_count}")

st.write("## Deals Report")
total_deals, closed_deals_count, average_deal_size = pipeline.get_deals_report()
st.write(f"Total Deals: {total_deals}")
st.write(f"Closed Deals: {closed_deals_count}")
st.write(f"Average Deal Size: {average_deal_size:.2f} GBP")

# Display logo in the sidebar
st.sidebar.image("logo.png", use_column_width=True)
