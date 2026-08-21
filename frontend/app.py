import sys
import os

# Ensure root project directory, backend directory, and frontend directory are in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(ROOT_DIR, "backend"))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

import streamlit as st
import requests
import json
import time
import re

try:
    import utils
except ImportError:
    from frontend import utils

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.roi_engine import get_applicable_roi
from backend.msme_scoring_engine import calculate_mse_existing_score, calculate_mse_new_score, assign_cbi_risk_grade
from backend.financial_intelligence import (
    FinancialStatementSpreader,
    RatioDiagnosticsEngine,
    ForensicAuditor,
    FinancialForecaster,
    EnterpriseValuator,
    MSEParameterAutoMapper
)
from backend.corporate_profiles import CORPORATE_PROFILES
from backend.financial_document_parser import FinancialDocumentParser

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="CBoI Intelligent Loan Appraisal", layout="wide")

# Initialize session state
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None
if "ocr_data" not in st.session_state:
    st.session_state.ocr_data = {}
if "ocr_done" not in st.session_state:
    st.session_state.ocr_done = False
if "role" not in st.session_state:
    st.session_state.role = "Applicant"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "polling" not in st.session_state:
    st.session_state.polling = False

# Sidebar Auth
st.sidebar.title("🔐 Authentication")
st.session_state.role = st.sidebar.radio("Select Role", ["Applicant", "Credit Manager"])

if st.session_state.role == "Credit Manager":
    if not st.session_state.logged_in:
        def do_login():
            if st.session_state.get("passcode_input") == "CBOI_ADMIN":
                st.session_state.logged_in = True
            else:
                st.session_state.login_error = "Invalid Passcode"
                
        st.sidebar.text_input("Enter Passcode", type="password", key="passcode_input", on_change=do_login)
        st.sidebar.button("Login", on_click=do_login)
        
        if st.session_state.get("login_error"):
            st.sidebar.error(st.session_state.login_error)
            st.session_state.login_error = ""
    else:
        st.sidebar.success("Authenticated as Credit Manager")
        def do_logout():
            st.session_state.logged_in = False
        st.sidebar.button("Logout", on_click=do_logout)

st.title("🏦 Central Bank of India - Intelligent Loan Appraisal")
st.markdown("Powered by the Central Bank Automated Underwriting Engine")

# Render Local Logo
logo_path = os.path.join(FRONTEND_DIR, "Logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=300)
elif os.path.exists("Logo.png"):
    st.image("Logo.png", width=300)

if st.session_state.role == "Applicant":
    tabs = st.tabs(["📄 Applicant Portal"])
    tab1 = tabs[0]
    tab_corp = None
    tab2 = None
else:
    if not (st.session_state.role == "Credit Manager" and st.session_state.logged_in):
        tabs = st.tabs(["📄 Applicant Portal", "🔒 Manager Access Required"])
        tab1 = tabs[0]
        tab_corp = None
        tab2 = tabs[1]
    else:
        tabs = st.tabs(["📄 Applicant Portal", "🏢 Corporate Financial Intelligence & Valuation Hub", "🛡️ Credit Manager Dashboard"])
        tab1 = tabs[0]
        tab_corp = tabs[1]
        tab2 = tabs[2]

with tab1:
    tab_apply, tab_track = st.tabs(["📝 Submit New Application", "🔍 Track Application Status"])
    
    with tab_apply:
        st.header("Loan Application Form")
        st.markdown("Submit your details for formal automated appraisal.")

        # --- 1-CLICK DEMO CASE LOADER ---
        with st.expander("⚡ 1-Click Demo Profiles Loader (Instant Auto-Fill for Testing / Evaluation)", expanded=False):
            st.markdown("Select a benchmark pre-configured banking profile to instantly populate all underwriting parameters:")
            demo_choice = st.selectbox(
                "Choose Demo Profile:",
                [
                    "-- Select Demo Case --",
                    "1. Dr. Rajesh Sharma (Retail Home Loan - Prime 790 CIBIL - Approved @ 7.40%)",
                    "2. Sunita Menon (Retail Auto Loan - 765 CIBIL - Approved @ 8.20%)",
                    "3. Amitabh Verma (Retail Personal Loan - 750 CIBIL - Clean 11.25%)",
                    "4. Apex Precision Engineering (MSME Existing - Form MSE 1 - CBI 1 Prime - Fast-Track @ 8.15%)",
                    "5. Surat Silk & Synthetics (MSME Existing - Form MSE 1 - CBI 5 - Approved with Covenants)",
                    "6. BioGreen Agro Processing (MSME Greenfield - Form MSE II - CBI 2 - CGTMSE Backed @ 8.15%)",
                    "7. Sunrise Biofuels Startup (MSME Greenfield - Form MSE II - CBI 10 - Sub-Hurdle Rate Rejected)",
                    "8. Defaulter Steels LLP (MSME Existing - Form MSE 1 - Defaulter Override - Score 0 / CBI 10 Rejected)"
                ],
                key="demo_profile_selector"
            )
            if demo_choice != "-- Select Demo Case --":
                if "Dr. Rajesh Sharma" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Dr. Rajesh Sharma", "age": 42, "gender": "Male", "marital_status": "Married", "category": "GEN",
                        "occupation": "Salaried", "gross_monthly_income": 350000, "net_monthly_income": 280000, "total_assets": 25000000,
                        "credit_score": 790, "avg_credit_balance_6m": 800000, "existing_emi": 20000, "active_lines": 1, "inquiries_6m": 0,
                        "loan_amount": 5000000, "tenure_months": 240, "loan_type": "Home Loan", "property_value": 8500000, "security_type": "Property"
                    }
                elif "Sunita Menon" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Sunita Menon", "age": 36, "gender": "Female", "marital_status": "Single", "category": "GEN",
                        "occupation": "Salaried", "gross_monthly_income": 180000, "net_monthly_income": 140000, "total_assets": 9000000,
                        "credit_score": 765, "avg_credit_balance_6m": 350000, "existing_emi": 15000, "active_lines": 2, "inquiries_6m": 1,
                        "loan_amount": 1200000, "tenure_months": 60, "loan_type": "Auto Loan", "property_value": 1600000, "security_type": "Vehicle"
                    }
                elif "Amitabh Verma" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Amitabh Verma", "age": 31, "gender": "Male", "marital_status": "Single", "category": "GEN",
                        "occupation": "Salaried", "gross_monthly_income": 140000, "net_monthly_income": 115000, "total_assets": 4500000,
                        "credit_score": 750, "avg_credit_balance_6m": 250000, "existing_emi": 8000, "active_lines": 1, "inquiries_6m": 1,
                        "loan_amount": 400000, "tenure_months": 36, "loan_type": "Personal Loan", "property_value": 0, "security_type": "None"
                    }
                elif "Apex Precision Engineering" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Apex Precision Engineering Pvt Ltd", "age": 48, "gender": "Male", "marital_status": "Married", "category": "GEN",
                        "occupation": "Business", "gross_monthly_income": 450000, "net_monthly_income": 380000, "total_assets": 18000000,
                        "credit_score": 780, "avg_credit_balance_6m": 600000, "existing_emi": 35000, "active_lines": 3, "inquiries_6m": 0,
                        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - Existing Unit", "property_value": 8000000, "security_type": "Property",
                        "current_ratio": 1.45, "debt_equity_ratio": 1.5, "sales_growth_rate": 22.0, "pat_margin": 16.0,
                        "sanction_compliance": "Compliant", "stock_statement_status": "Timely", "debt_servicing_history": "Within 1 month",
                        "inventory_compliance": "Fair Compliance", "bills_culture": True, "bill_payment_record": "Prompt",
                        "review_documents_timely": True, "lc_bg_status": "Prompt / No Facility", "ancillary_relationship": "Substantial"
                    }
                elif "Surat Silk" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Surat Silk & Synthetics Mills", "age": 52, "gender": "Male", "marital_status": "Married", "category": "GEN",
                        "occupation": "Business", "gross_monthly_income": 380000, "net_monthly_income": 290000, "total_assets": 12000000,
                        "credit_score": 715, "avg_credit_balance_6m": 400000, "existing_emi": 40000, "active_lines": 3, "inquiries_6m": 1,
                        "loan_amount": 4500000, "tenure_months": 60, "loan_type": "MSME Loan - Existing Unit", "property_value": 6500000, "security_type": "Property",
                        "current_ratio": 1.25, "debt_equity_ratio": 2.6, "sales_growth_rate": 12.0, "pat_margin": 8.0,
                        "sanction_compliance": "Compliant", "stock_statement_status": "Monthly", "debt_servicing_history": "Within 2 months",
                        "inventory_compliance": "Fair Compliance", "bills_culture": True, "bill_payment_record": "Prompt",
                        "review_documents_timely": True, "lc_bg_status": "Prompt / No Facility", "ancillary_relationship": "Moderate"
                    }
                elif "BioGreen Agro" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "BioGreen Agro Processing LLP", "age": 39, "gender": "Female", "marital_status": "Married", "category": "GEN",
                        "occupation": "Business", "gross_monthly_income": 400000, "net_monthly_income": 320000, "total_assets": 14000000,
                        "credit_score": 755, "avg_credit_balance_6m": 500000, "existing_emi": 20000, "active_lines": 2, "inquiries_6m": 1,
                        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - New Unit", "property_value": 6500000, "security_type": "CGTMSE / Plant & Machinery",
                        "projected_sales_growth": 18.0, "projected_pat_margin": 14.0, "projected_der": 1.8,
                        "inputs_access": "Locally Available / Tied up", "market_access": "Locally Available / Tied up",
                        "promoter_experience": "Qualified and Experienced", "bank_relationship": "Existing Customer",
                        "premises_type": "Owned", "collateral_coverage": "Covered under CGTMSE Scheme", "cgtmse_covered": True
                    }
                elif "Sunrise Biofuels" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Sunrise Biofuels Startup", "age": 33, "gender": "Male", "marital_status": "Single", "category": "GEN",
                        "occupation": "Business", "gross_monthly_income": 120000, "net_monthly_income": 85000, "total_assets": 3000000,
                        "credit_score": 620, "avg_credit_balance_6m": 100000, "existing_emi": 45000, "active_lines": 4, "inquiries_6m": 3,
                        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - New Unit", "property_value": 2000000, "security_type": "None",
                        "projected_sales_growth": 3.0, "projected_pat_margin": 2.0, "projected_der": 4.5,
                        "inputs_access": "Not Identified", "market_access": "Unidentified",
                        "promoter_experience": "No qualification/experience", "bank_relationship": "Introduced by Govt Dept / Others",
                        "premises_type": "Leased / Rented", "collateral_coverage": "Unsecured", "cgtmse_covered": False
                    }
                elif "Defaulter Steels" in demo_choice:
                    st.session_state.ocr_data = {
                        "name": "Defaulter Steels LLP", "age": 50, "gender": "Male", "marital_status": "Married", "category": "GEN",
                        "occupation": "Business", "gross_monthly_income": 300000, "net_monthly_income": 220000, "total_assets": 5000000,
                        "credit_score": 550, "avg_credit_balance_6m": 10000, "existing_emi": 80000, "active_lines": 5, "inquiries_6m": 4,
                        "loan_amount": 3000000, "tenure_months": 48, "loan_type": "MSME Loan - Existing Unit", "property_value": 4000000, "security_type": "Property",
                        "current_ratio": 0.90, "debt_equity_ratio": 4.5, "sales_growth_rate": -5.0, "pat_margin": -2.0,
                        "sanction_compliance": "Non-compliant", "stock_statement_status": "Non-Submission", "debt_servicing_history": "Overdue > 3 months",
                        "inventory_compliance": "High deviation", "bills_culture": False, "bill_payment_record": "Overdue > 3 months",
                        "review_documents_timely": False, "lc_bg_status": "Devolvement / Invocation", "ancillary_relationship": "None"
                    }
                st.success(f"Loaded demo profile: {demo_choice.split('(')[0].strip()}! Values populated below.")
    
        st.subheader("📸 Auto-Fill via Scan (OCR)")
        uploaded_file = st.file_uploader("Upload Scanned Application (PNG/JPG)", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None and not st.session_state.ocr_done:
            with st.spinner("Extracting data with EasyOCR..."):
                extracted = utils.extract_ocr_data(uploaded_file.read())
                st.session_state.ocr_data = extracted
                st.session_state.ocr_done = True
                st.success("Extracted! Please review the auto-filled fields below.")
                st.rerun()
                
        if uploaded_file is None and not st.session_state.ocr_data:
            st.session_state.ocr_done = False
        
        # Reactive Loan Application Form (Instant rendering without form lag)
        with st.expander("1. Personal Information", expanded=True):
            col1, col2, col3 = st.columns(3)
            name = col1.text_input("Applicant / Entity Name", st.session_state.ocr_data.get('name', "John Doe"))
            age = col2.number_input("Age (or Vintage in Yrs)", min_value=18, max_value=80, value=int(st.session_state.ocr_data.get('age', 35)))
            gender_default = st.session_state.ocr_data.get('gender', 'Male')
            gender_idx = ["Male", "Female", "Other"].index(gender_default) if gender_default in ["Male", "Female", "Other"] else 0
            gender = col3.selectbox("Gender", ["Male", "Female", "Other"], index=gender_idx)
            
            col4, col5 = st.columns(2)
            mar_default = st.session_state.ocr_data.get('marital_status', 'Married')
            mar_idx = ["Single", "Married", "Divorced", "Widowed"].index(mar_default) if mar_default in ["Single", "Married", "Divorced", "Widowed"] else 1
            marital_status = col4.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"], index=mar_idx)
            cat_default = st.session_state.ocr_data.get('category', 'GEN')
            cat_idx = ["GEN", "OBC", "SC", "ST"].index(cat_default) if cat_default in ["GEN", "OBC", "SC", "ST"] else 0
            category = col5.selectbox("Category", ["GEN", "OBC", "SC", "ST"], index=cat_idx)

        with st.expander("2. Employment & Financial Capacity", expanded=True):
            col1, col2 = st.columns(2)
            occ_default = st.session_state.ocr_data.get('occupation', 'Business')
            occ_opts = ["Salaried", "Self_Employed", "Business", "Professional", "Retired"]
            occ_idx = occ_opts.index(occ_default) if occ_default in occ_opts else 2
            occupation = col1.selectbox("Occupation / Entity Type", occ_opts, index=occ_idx)
            gross_income = col2.number_input("Gross Monthly Income / Revenue (₹)", min_value=0, value=int(float(st.session_state.ocr_data.get('gross_monthly_income', 150000))), step=10000)
            
            col3, col4 = st.columns(2)
            net_income = col3.number_input("Net Monthly Income / Profit (₹)", min_value=0, value=int(float(st.session_state.ocr_data.get('net_monthly_income', 120000))), step=10000)
            total_assets = col4.number_input("Total Assets Value (₹)", min_value=0, value=int(float(st.session_state.ocr_data.get('total_assets', 15000000))), step=500000)

        with st.expander("3. Credit & Bureau History", expanded=True):
            st.info("CIBIL Score is highly weighted in the risk assessment.")
            col1, col2 = st.columns(2)
            credit_score = col1.number_input("Credit Score (CIBIL)", min_value=300, max_value=900, value=int(st.session_state.ocr_data.get('credit_score', 750)), step=10)
            avg_credit_balance_6m = col2.number_input("Avg Bank Balance (Last 6M) (₹)", min_value=0, value=int(float(st.session_state.ocr_data.get('avg_credit_balance_6m', 500000))), step=10000)
            
            col3, col4, col5 = st.columns(3)
            existing_emi = col3.number_input("Existing Monthly EMI (₹)", min_value=0, value=int(float(st.session_state.ocr_data.get('existing_emi', 25000))), step=5000)
            active_lines = col4.number_input("Active Credit Lines", min_value=0, value=int(st.session_state.ocr_data.get('active_lines', 2)), step=1)
            inquiries_6m = col5.number_input("Hard Inquiries (Last 6M)", min_value=0, value=int(st.session_state.ocr_data.get('inquiries_6m', 0)), step=1)

        with st.expander("4. Loan Request & Facility Details", expanded=True):
            col1, col2 = st.columns(2)
            loan_amount = col1.number_input("Requested Loan Amount (₹)", min_value=100000, value=int(float(st.session_state.ocr_data.get('loan_amount', 5000000))), step=100000)
            tenure_months = col2.number_input("Tenure (Months)", min_value=12, value=int(st.session_state.ocr_data.get('tenure_months', 240)), step=12)
            
            col3, col4 = st.columns(2)
            col3.info("Interest Rate: 🏦 Auto-Assigned by Central Bank of India Policy")
            ltype_default = st.session_state.ocr_data.get('loan_type', 'Home Loan')
            ltype_opts = ["Home Loan", "Auto Loan", "Personal Loan", "Education Loan", "MSME Loan - Existing Unit", "MSME Loan - New Unit"]
            ltype_idx = ltype_opts.index(ltype_default) if ltype_default in ltype_opts else 0
            loan_type = col4.selectbox("Loan Type", ltype_opts, index=ltype_idx, key="loan_type_select")
            
            col5, col6 = st.columns(2)
            property_value = col5.number_input("Property / Primary Collateral Value (₹)", min_value=0, value=int(float(st.session_state.ocr_data.get('property_value', 7000000))), step=100000)
            sec_default = st.session_state.ocr_data.get('security_type', 'Property')
            sec_opts = ["Property", "Vehicle", "Liquid_Assets", "CGTMSE / Plant & Machinery", "None"]
            sec_idx = sec_opts.index(sec_default) if sec_default in sec_opts else 0
            security_type = col6.selectbox("Security Type", sec_opts, index=sec_idx)
        
        # Reactive MSME Scoring Parameters (Instantly displayed when MSME is selected)
        msme_data = {}
        if "MSME" in loan_type:
            if "New" in loan_type:
                with st.expander("🏢 Central Bank of India MSME Scoring Parameters (Form MSE II - New Greenfield Units)", expanded=True):
                    st.caption("Scoring under **Form MSE II (New Units)** - All 9 Regulatory Parameters Evaluated")
                    m_col1, m_col2, m_col3 = st.columns(3)
                    msme_data["projected_sales_growth"] = m_col1.number_input("1. Projected 3-Yr Sales Growth (%)", value=float(st.session_state.ocr_data.get('projected_sales_growth', 16.0)), step=1.0)
                    msme_data["projected_pat_margin"] = m_col2.number_input("2. Projected PAT Margin (%)", value=float(st.session_state.ocr_data.get('projected_pat_margin', 12.0)), step=0.5)
                    msme_data["projected_der"] = m_col3.number_input("3. Projected Debt-Equity Ratio", value=float(st.session_state.ocr_data.get('projected_der', 1.8)), step=0.1)
                    
                    m_col4, m_col5, m_col6 = st.columns(3)
                    msme_data["inputs_access"] = m_col4.selectbox("4. Access to Raw Materials & Inputs", ["Locally Available / Tied up", "Source Identified", "Not Identified"])
                    msme_data["market_access"] = m_col5.selectbox("5. Access to Market / Off-take", ["Locally Available / Tied up", "Market Identified", "Unidentified"])
                    msme_data["promoter_experience"] = m_col6.selectbox("6. Promoter Qualification & Exp", ["Qualified and Experienced", "Qualified / Trained", "No qualification/experience"])
                    
                    m_col7, m_col8, m_col9 = st.columns(3)
                    msme_data["bank_relationship"] = m_col7.selectbox("7. Relationship with Bank", ["Existing Customer", "Introduced by Govt Dept / Others"])
                    msme_data["premises_type"] = m_col8.selectbox("8. Factory / Operating Premises", ["Owned", "Leased / Rented"])
                    msme_data["collateral_coverage"] = m_col9.selectbox("9. Collateral & CGTMSE Coverage", ["Covered under CGTMSE Scheme", "Over 100% Tangible Collateral", "Up to 50% Collateral", "Below 50% Collateral", "Unsecured"])
            else:
                with st.expander("🏢 Central Bank of India MSME Scoring Parameters (Form MSE 1 - Existing Units)", expanded=True):
                    st.caption("Scoring under **Form MSE 1 (Existing Units)** - All 13 Regulatory Parameters Evaluated")
                    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                    msme_data["current_ratio"] = m_col1.number_input("2. Current Ratio (CR)", value=float(st.session_state.ocr_data.get('current_ratio', 1.35)), step=0.05)
                    msme_data["debt_equity_ratio"] = m_col2.number_input("3. Debt-Equity Ratio (DER)", value=float(st.session_state.ocr_data.get('debt_equity_ratio', 1.9)), step=0.1)
                    msme_data["sales_growth_rate"] = m_col3.number_input("4. 3-Yr Net Sales Growth (%)", value=float(st.session_state.ocr_data.get('sales_growth_rate', 18.0)), step=1.0)
                    msme_data["pat_margin"] = m_col4.number_input("5. PAT Margin (%)", value=float(st.session_state.ocr_data.get('pat_margin', 11.0)), step=0.5)
                    
                    m_col5, m_col6, m_col7 = st.columns(3)
                    s_default = st.session_state.ocr_data.get('sanction_compliance', 'Compliant')
                    s_opts = ["Compliant", "Non-Compliant"]
                    s_idx = s_opts.index(s_default) if s_default in s_opts else 0
                    msme_data["sanction_compliance"] = m_col5.selectbox("1. Sanction Terms Compliance", s_opts, index=s_idx)

                    stk_default = st.session_state.ocr_data.get('stock_statement_status', 'Timely')
                    stk_opts = ["Timely", "Delayed", "Non-Submission"]
                    stk_idx = stk_opts.index(stk_default) if stk_default in stk_opts else 0
                    msme_data["stock_statement_status"] = m_col6.selectbox("6. Stock Statement / QIS Submission", stk_opts, index=stk_idx)

                    debt_default = st.session_state.ocr_data.get('debt_servicing_history', 'Within 1 month')
                    debt_opts = ["Within 1 month", "Within 2 months", "Within 3 months", "Overdue > 3 months"]
                    debt_idx = debt_opts.index(debt_default) if debt_default in debt_opts else 0
                    msme_data["debt_servicing_history"] = m_col7.selectbox("7. Debt Servicing Track Record", debt_opts, index=debt_idx)
                    
                    m_col8, m_col9, m_col10 = st.columns(3)
                    inv_default = st.session_state.ocr_data.get('inventory_compliance', 'Fair compliance')
                    inv_opts = ["Fair Compliance", "Compliance (15%-30% dev)"]
                    inv_idx = 0 if "fair" in str(inv_default).lower() else 1
                    msme_data["inventory_compliance"] = m_col8.selectbox("8. Inventory Norms Compliance", inv_opts, index=inv_idx)

                    bills_default = st.session_state.ocr_data.get('bills_culture', True)
                    bills_idx = 0 if bills_default else 1
                    msme_data["bills_culture"] = m_col9.selectbox("9. Compliance to Bills Culture", ["Compliant", "Non-Compliant"], index=bills_idx) == "Compliant"

                    bpay_default = st.session_state.ocr_data.get('bill_payment_record', 'Prompt')
                    bpay_opts = ["Prompt", "Delayed", "Overdue > 3 months"]
                    bpay_idx = bpay_opts.index(bpay_default) if bpay_default in bpay_opts else 0
                    msme_data["bill_payment_record"] = m_col10.selectbox("10. Trade Bills Payment Track", bpay_opts, index=bpay_idx)
                    
                    m_col11, m_col12, m_col13 = st.columns(3)
                    rev_default = st.session_state.ocr_data.get('review_documents_timely', True)
                    rev_idx = 0 if rev_default else 1
                    msme_data["review_documents_timely"] = m_col11.selectbox("11. Review Documents Submission", ["Timely (< 3 mos)", "Delayed"], index=rev_idx) == "Timely (< 3 mos)"

                    lc_default = st.session_state.ocr_data.get('lc_bg_status', 'Prompt / No Facility')
                    lc_opts = ["Prompt / No Facility", "Devolvement / Invocation"]
                    lc_idx = lc_opts.index(lc_default) if lc_default in lc_opts else 0
                    msme_data["lc_bg_status"] = m_col12.selectbox("12. LC / BG Commitments", lc_opts, index=lc_idx)

                    anc_default = st.session_state.ocr_data.get('ancillary_relationship', 'Substantial')
                    anc_opts = ["Substantial", "Moderate"]
                    anc_idx = anc_opts.index(anc_default) if anc_default in anc_opts else 0
                    msme_data["ancillary_relationship"] = m_col13.selectbox("13. Ancillary Deposits & Association", anc_opts, index=anc_idx)
                    
                    collat_default = st.session_state.ocr_data.get('collateral_coverage', 'Covered under CGTMSE Scheme')
                    collat_opts = ["Covered under CGTMSE Scheme", "Over 100% Tangible Collateral", "Up to 50% Collateral", "Below 50% Collateral", "Unsecured"]
                    collat_idx = collat_opts.index(collat_default) if collat_default in collat_opts else 0
                    msme_data["collateral_coverage"] = st.selectbox("Collateral / Primary Security Backing", collat_opts, index=collat_idx)

        submitted = st.button("🚀 Submit Application for Automated Appraisal", type="primary", use_container_width=True)
        
        if submitted:
            payload = {
                "name": name, "age": age, "gender": gender, "marital_status": marital_status,
                "category": category, "occupation": occupation, "gross_monthly_income": gross_income,
                "net_monthly_income": net_income, "total_assets": total_assets, 
                "avg_credit_balance_6m": avg_credit_balance_6m, "existing_emi": existing_emi,
                "active_lines": active_lines, "inquiries_6m": inquiries_6m, "credit_score": credit_score,
                "loan_amount": loan_amount, "interest_rate": 0.0, "tenure_months": tenure_months,
                "loan_type": loan_type, "property_value": property_value, "security_type": security_type,
                **msme_data
            }
            
            with st.spinner("Submitting Application to Agentic Pipeline..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/apply", json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.thread_id = result.get("thread_id")
                        st.session_state.polling = True
                        st.success(f"Application Submitted in 1-Click! Tracking ID: {st.session_state.thread_id}")
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
    
        # Polling Loop for Async Processing
        if st.session_state.get("polling") and st.session_state.get("thread_id"):
            status_placeholder = st.empty()
            with status_placeholder.container():
                st.info("Tracking application progress in real-time...")
                try:
                    res = requests.get(f"{API_BASE_URL}/status/{st.session_state.thread_id}").json()
                    status = res.get("status")
                    
                    if status == "PROCESSING" or status == "INITIALIZING":
                        logs = res.get("agent_logs", [])
                        st.write(f"Agents completed: {len(logs)} / 10")
                        st.progress(min(len(logs) * 10, 100))
                        for log in logs[-3:]:
                            st.write(f"✅ {log['agent']}: {log['summary']}")
                        time.sleep(2)
                        st.rerun()
                    elif status == "WAITING_FOR_MANAGER":
                        st.session_state.polling = False
                        st.session_state.latest_result = res
                        st.success("Verification Complete! Awaiting Manager Approval.")
                        st.info("Log in as Credit Manager to review.")
                    elif status == "COMPLETED":
                        st.session_state.polling = False
                        st.session_state.latest_result = res
                        st.success("Decision Finalized.")
                except Exception as e:
                    st.error(f"Failed to fetch status: {e}")
                    time.sleep(2)
                    st.rerun()
        with tab_track:
            st.header("Track Your Application")
            st.markdown("Enter your Tracking ID to view real-time status or download your final report.")
            track_id = st.text_input("Application Tracking ID")
            if st.button("Check Status"):
                if track_id:
                    try:
                        res = requests.get(f"{API_BASE_URL}/status/{track_id}").json()
                        status = res.get("status")
                        if status == "INITIALIZING":
                            st.info("Application is initializing or not found.")
                        elif status in ["PROCESSING", "WAITING_FOR_MANAGER"]:
                            st.warning("Application is still under review.")
                        elif status == "COMPLETED":
                            st.success(f"Final Decision: {res.get('decision_outcome')}")
                            st.subheader("Credit Appraisal One-Pager")
                            st.markdown(res.get("short_report", ""), unsafe_allow_html=True)
                            docx_bytes = utils.generate_docx(res.get("short_report", ""))
                            st.download_button("📄 Download Final Report (Docx)", docx_bytes, "Applicant_Report.docx")
                    except Exception as e:
                        st.error("Invalid ID or failed to fetch status.")
                else:
                    st.error("Please enter a Tracking ID.")

# =============================================================================
# TOP-LEVEL TAB: CORPORATE FINANCIAL INTELLIGENCE & VALUATION HUB
# =============================================================================
if tab_corp:
    with tab_corp:
        st.header("🏢 Corporate Financial Intelligence & Valuation Hub")
        st.caption("Autonomous Multi-Year CMA Spreading, 5-Pillar Diagnostics, Forensic Accounting (Altman Z'' & Beneish M-Score), Macro Stress Simulator & DCF Valuation")

        col_sel1, col_sel2 = st.columns([3, 2])
    with col_sel1:
        corp_choice = st.selectbox(
            "Select Corporate Profile or Upload Financials:",
            [
                "Apex Precision Engineering Pvt Ltd (Prime MSME Manufacturing - CBI 1)",
                "Surat Silk Mills Pvt Ltd (Moderate Textile Manufacturing - CBI 5)",
                "BioGreen Agro Processors LLP (Greenfield Food Processing - CBI 2)",
                "Defaulter Steels LLP (Distressed Steel Entity - CBI 10)",
                "📁 Upload Custom Balance Sheet / P&L (CSV or JSON)"
            ],
            key="corp_profile_selector"
        )
    with col_sel2:
        proposed_corp_loan = st.number_input("Proposed Credit Facility (₹):", min_value=100000.0, max_value=500000000.0, value=5000000.0, step=500000.0)

    # Ingestion Resolution
    raw_corp_data = None
    if "Apex Precision" in corp_choice:
        raw_corp_data = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]
    elif "Surat Silk" in corp_choice:
        raw_corp_data = CORPORATE_PROFILES["Surat Silk Mills Pvt Ltd"]
    elif "BioGreen" in corp_choice:
        raw_corp_data = CORPORATE_PROFILES["BioGreen Agro Processors LLP"]
    elif "Defaulter Steels" in corp_choice:
        raw_corp_data = CORPORATE_PROFILES["Defaulter Steels LLP"]
    else:
        uploaded_file = st.file_uploader("Upload Audited Financials (.csv or .json):", type=["csv", "json"])
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith(".csv"):
                    raw_corp_data = FinancialDocumentParser.parse_csv_file(uploaded_file.getvalue())
                else:
                    raw_corp_data = FinancialDocumentParser.parse_json_or_dict(uploaded_file.getvalue())
                st.success("Custom financial statements parsed successfully!")
            except Exception as e:
                st.error(f"Error parsing uploaded file: {e}")
                raw_corp_data = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]
        else:
            st.info("Upload a financial file or select a benchmark corporate profile from above.")
            raw_corp_data = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]

    raw_corp_data["requested_loan_amount"] = proposed_corp_loan

    # --- EXECUTE CORE FINANCIAL INTELLIGENCE MATH ---
    spread = FinancialStatementSpreader.spread_financials(raw_corp_data)
    ratios = RatioDiagnosticsEngine.calculate_ratios(spread)
    altman_z = ForensicAuditor.calculate_altman_z_double_prime(spread)
    beneish_m = ForensicAuditor.calculate_beneish_m_score(spread)
    projections = FinancialForecaster.project_3_years(spread, sales_cagr=0.15)
    dcf = EnterpriseValuator.calculate_dcf_valuation(spread, proposed_loan_amount=proposed_corp_loan)
    flags = raw_corp_data.get("operational_flags", {})
    mse_scorecard = MSEParameterAutoMapper.auto_score_form_mse_1(spread, flags)
    
    credit_score = int(raw_corp_data.get("credit_score", 750))
    is_cgtmse = raw_corp_data.get("cgtmse_covered", True)
    official_roi = get_applicable_roi("MSME Loan - Existing Unit", credit_score, mse_grade=mse_scorecard["grade"], cgtmse_covered=is_cgtmse)

    # --- TOP EXECUTIVE KPI BANNER ---
    latest_rev = spread["pnl"]["revenue"][-1]
    latest_pat = spread["pnl"]["pat"][-1]
    latest_tnw = spread["balance_sheet"]["tangible_net_worth"][-1]
    
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Audited Revenue (FY26)", f"₹{latest_rev/1e7:.2f} Cr", help="Latest annual turnover")
    k2.metric("Tangible Net Worth", f"₹{latest_tnw/1e7:.2f} Cr", help="Net Worth = Equity + Reserves")
    k3.metric("PAT Margin", f"{ratios['profitability']['pat_margin_pct'][-1]:.1f}%", help="Net profit margin")
    k4.metric("Altman Z''-Score", f"{altman_z['z_score']:.2f}", delta=altman_z['zone'], delta_color="normal" if "Safe" in altman_z['zone'] else "inverse")
    k5.metric("Enterprise Value", f"₹{dcf['enterprise_value']/1e7:.2f} Cr", help="Discounted Cash Flow intrinsic value")
    k6.metric("Auto-Scored Risk Grade", f"{mse_scorecard['grade']}", delta=f"{mse_scorecard['total_score']}/100 Marks")

    st.markdown("---")

    # --- 6 INTERACTIVE SUB-TABS ---
    c_tab1, c_tab2, c_tab3, c_tab4, c_tab5, c_tab6 = st.tabs([
        "📁 3-Year Audited Financials (CMA)",
        "📊 5-Pillar Ratio Diagnostics & MPBF",
        "🔍 Forensic Early Warning Audit",
        "🧪 3-Year Forecasting & Stress Simulator",
        "💎 DCF Valuation & Debt Sizing",
        "🏛️ Auto-Populated Form MSE 1 Scorecard"
    ])

    # 1. 3-YEAR AUDITED FINANCIALS
    with c_tab1:
        st.subheader("📑 3-Year Credit Monitoring Arrangement (CMA) Financial Spreading")
        years = spread["years"]
        
        col_pnl, col_bs = st.columns(2)
        with col_pnl:
            st.markdown("##### 📈 Profit & Loss Statement (₹ Lakhs)")
            pnl_df = pd.DataFrame({
                "Line Item": ["Gross Turnover / Sales", "Cost of Goods Sold (COGS)", "Gross Profit", "Operating Expenses (Opex)", "EBITDA (Operating Profit)", "Depreciation & Amortization", "EBIT (Operating Income)", "Interest / Finance Charges", "Profit After Tax (PAT)", "Cash Accruals (PAT + Dep)"],
                years[0]: [spread["pnl"]["revenue"][0]/1e5, spread["pnl"]["cogs"][0]/1e5, spread["pnl"]["gross_profit"][0]/1e5, spread["pnl"]["operating_expenses"][0]/1e5, spread["pnl"]["ebitda"][0]/1e5, spread["pnl"]["depreciation"][0]/1e5, spread["pnl"]["ebit"][0]/1e5, spread["pnl"]["interest_expense"][0]/1e5, spread["pnl"]["pat"][0]/1e5, spread["pnl"]["cash_accruals"][0]/1e5],
                years[1]: [spread["pnl"]["revenue"][1]/1e5, spread["pnl"]["cogs"][1]/1e5, spread["pnl"]["gross_profit"][1]/1e5, spread["pnl"]["operating_expenses"][1]/1e5, spread["pnl"]["ebitda"][1]/1e5, spread["pnl"]["depreciation"][1]/1e5, spread["pnl"]["ebit"][1]/1e5, spread["pnl"]["interest_expense"][1]/1e5, spread["pnl"]["pat"][1]/1e5, spread["pnl"]["cash_accruals"][1]/1e5],
                years[2]: [spread["pnl"]["revenue"][2]/1e5, spread["pnl"]["cogs"][2]/1e5, spread["pnl"]["gross_profit"][2]/1e5, spread["pnl"]["operating_expenses"][2]/1e5, spread["pnl"]["ebitda"][2]/1e5, spread["pnl"]["depreciation"][2]/1e5, spread["pnl"]["ebit"][2]/1e5, spread["pnl"]["interest_expense"][2]/1e5, spread["pnl"]["pat"][2]/1e5, spread["pnl"]["cash_accruals"][2]/1e5]
            })
            st.dataframe(pnl_df.style.format({years[0]: "{:,.2f}", years[1]: "{:,.2f}", years[2]: "{:,.2f}"}), use_container_width=True, hide_index=True)

        with col_bs:
            st.markdown("##### 🏛️ Balance Sheet (₹ Lakhs)")
            bs_df = pd.DataFrame({
                "Line Item": ["Cash & Bank Balances", "Sundry Debtors (Receivables)", "Inventory (Raw, WIP, FG)", "Total Current Assets", "Net Fixed Assets (PPE)", "Total Assets", "Sundry Creditors (Payables)", "Short-Term Bank Borrowings", "Total Current Liabilities", "Long-Term Term Debt", "Tangible Net Worth (TNW)"],
                years[0]: [spread["balance_sheet"]["cash_and_bank"][0]/1e5, spread["balance_sheet"]["sundry_debtors"][0]/1e5, spread["balance_sheet"]["inventory"][0]/1e5, spread["balance_sheet"]["current_assets"][0]/1e5, spread["balance_sheet"]["net_fixed_assets"][0]/1e5, spread["balance_sheet"]["total_assets"][0]/1e5, spread["balance_sheet"]["sundry_creditors"][0]/1e5, spread["balance_sheet"]["short_term_borrowings"][0]/1e5, spread["balance_sheet"]["current_liabilities"][0]/1e5, spread["balance_sheet"]["long_term_debt"][0]/1e5, spread["balance_sheet"]["tangible_net_worth"][0]/1e5],
                years[1]: [spread["balance_sheet"]["cash_and_bank"][1]/1e5, spread["balance_sheet"]["sundry_debtors"][1]/1e5, spread["balance_sheet"]["inventory"][1]/1e5, spread["balance_sheet"]["current_assets"][1]/1e5, spread["balance_sheet"]["net_fixed_assets"][1]/1e5, spread["balance_sheet"]["total_assets"][1]/1e5, spread["balance_sheet"]["sundry_creditors"][1]/1e5, spread["balance_sheet"]["short_term_borrowings"][1]/1e5, spread["balance_sheet"]["current_liabilities"][1]/1e5, spread["balance_sheet"]["long_term_debt"][1]/1e5, spread["balance_sheet"]["tangible_net_worth"][1]/1e5],
                years[2]: [spread["balance_sheet"]["cash_and_bank"][2]/1e5, spread["balance_sheet"]["sundry_debtors"][2]/1e5, spread["balance_sheet"]["inventory"][2]/1e5, spread["balance_sheet"]["current_assets"][2]/1e5, spread["balance_sheet"]["net_fixed_assets"][2]/1e5, spread["balance_sheet"]["total_assets"][2]/1e5, spread["balance_sheet"]["sundry_creditors"][2]/1e5, spread["balance_sheet"]["short_term_borrowings"][2]/1e5, spread["balance_sheet"]["current_liabilities"][2]/1e5, spread["balance_sheet"]["long_term_debt"][2]/1e5, spread["balance_sheet"]["tangible_net_worth"][2]/1e5]
            })
            st.dataframe(bs_df.style.format({years[0]: "{:,.2f}", years[1]: "{:,.2f}", years[2]: "{:,.2f}"}), use_container_width=True, hide_index=True)

        # Plotly Historical Performance Trend
        trend_df = pd.DataFrame({
            "Financial Year": years,
            "Turnover (₹ Cr)": [r / 1e7 for r in spread["pnl"]["revenue"]],
            "EBITDA (₹ Cr)": [e / 1e7 for e in spread["pnl"]["ebitda"]],
            "PAT (₹ Cr)": [p / 1e7 for p in spread["pnl"]["pat"]]
        })
        fig_trend = px.bar(trend_df, x="Financial Year", y=["Turnover (₹ Cr)", "EBITDA (₹ Cr)", "PAT (₹ Cr)"], barmode="group", title="3-Year Financial Trajectory (Turnover vs EBITDA vs PAT)")
        fig_trend.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_trend, use_container_width=True)

    # 2. 5-PILLAR RATIOS & MPBF
    with c_tab2:
        st.subheader("📊 5-Pillar Institutional Ratio Diagnostics")
        
        r_col1, r_col2, r_col3, r_col4 = st.columns(4)
        r_col1.metric("Current Ratio", f"{ratios['liquidity']['current_ratio'][-1]:.2f}", help="Standard Benchmark >= 1.33")
        r_col2.metric("Debt-Equity (DER)", f"{ratios['solvency']['debt_to_equity'][-1]:.2f}", help="Prudent Cap <= 2.00")
        r_col3.metric("DSCR Coverage", f"{ratios['solvency']['debt_service_coverage_ratio'][-1]:.2f}x", help="Minimum Bank Hurdle >= 1.20x")
        r_col4.metric("Cash Conversion Cycle", f"{ratios['efficiency']['cash_conversion_cycle_days'][-1]:.0f} Days", help="Debtor Days + Inventory Days - Creditor Days")

        st.markdown("---")
        
        # Working Capital Sizing Table
        st.markdown("##### 💼 Working Capital Sizing (Tandon & Nayak Committee MPBF)")
        mpbf = ratios["mpbf_working_capital"]
        mpbf_df = pd.DataFrame({
            "Regulatory Assessment Model": [
                "Tandon Committee Method I (75% of Working Capital Gap)",
                "Tandon Committee Method II (75% Current Assets - Other CL)",
                "Nayak Committee Model (20% of Projected Turnover for MSEs)",
                "🏦 Recommended Maximum Bank Working Capital Limit"
            ],
            "Assessed Limit (₹ Lakhs)": [
                f"₹{mpbf['tandon_method_1']/1e5:,.2f}",
                f"₹{mpbf['tandon_method_2']/1e5:,.2f}",
                f"₹{mpbf['nayak_turnover_method']/1e5:,.2f}",
                f"₹{mpbf['recommended_limit']/1e5:,.2f}"
            ],
            "Compliance Rule / Banking Norm": [
                "Borrower finances min 25% of Working Capital Gap from Long-term Net Working Capital",
                "Borrower finances min 25% of Total Current Assets from Long-term Net Working Capital",
                "Mandatory formula for MSE borrowers with credit facilities up to ₹5 Crores",
                "Sanctionable working capital limit within statutory solvency ceiling"
            ]
        })
        st.dataframe(mpbf_df, use_container_width=True, hide_index=True)

    # 3. FORENSIC AUDIT (ALTMAN Z & BENEISH M)
    with c_tab3:
        st.subheader("🔍 Forensic Accounting & Distress Early Warning Models")
        
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown("##### ⚠️ Altman Z''-Score (Bankruptcy & Default Risk)")
            
            fig_z = go.Figure(go.Indicator(
                mode="gauge+number",
                value=altman_z["z_score"],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': f"Altman Z''-Score: {altman_z['zone']}"},
                gauge={
                    'axis': {'range': [0, 5]},
                    'bar': {'color': altman_z["badge_color"]},
                    'steps': [
                        {'range': [0, 1.10], 'color': '#FCA5A5'},   # Red Distress
                        {'range': [1.10, 2.60], 'color': '#FDE68A'}, # Amber Grey
                        {'range': [2.60, 5.0], 'color': '#A7F3D0'}   # Green Safe
                    ],
                    'threshold': {
                        'line': {'color': "black", 'width': 3},
                        'thickness': 0.75,
                        'value': 2.60
                    }
                }
            ))
            fig_z.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_z, use_container_width=True)
            st.caption(f"**Diagnostic Status:** {altman_z['risk_level']}")

        with f_col2:
            st.markdown("##### 🕵️ Beneish M-Score (Earnings Manipulation Detection)")
            st.markdown(f"**M-Score:** `{beneish_m['m_score']}` *(Threshold: `-1.78`)*")
            if beneish_m["manipulation_flag"]:
                st.error(f"🚨 **Alert:** {beneish_m['risk_assessment']}")
            else:
                st.success(f"✅ **Clean Audit:** {beneish_m['risk_assessment']}")

            # Indices table
            m_df = pd.DataFrame([
                {"Forensic Index": "DSRI (Days Sales in Receivables)", "Value": beneish_m["indices"]["DSRI_receivables_growth"], "Benchmark": "< 1.20", "Status": "Normal" if beneish_m["indices"]["DSRI_receivables_growth"] < 1.20 else "High"},
                {"Forensic Index": "GMI (Gross Margin Index)", "Value": beneish_m["indices"]["GMI_margin_deterioration"], "Benchmark": "< 1.10", "Status": "Normal" if beneish_m["indices"]["GMI_margin_deterioration"] < 1.10 else "High"},
                {"Forensic Index": "AQI (Asset Quality Index)", "Value": beneish_m["indices"]["AQI_asset_quality"], "Benchmark": "< 1.20", "Status": "Normal" if beneish_m["indices"]["AQI_asset_quality"] < 1.20 else "High"},
                {"Forensic Index": "SGI (Sales Growth Index)", "Value": beneish_m["indices"]["SGI_sales_growth"], "Benchmark": "< 1.30", "Status": "Normal" if beneish_m["indices"]["SGI_sales_growth"] < 1.30 else "High"},
                {"Forensic Index": "TATA (Total Accruals to Assets)", "Value": beneish_m["indices"]["TATA_accruals_to_assets"], "Benchmark": "< 0.05", "Status": "Normal" if beneish_m["indices"]["TATA_accruals_to_assets"] < 0.05 else "High"}
            ])
            st.dataframe(m_df, use_container_width=True, hide_index=True)

    # 4. 3-YEAR FORECASTING & STRESS SIMULATOR
    with c_tab4:
        st.subheader("🧪 3-Year Financial Forecasting & Macro Stress Testing Simulator")
        st.caption("Simulate real-time economic shocks on the borrower's audited balance sheet to test DSCR solvency buffers:")

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            rev_shock = st.slider("📉 Demand Shock (Revenue Decline %):", min_value=-40, max_value=20, value=0, step=5)
        with col_s2:
            cost_shock = st.slider("📈 Cost Inflation (COGS Increase %):", min_value=0, max_value=30, value=0, step=5)
        with col_s3:
            rate_shock = st.slider("🏦 Interest Rate Hike (+bps on RBLR):", min_value=0, max_value=400, value=0, step=50)

        stress_res = FinancialForecaster.simulate_stress_scenario(
            spread,
            revenue_shock_pct=rev_shock / 100.0,
            cogs_increase_pct=cost_shock / 100.0,
            interest_rate_shock_bps=rate_shock
        )

        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Stressed Turnover", f"₹{stress_res['stressed_revenue']/1e7:.2f} Cr", delta=f"{rev_shock}%")
        sc2.metric("Stressed EBITDA", f"₹{stress_res['stressed_ebitda']/1e5:.2f} L")
        sc3.metric("Stressed DSCR", f"{stress_res['stressed_dscr']:.2f}x", delta=">= 1.20x Solvency", delta_color="normal" if stress_res["stressed_dscr"] >= 1.20 else "inverse")
        sc4.metric("Stressed ICR", f"{stress_res['stressed_icr']:.2f}x", delta=">= 1.50x Interest", delta_color="normal" if stress_res["stressed_icr"] >= 1.50 else "inverse")

        if stress_res["is_solvent"]:
            st.success(f"🛡️ **Solvency Assessment:** {stress_res['solvency_status']}")
        else:
            st.error(f"🚨 **Solvency Warning:** {stress_res['solvency_status']}")

        # 3-Year Forward Projections Table
        st.markdown("##### 🔮 3-Year Baseline Projections (15% Organic Growth)")
        proj_df = pd.DataFrame({
            "Metric": ["Projected Turnover (₹ Lakhs)", "Projected EBITDA (₹ Lakhs)", "Projected Net Profit / PAT (₹ Lakhs)", "Projected DSCR"],
            projections["projection_years"][0]: [f"₹{projections['projected_revenue'][0]/1e5:,.2f}", f"₹{projections['projected_ebitda'][0]/1e5:,.2f}", f"₹{projections['projected_pat'][0]/1e5:,.2f}", f"{projections['projected_dscr'][0]:.2f}x"],
            projections["projection_years"][1]: [f"₹{projections['projected_revenue'][1]/1e5:,.2f}", f"₹{projections['projected_ebitda'][1]/1e5:,.2f}", f"₹{projections['projected_pat'][1]/1e5:,.2f}", f"{projections['projected_dscr'][1]:.2f}x"],
            projections["projection_years"][2]: [f"₹{projections['projected_revenue'][2]/1e5:,.2f}", f"₹{projections['projected_ebitda'][2]/1e5:,.2f}", f"₹{projections['projected_pat'][2]/1e5:,.2f}", f"{projections['projected_dscr'][2]:.2f}x"]
        })
        st.dataframe(proj_df, use_container_width=True, hide_index=True)

    # 5. DCF VALUATION & DEBT SIZING
    with c_tab5:
        st.subheader("💎 Discounted Cash Flow (DCF) Enterprise Valuation & Debt Sizing")
        
        v_col1, v_col2, v_col3 = st.columns(3)
        v_col1.metric("Implied Enterprise Value (EV)", f"₹{dcf['enterprise_value']/1e7:.2f} Cr", help="Intrinsic Enterprise Value based on FCFF DCF model")
        v_col2.metric("Implied Equity Value", f"₹{dcf['equity_value']/1e7:.2f} Cr", help="Equity Value = Enterprise Value - Net Debt")
        v_col3.metric("Loan-to-Enterprise Value (LTV on EV)", f"{dcf['loan_to_enterprise_value_pct']:.1f}%", delta="Prudent < 35%", delta_color="normal" if dcf["loan_to_enterprise_value_pct"] <= 35.0 else "inverse")

        st.info(f"📊 **Leverage Assessment:** {dcf['leverage_assessment']} | **Assumed WACC:** `{dcf['wacc_pct']}%` | **Terminal Growth:** `{dcf['terminal_growth_pct']}%`")

        # 5-Year FCFF Cash Flow Waterfall
        fcff_df = pd.DataFrame({
            "Projection Year": [f"Year {t}" for t in range(1, 6)],
            "Projected FCFF (₹ Lakhs)": [f / 1e5 for f in dcf["fcff_projections"]]
        })
        fig_fcff = px.bar(fcff_df, x="Projection Year", y="Projected FCFF (₹ Lakhs)", text="Projected FCFF (₹ Lakhs)", title="5-Year Free Cash Flow to Firm (FCFF) Waterfall")
        fig_fcff.update_traces(marker_color="#3B82F6", texttemplate='%{text:.1f} L', textposition='outside')
        fig_fcff.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fcff, use_container_width=True)

    # 6. AUTO-POPULATED FORM MSE 1 SCORECARD
    with c_tab6:
        st.subheader("🏛️ Auto-Populated Central Bank Form MSE 1 Scorecard")
        st.markdown(f"**Total Score:** **`{mse_scorecard['total_score']}/100`** | **Central Bank Risk Grade:** **`{mse_scorecard['grade']}`** ({mse_scorecard['risk_profile']})")
        
        if mse_scorecard["hurdle_rate_met"]:
            st.success(f"✅ **HURDLE RATE MET (> 50 Marks)** — Assigned Official RBLR ROI of **`{official_roi:.2f}% p.a.`**")
        else:
            st.error(f"🛑 **SUB-HURDLE RATE BREACH (Score <= 50 Marks)** — Ineligible for Standard Sanction under Central Bank Guidelines.")

        # Full 13-parameter breakdown table
        param_rows = []
        for p in mse_scorecard["parameter_scores"]:
            param_rows.append({
                "Parameter Name": p["param"],
                "Assessed Value / Ratio": p["value"],
                "Score Awarded": p["score"],
                "Max Marks": p["max"]
            })
        st.dataframe(pd.DataFrame(param_rows), use_container_width=True, hide_index=True)

        st.markdown("---")
        if st.button("🚀 Push This Corporate Profile to Loan Application Queue", type="primary", use_container_width=True):
            st.session_state.ocr_data = {
                "name": raw_corp_data["company_name"],
                "age": 45,
                "gender": "Male",
                "marital_status": "Married",
                "category": "GEN",
                "occupation": "Business",
                "gross_monthly_income": int(latest_rev / 12),
                "net_monthly_income": int(latest_pat / 12),
                "total_assets": int(spread["balance_sheet"]["total_assets"][-1]),
                "credit_score": int(credit_score),
                "avg_credit_balance_6m": int(spread["balance_sheet"]["cash_and_bank"][-1]),
                "existing_emi": int(spread["pnl"]["interest_expense"][-1] / 12),
                "active_lines": 3,
                "inquiries_6m": 0,
                "loan_amount": int(proposed_corp_loan),
                "tenure_months": int(raw_corp_data.get("tenure_months", 60)),
                "loan_type": raw_corp_data.get("loan_type", "MSME Loan - Existing Unit"),
                "property_value": int(spread["balance_sheet"]["net_fixed_assets"][-1] * 1.25),
                "security_type": "Property",
                "current_ratio": float(ratios["liquidity"]["current_ratio"][-1]),
                "debt_equity_ratio": float(ratios["solvency"]["debt_to_equity"][-1]),
                "sales_growth_rate": float(ratios["efficiency"]["sales_growth_rate_pct"][-1] if len(ratios["efficiency"]["sales_growth_rate_pct"]) > 1 else 15.0),
                "pat_margin": float(ratios["profitability"]["pat_margin_pct"][-1]),
                "sanction_compliance": flags.get("sanction_compliance", "Compliant"),
                "stock_statement_status": flags.get("stock_statement_status", "Timely"),
                "debt_servicing_history": flags.get("debt_servicing_history", "Within 1 month"),
                "inventory_compliance": flags.get("inventory_compliance", "Fair compliance"),
                "bills_culture": flags.get("bills_culture", True),
                "bill_payment_record": flags.get("bill_payment_record", "Prompt"),
                "review_documents_timely": flags.get("review_documents_timely", True),
                "lc_bg_status": flags.get("lc_bg_status", "Prompt / No Facility"),
                "ancillary_relationship": flags.get("ancillary_relationship", "Substantial"),
                "collateral_coverage": "Covered under CGTMSE Scheme" if is_cgtmse else "Over 100% Tangible Collateral",
                "cgtmse_covered": is_cgtmse
            }
            st.session_state.ocr_done = True
            st.success("✅ Profile pushed to Loan Application Form! Switch to Tab 1 to submit.")
            st.rerun()

if tab2:
    with tab2:
        st.header("Credit Manager Dashboard")
    
        if not (st.session_state.role == "Credit Manager" and st.session_state.logged_in):
            st.error("🚫 Access Denied. Please login as a Credit Manager from the sidebar using your passcode.")
        else:
            manager_tab1, manager_tab2, manager_tab3 = st.tabs([
                "🔴 Active Underwriting Pipeline", 
                "📊 Executive Portfolio Analytics & Risk Intelligence", 
                "📂 Complete Application History & Overrides"
            ])
            
            # =========================================================================
            # MANAGER TAB 1: ACTIVE UNDERWRITING PIPELINE (HITL QUEUE)
            # =========================================================================
            with manager_tab1:
                st.markdown("Human-In-The-Loop (HITL) Review & Automated Assessment")
                
                # --- PENDING APPLICATIONS LIST ---
                try:
                    pending_res = requests.get(f"{API_BASE_URL}/pending").json()
                    if pending_res and len(pending_res) > 0:
                        st.info(f"You have {len(pending_res)} application(s) awaiting your review.")
                        pending_df = pd.DataFrame(pending_res)
                        pending_df['loan_amount'] = pending_df['loan_amount'].apply(lambda x: f"₹{x:,.2f}")
                        st.dataframe(pending_df, use_container_width=True, hide_index=True)
                        
                        selected_pending = st.selectbox("Select Application to Review:", pending_df['thread_id'])
                        if st.button("Load Application"):
                            st.session_state.thread_id = selected_pending
                            # Fetch latest status
                            res = requests.get(f"{API_BASE_URL}/status/{selected_pending}").json()
                            st.session_state.latest_result = res
                            st.rerun()
                    else:
                        st.success("No applications are currently waiting for manager approval.")
                except Exception as e:
                    st.error(f"Failed to fetch pending applications: {e}")
                    
                st.markdown("---")
                
                # --- DISPLAY SELECTED APPLICATION APPRAISAL MEMO ---
                if st.session_state.latest_result:
                    result = st.session_state.latest_result
                    st.header(f"Credit Appraisal Review: {st.session_state.thread_id}")
                    
                    # Top Status Banner
                    st.success(f"**System Recommendation:** {result.get('decision_outcome')} (App ID: {st.session_state.thread_id})")
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.subheader("⚙️ Verification Timeline")
                        agent_logs = result.get("agent_logs", [])
                        for log in agent_logs:
                            st.markdown(f"**{log['agent']}**: ✅ {log['summary']}")
                            
                    with col2:
                        st.subheader("📊 Financial Snapshot")
                        metrics = result.get("financial_metrics", {})
                        msme_sc = metrics.get("msme_scorecard") or result.get("msme_scorecard")
                        
                        if msme_sc:
                            st.metric("Central Bank MSE Score", f"{msme_sc.get('total_score')}/100", delta=f"{msme_sc.get('grade')}")
                            hurdle_txt = "✅ Hurdle Met (> 50)" if msme_sc.get('hurdle_rate_met', True) else "❌ Sub-Hurdle Rate (<= 50)"
                            st.caption(f"**Hurdle Status:** {hurdle_txt} | **Risk Grade:** {msme_sc.get('grade')} ({msme_sc.get('risk_profile')})")
                        
                        if "official_roi" in metrics:
                            st.metric("Bank Assigned ROI", f"{metrics.get('official_roi'):.2f}%")
                            
                        st.metric("Calculated FOIR", f"{metrics.get('calculated_foir', 0):.2f}%")
                        
                        ltv = metrics.get('ltv_compliance', {})
                        st.metric("LTV Ratio", f"{ltv.get('ltv', 0):.2f}%", 
                                  delta="Compliant" if ltv.get('compliant') else "Violation",
                                  delta_color="normal" if ltv.get('compliant') else "inverse")
                        
                    st.markdown("---")
                    
                    # --- MIDDLE SECTION: ML Risk ---
                    st.subheader("🧠 Predictive Risk Assessment")
                    risk = result.get("risk_score", {})
                    try:
                        pd_val = float(risk.get('pd_percentage', 0.0))
                    except (ValueError, TypeError):
                        pd_val = 0.0
                    
                    st.markdown(f"**Probability of Default (PD):** `{pd_val:.2f}%`")
                    
                    # Visual Progress bar for 5-Tier PD Distribution
                    if pd_val < 15.0:
                        bar_color = "#2e7d32" # Very Low (Dark Green)
                    elif pd_val < 25.0:
                        bar_color = "#4caf50" # Low (Green)
                    elif pd_val < 40.0:
                        bar_color = "#ff9800" # Moderate (Amber)
                    elif pd_val < 55.0:
                        bar_color = "#f4511e" # Elevated (Deep Orange)
                    else:
                        bar_color = "#d32f2f" # High / Critical Default (Red)

                    st.markdown(f'''
                        <div style="background-color: #f0f2f6; border-radius: 5px; width: 100%; height: 25px;">
                            <div style="background-color: {bar_color}; width: {min(pd_val, 100.0)}%; height: 100%; border-radius: 5px;"></div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    st.caption(f"Risk Category: **{risk.get('risk_category', 'Unknown')}** | Explanation: {risk.get('explanation', '')}")
                    
                    # --- CRITICAL RISK DRIVERS ---
                    st.markdown("##### 🔍 Key Risk Drivers (Top 3 Impacting Factors):")
                    drivers = risk.get('drivers', [])
                    if drivers:
                        for d in drivers:
                            feat_name = d.get('feature', 'Unknown')
                            shap_val = d.get('shap_value', 0.0)
                            val = d.get('value', 0.0)
                            
                            if shap_val > 0:
                                st.markdown(f"- 🔴 **{feat_name}** (`{val}`): Contributed positively to default risk.")
                            else:
                                st.markdown(f"- 🟢 **{feat_name}** (`{val}`): Reduced default risk.")
                    else:
                        st.write("No strong risk drivers identified.")
                        
                    st.markdown("---")
                    
                    # --- POLICY ADHERENCE ---
                    st.subheader("📜 Regulatory & Underwriting Policy Adherence")
                    policies = result.get("applicable_policies", [])
                    if policies:
                        app_cibil = metrics.get('credit_score', 0)
                        if app_cibil >= 750:
                            st.markdown(f"- 🟢 **Credit Bureau Standing**: Applicant holds a **Prime CIBIL Score of `{app_cibil}`**, qualifying for prime pricing under Central Bank of India RBLR lending framework.")
                        elif app_cibil >= 700:
                            st.markdown(f"- 🟡 **Credit Bureau Standing**: Applicant holds a **Standard CIBIL Score of `{app_cibil}`**, within acceptable lending parameters.")
                        else:
                            st.markdown(f"- 🔴 **Credit Bureau Standing**: Applicant holds a **Sub-Prime CIBIL Score of `{app_cibil}`**, representing elevated credit default risk.")
                            
                        app_foir = metrics.get('calculated_foir', 0)
                        if app_foir <= 50:
                            st.markdown(f"- 🟢 **Debt Serviceability (FOIR)**: Current FOIR is **`{app_foir:.1f}%`**, well below the bank's maximum allowable cap of 50.0%.")
                        else:
                            st.markdown(f"- 🔴 **Debt Serviceability (FOIR)**: Current FOIR is **`{app_foir:.1f}%`**, exceeding the standard prudential threshold of 50.0%.")
                            
                        ltv_comp = metrics.get('ltv_compliance', {})
                        if not ltv_comp.get('compliant'):
                            st.markdown(f"- 🛑 **Collateral Adequacy (LTV)**: The requested loan amount exceeds the maximum permissible Loan-to-Value limits for this property class (Currently `{ltv_comp.get('ltv', 0):.1f}%`).")
                        else:
                            st.markdown(f"- 🏦 **Collateral Adequacy (LTV)**: The requested loan is well within the acceptable Loan-to-Value regulatory limits (`{ltv_comp.get('ltv', 0):.1f}%`).")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        with st.expander("🔍 View Referenced Regulatory Clauses"):
                            for pol in policies:
                                clean_pol = re.sub(r'【.*?】|\[.*?\]', '', pol)
                                clean_pol = re.sub(r'\s+', ' ', clean_pol).strip()
                                st.info(f"> {clean_pol}")
                    else:
                        st.write("Awaiting system processing.")
                        
                    st.markdown("---")
                    
                    # --- PUBLISHABLE REPORTS ---
                    st.subheader("📑 Formal Appraisal Reports")
                    
                    detailed_report = result.get("detailed_report", "")
                    short_report = result.get("short_report", "")
                    
                    if short_report or detailed_report:
                        report_tab1, report_tab2 = st.tabs(["Short Report (One-Pager)", "Detailed Report (Memo)"])
                        
                        with report_tab1:
                            st.markdown(short_report, unsafe_allow_html=True)
                            if short_report:
                                docx_bytes = utils.generate_docx(short_report)
                                st.download_button(
                                    label="📄 Download Short Report (Docx)",
                                    data=docx_bytes,
                                    file_name="Short_Appraisal_Report.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                        with report_tab2:
                            st.markdown(detailed_report, unsafe_allow_html=True)
                            if detailed_report:
                                docx_bytes = utils.generate_docx(detailed_report)
                                st.download_button(
                                    label="📄 Download Detailed Memo (Docx)",
                                    data=docx_bytes,
                                    file_name="Detailed_Appraisal_Memo.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                    
                    st.markdown("---")
                    
                    # --- APPROVAL BUTTONS ---
                    if result.get("status") == "WAITING_FOR_MANAGER":
                        st.subheader("Final Manager Decision")
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            if st.button("✅ APPROVE Application", type="primary", use_container_width=True):
                                resp = requests.post(f"{API_BASE_URL}/approve/{st.session_state.thread_id}", json={"decision": "APPROVED"})
                                if resp.status_code == 200:
                                    st.session_state.latest_result["status"] = "COMPLETED"
                                    st.session_state.latest_result["final_decision"] = "APPROVED (Manager)"
                                    st.rerun()
                        with col_b:
                            if st.button("❌ REJECT Application", use_container_width=True):
                                resp = requests.post(f"{API_BASE_URL}/approve/{st.session_state.thread_id}", json={"decision": "REJECTED"})
                                if resp.status_code == 200:
                                    st.session_state.latest_result["status"] = "COMPLETED"
                                    st.session_state.latest_result["final_decision"] = "REJECTED (Manager)"
                                    st.rerun()
                    else:
                        st.success(f"**Final Decision:** {result.get('final_decision')}")
                        
                else:
                    st.write("Select an application from the pending list above to review.")

            # =========================================================================
            # MANAGER TAB 2: EXECUTIVE PORTFOLIO ANALYTICS & RISK INTELLIGENCE
            # =========================================================================
            with manager_tab2:
                st.subheader("📊 Executive Portfolio Analytics & Risk Intelligence")
                st.caption("Real-Time Credit Portfolio Distribution, Hurdle Rate Clearance, and Asset Quality Monitoring")

                try:
                    hist_res = requests.get(f"{API_BASE_URL}/history").json()
                    if hist_res and isinstance(hist_res, list) and len(hist_res) > 0:
                        records = []
                        for h in hist_res:
                            app = h.get("application_data") or {}
                            dec = h.get("decision", "PENDING")
                            l_type = app.get("loan_type", "Home Loan")
                            amt = float(h.get("loan_amount", 0.0))
                            cibil = int(app.get("credit_score", 700))
                            risk_cat = h.get("risk_category", "Moderate Risk")
                            
                            # Calculate MSME scorecard & ROI
                            msme_sc = None
                            cbi_grade = "N/A"
                            cbi_score = None
                            hurdle_met = True
                            
                            if "MSME" in l_type:
                                if "New" in l_type:
                                    msme_sc = calculate_mse_new_score(app)
                                else:
                                    msme_sc = calculate_mse_existing_score(app)
                                cbi_grade = msme_sc["grade"]
                                cbi_score = msme_sc["total_score"]
                                hurdle_met = msme_sc["hurdle_rate_met"]
                                
                            roi_val = get_applicable_roi(l_type, cibil, mse_grade=cbi_grade, cgtmse_covered=app.get("cgtmse_covered", False))
                            
                            # LTV and FOIR
                            gross_inc = float(app.get("gross_monthly_income", 100000))
                            p_val = float(app.get("property_value", 0))
                            ltv_val = round((amt / p_val * 100), 2) if p_val > 0 else 0.0
                            
                            records.append({
                                "thread_id": h.get("thread_id"),
                                "applicant_name": h.get("applicant_name"),
                                "loan_type": l_type,
                                "loan_amount": amt,
                                "credit_score": cibil,
                                "decision": dec,
                                "is_approved": "APPROVED" in dec.upper(),
                                "risk_category": risk_cat,
                                "cbi_grade": cbi_grade,
                                "cbi_score": cbi_score,
                                "hurdle_met": hurdle_met,
                                "official_roi": roi_val,
                                "ltv": ltv_val,
                                "created_at": h.get("created_at")
                            })
                        
                        df_p = pd.DataFrame(records)
                        
                        # --- ANALYTICS SCOPE SELECTOR ---
                        col_scope1, col_scope2 = st.columns([3, 1])
                        with col_scope1:
                            analytics_scope = st.radio(
                                "📊 Select Analytics Portfolio Scope:",
                                [
                                    "🟢 Sanctioned Credit Book (Approved Advances Only - Institutional Standard)",
                                    "🌐 Full Underwriting Pipeline (All Applications Including Rejected & Pending)"
                                ],
                                horizontal=True,
                                key="analytics_scope_selector"
                            )
                        with col_scope2:
                            st.write("") # spacer
                            if st.button("🔄 Refresh Analytics", use_container_width=True):
                                st.rerun()

                        # Determine active dataset based on scope
                        if "Approved Advances Only" in analytics_scope:
                            df_view = df_p[df_p["is_approved"]]
                            scope_label = "Sanctioned Credit Book"
                        else:
                            df_view = df_p
                            scope_label = "Full Underwriting Pipeline"
                        
                        # --- TOP KPI METRIC CARDS ---
                        total_apps = len(df_p)
                        approved_df = df_p[df_p["is_approved"]]
                        total_exposure = df_p["loan_amount"].sum()
                        total_sanctioned = approved_df["loan_amount"].sum()
                        sanction_rate = (len(approved_df) / total_apps * 100) if total_apps > 0 else 0.0
                        
                        view_count = len(df_view)
                        view_exposure = df_view["loan_amount"].sum() if not df_view.empty else 0.0
                        avg_cibil = df_view["credit_score"].mean() if not df_view.empty else 0.0
                        avg_roi = df_view["official_roi"].mean() if not df_view.empty else 0.0
                        
                        msme_view_df = df_view[df_view["cbi_grade"] != "N/A"]
                        msme_hurdle_pass = (msme_view_df["hurdle_met"].sum() / len(msme_view_df) * 100) if len(msme_view_df) > 0 else 0.0
                        
                        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
                        kpi1.metric(f"Active Facilities ({scope_label.split()[0]})", f"{view_count}", help=f"Total facilities in {scope_label}")
                        kpi2.metric("Active Capital Exposure", f"₹{view_exposure/1e7:.2f} Cr", help="Total loan volume in selected scope")
                        kpi3.metric("Total Sanctioned Capital", f"₹{total_sanctioned/1e7:.2f} Cr", help="Total credit volume approved by bank")
                        kpi4.metric("Pipeline Sanction Rate", f"{sanction_rate:.1f}%", help="Percentage of approved applications")
                        kpi5.metric("Weighted Avg ROI", f"{avg_roi:.2f}%", help="Average lending rate pegged to RBLR")
                        kpi6.metric("MSME Hurdle Pass", f"{msme_hurdle_pass:.1f}%", help="Enterprises meeting > 50 marks")
                        
                        st.markdown("---")
                        
                        # --- ROW 1 CHARTS: CBI RISK GRADES & PRODUCT EXPOSURE ---
                        c_col1, c_col2 = st.columns([3, 2])
                        
                        with c_col1:
                            st.subheader(f"🏛️ MSE Risk Grade Distribution ({scope_label})")
                            if not msme_view_df.empty:
                                all_cbi_grades = [f"CBI {i}" for i in range(1, 11)]
                                grade_counts = msme_view_df["cbi_grade"].value_counts().reindex(all_cbi_grades, fill_value=0).reset_index()
                                grade_counts.columns = ["Risk Grade", "Count"]
                                
                                # Assign colors: CBI 1-4 green, CBI 5-6 blue, CBI 7-10 red
                                colors = []
                                for g in grade_counts["Risk Grade"]:
                                    num = int(g.split()[1])
                                    if num <= 4:
                                        colors.append("#10B981") # Emerald Green (Prime)
                                    elif num <= 6:
                                        colors.append("#2563EB") # Royal Blue (Covenants)
                                    else:
                                        colors.append("#EF4444") # Crimson Red (Sub-Hurdle)
                                        
                                fig_grades = px.bar(
                                    grade_counts, x="Risk Grade", y="Count",
                                    text="Count",
                                    title=f"Central Bank MSE Risk Grades in {scope_label} (Hurdle Rate > 50 Marks)",
                                    labels={"Count": "Number of Enterprises", "Risk Grade": "Central Bank Risk Grade"}
                                )
                                fig_grades.update_traces(marker_color=colors, textposition="outside")
                                fig_grades.add_vline(x=5.5, line_width=2, line_dash="dash", line_color="#DC2626", annotation_text="HURDLE BENCHMARK (> 50 Marks)", annotation_position="top right")
                                fig_grades.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)")
                                st.plotly_chart(fig_grades, use_container_width=True)
                            else:
                                st.info("No MSME facilities available in this scope.")
                                
                        with c_col2:
                            st.subheader(f"🥧 Exposure Allocation by Product ({scope_label})")
                            if not df_view.empty:
                                prod_exp = df_view.groupby("loan_type")["loan_amount"].sum().reset_index()
                                prod_exp["loan_amount_cr"] = prod_exp["loan_amount"] / 1e7
                                fig_pie = px.pie(
                                    prod_exp, values="loan_amount_cr", names="loan_type",
                                    hole=0.45,
                                    title="Active Capital Exposure (₹ Crores)"
                                )
                                fig_pie.update_traces(textinfo="percent+label", pull=[0.05]*len(prod_exp))
                                fig_pie.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
                                st.plotly_chart(fig_pie, use_container_width=True)
                            else:
                                st.info("No active advances to display.")
                            
                        st.markdown("---")
                        
                        # --- ROW 2 CHARTS: RISK FRONTIER & DECISION FUNNEL ---
                        c_col3, c_col4 = st.columns([3, 2])
                        
                        with c_col3:
                            st.subheader(f"🎯 Credit Risk Frontier ({scope_label})")
                            if not df_view.empty:
                                df_view_copy = df_view.copy()
                                df_view_copy["decision_badge"] = df_view_copy["decision"].apply(lambda x: "APPROVED" if "APPROV" in str(x).upper() else "REJECTED")
                                fig_scatter = px.scatter(
                                    df_view_copy, x="credit_score", y="ltv",
                                    size="loan_amount",
                                    color="decision_badge",
                                    hover_name="applicant_name",
                                    hover_data={"loan_type": True, "credit_score": True, "ltv": ":.2f", "official_roi": ":.2f", "cbi_grade": True},
                                    color_discrete_map={"APPROVED": "#10B981", "REJECTED": "#EF4444"},
                                    title="Borrower Bureau Score (CIBIL) vs Collateral LTV Ratio (%)",
                                    labels={"credit_score": "CIBIL Bureau Score", "ltv": "Collateral LTV (%)", "decision_badge": "Decision"}
                                )
                                fig_scatter.add_hline(y=80.0, line_width=2, line_dash="dash", line_color="#DC2626", annotation_text="RBI 80% Max LTV Ceiling", annotation_position="bottom right")
                                fig_scatter.add_vline(x=700.0, line_width=2, line_dash="dot", line_color="#F59E0B", annotation_text="Prime CIBIL Cutoff (700)", annotation_position="top left")
                                fig_scatter.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20), plot_bgcolor="rgba(0,0,0,0)")
                                st.plotly_chart(fig_scatter, use_container_width=True)
                            else:
                                st.info("No active advances to plot.")
                            
                        with c_col4:
                            st.subheader("⚖️ Full Underwriting Conversion Funnel")
                            funnel_data = {
                                "Stage": ["Total Received", "LTV Compliant", "Hurdle Met (>50)", "Sanctioned"],
                                "Count": [
                                    len(df_p),
                                    len(df_p[df_p["ltv"] <= 80.0]),
                                    len(df_p[df_p["hurdle_met"] == True]),
                                    len(approved_df)
                                ]
                            }
                            df_funnel = pd.DataFrame(funnel_data)
                            fig_funnel = px.funnel(df_funnel, x="Count", y="Stage", title="Underwriting Policy Conversion Funnel")
                            fig_funnel.update_traces(marker_color=["#6366F1", "#3B82F6", "#10B981", "#059669"])
                            fig_funnel.update_layout(height=380, margin=dict(l=20, r=20, t=40, b=20))
                            st.plotly_chart(fig_funnel, use_container_width=True)
                            
                        st.markdown("---")
                        
                        # --- PORTFOLIO DATASET DOWNLOAD ---
                        st.subheader("📥 Export Regulatory & ALCO Portfolio Dataset")
                        st.caption(f"Download the active dataset ({scope_label}) for Asset-Liability Committee (ALCO) review and internal risk audits.")
                        
                        csv_export = df_view[['thread_id', 'applicant_name', 'loan_type', 'loan_amount', 'credit_score', 'cbi_grade', 'cbi_score', 'hurdle_met', 'official_roi', 'ltv', 'risk_category', 'decision', 'created_at']].to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label=f"📊 Download {scope_label} Dataset (CSV)",
                            data=csv_export,
                            file_name=f"CBoI_{scope_label.replace(' ', '_')}.csv",
                            mime="text/csv"
                        )
                        
                    else:
                        st.info("No application history available to generate portfolio analytics. Submit new applications to view real-time charts.")
                except Exception as e:
                    st.error(f"Failed to generate analytics: {e}")

            # =========================================================================
            # MANAGER TAB 3: APPLICATION DATABASE HISTORY & OVERRIDES
            # =========================================================================
            with manager_tab3:
                st.subheader("Application Database History & Override Log")
                st.markdown("View all processed applications stored in the central database.")
                
                search_query = st.text_input("🔍 Search by Applicant Name", "")
                
                if st.button("Refresh History"):
                    st.rerun()
                    
                try:
                    hist_res = requests.get(f"{API_BASE_URL}/history").json()
                    if hist_res and isinstance(hist_res, list) and len(hist_res) > 0:
                        df = pd.DataFrame(hist_res)
                        # Filter by search query
                        if search_query:
                            df = df[df['applicant_name'].str.contains(search_query, case=False, na=False)]
                            
                        if not df.empty:
                            # Convert created_at to proper datetime format
                            df['created_at'] = pd.to_datetime(df['created_at'])
                            # Format loan amount
                            df['loan_amount'] = df['loan_amount'].apply(lambda x: f"₹{x:,.2f}")
                            # Reorder and rename columns for display
                            display_df = df[['created_at', 'thread_id', 'applicant_name', 'loan_amount', 'risk_category', 'decision']]
                            st.dataframe(display_df, use_container_width=True, hide_index=True)
                            
                            st.markdown("---")
                            st.subheader("View Full Appraisal Report")
                            selected_thread = st.selectbox("Select Application ID to View:", df['thread_id'])
                            if selected_thread:
                                selected_row = df[df['thread_id'] == selected_thread].iloc[0]
                                
                                st.write(f"**Applicant:** {selected_row['applicant_name']} | **Decision:** {selected_row['decision']}")
                                
                                report_to_show = selected_row.get('detailed_report')
                                app_data = selected_row.get('application_data', {})
                                justification = selected_row.get('manager_justification')
                                
                                # --- TIMELINE SECTION ---
                                st.subheader("⏱️ Application Timeline")
                                
                                st.info(f"🟢 **Application Submitted** — *{selected_row['created_at'].strftime('%Y-%m-%d %H:%M:%S')}*")
                                st.info("🤖 **AI Verification & Appraisal Completed** — *System Analysis Generated*")
                                if justification:
                                    st.warning("🏦 **Initial Recommendation** — *System Recommended Decision*")
                                    st.error(f"🔴 **Manager Override** — *Decision Manually Changed to {selected_row['decision']}*")
                                else:
                                    st.success(f"✅ **Final Decision** — *{selected_row['decision']}*")
                                
                                st.markdown("---")
                                st.subheader("Applicant Profile & Data")
                                
                                p_col1, p_col2, p_col3 = st.columns(3)
                                with p_col1:
                                    st.markdown(f"**Name:** {app_data.get('name', 'N/A')}")
                                    st.markdown(f"**Age & Gender:** {app_data.get('age', 'N/A')} ({app_data.get('gender', 'N/A')})")
                                    st.markdown(f"**Marital Status:** {app_data.get('marital_status', 'N/A')}")
                                with p_col2:
                                    st.markdown(f"**Occupation:** {app_data.get('occupation', 'N/A')}")
                                    st.markdown(f"**Gross Income:** ₹{app_data.get('gross_monthly_income', 0):,.2f}")
                                    st.markdown(f"**Net Income:** ₹{app_data.get('net_monthly_income', 0):,.2f}")
                                    st.markdown(f"**Credit Score:** {app_data.get('credit_score', 'N/A')}")
                                with p_col3:
                                    st.markdown(f"**Loan Type:** {app_data.get('loan_type', 'N/A')}")
                                    st.markdown(f"**Loan Amount:** ₹{app_data.get('loan_amount', 0):,.2f}")
                                    st.markdown(f"**Interest Rate:** {app_data.get('interest_rate', 'N/A')}%")
                                    st.markdown(f"**Tenure:** {app_data.get('tenure_months', 'N/A')} months")
                                
                                if justification:
                                    st.error(f"**Override Justification:** {justification}")
                                    
                                if report_to_show:
                                    with st.expander("Expand Detailed Report Memo", expanded=True):
                                        st.markdown(report_to_show, unsafe_allow_html=True)
                                        
                                    # Create Downloadable Docx with Justification included
                                    full_report_text = report_to_show
                                    if justification:
                                        full_report_text += f"\n\n========================================\nMANAGER OVERRIDE JUSTIFICATION\n========================================\n{justification}\n"
                                    
                                    docx_bytes = utils.generate_docx(full_report_text)
                                    st.download_button(
                                        label="📄 Download Detailed Memo & Justifications (Docx)",
                                        data=docx_bytes,
                                        file_name=f"Appraisal_Report_{selected_thread}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                                else:
                                    st.info("No detailed report available for this application.")
                                    
                                st.markdown("---")
                                st.subheader("Override System Decision")
                                st.warning("Use this to forcefully modify the decision for accountability and audits.")
                                new_decision = st.radio("New Decision", ["APPROVED", "REJECTED"], horizontal=True, key=f"rad_{selected_thread}")
                                override_justification = st.text_area("Justification for Override", key=f"txt_{selected_thread}")
                                
                                if st.button("Submit Override", key=f"btn_{selected_thread}"):
                                    if not override_justification.strip():
                                        st.error("You must provide a manual justification letter to override this decision.")
                                    else:
                                        payload = {"decision": new_decision, "justification": override_justification}
                                        try:
                                            res = requests.post(f"{API_BASE_URL}/override/{selected_thread}", json=payload)
                                            if res.status_code == 200:
                                                st.success("Decision overridden successfully!")
                                                time.sleep(1)
                                                st.rerun()
                                            else:
                                                st.error(f"Failed to override: {res.text}")
                                        except Exception as e:
                                            st.error(f"Failed to override: {e}")
                        else:
                            st.info(f"No application history found matching '{search_query}'.")
                                
                    else:
                        st.info("No application history found in the database.")
                except Exception as e:
                    st.error(f"Failed to fetch history: {e}")
