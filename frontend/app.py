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
import base64

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

st.set_page_config(
    page_title="Central Bank of India - Intelligent Loan Appraisal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# INSTITUTIONAL DESIGN SYSTEM (CUSTOM CSS - DARK & LIGHT ADAPTIVE)
# =============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
}

/* Institutional Header Bar */
.cboi-brand-header {
    background: linear-gradient(135deg, #002B49 0%, #004080 50%, #002B49 100%);
    padding: 20px 28px;
    border-radius: 14px;
    color: #FFFFFF !important;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px -4px rgba(0, 43, 73, 0.35);
    border-bottom: 4px solid #C59B27;
}

.cboi-brand-title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #FFFFFF !important;
    margin: 0;
}

.cboi-brand-subtitle {
    font-size: 0.85rem;
    color: #E2E8F0 !important;
    margin-top: 3px;
    font-weight: 500;
}

/* Live Telemetry Card */
.telemetry-card {
    background: var(--background-color, rgba(255, 255, 255, 0.05));
    border: 1px solid rgba(128, 128, 128, 0.25);
    border-top: 4px solid #002B49;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 20px;
}

.telemetry-header {
    font-size: 0.95rem;
    font-weight: 700;
    color: #38BDF8;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 14px;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    padding-bottom: 8px;
}

.telemetry-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px dashed rgba(128, 128, 128, 0.2);
    font-size: 0.86rem;
}

.telemetry-label {
    font-weight: 500;
    opacity: 0.85;
}

.telemetry-value {
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

/* Status Chips */
.chip-safe {
    background: rgba(16, 185, 129, 0.15);
    color: #10B981;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #10B981;
    font-size: 0.72rem;
    font-weight: 700;
}
.chip-warn {
    background: rgba(245, 158, 11, 0.15);
    color: #F59E0B;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #F59E0B;
    font-size: 0.72rem;
    font-weight: 700;
}
.chip-danger {
    background: rgba(239, 68, 68, 0.15);
    color: #EF4444;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #EF4444;
    font-size: 0.72rem;
    font-weight: 700;
}

/* Step Header Badge */
.step-header {
    background: rgba(0, 43, 73, 0.1);
    border-left: 4px solid #002B49;
    padding: 8px 14px;
    font-size: 0.92rem;
    font-weight: 700;
    border-radius: 0 8px 8px 0;
    margin: 14px 0 10px 0;
}

/* Clean tabs underline */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 8px 8px 0 0;
    font-weight: 600;
    font-size: 0.88rem;
    padding: 0 18px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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
with st.sidebar:
    logo_file = os.path.join(FRONTEND_DIR, "Logo.png")
    if os.path.exists(logo_file):
        st.image(logo_file, use_container_width=True)
    st.markdown("### 🔐 Security & Access")
    st.session_state.role = st.radio("Select Portal Role:", ["Applicant", "Credit Manager"])

    if st.session_state.role == "Credit Manager":
        if not st.session_state.logged_in:
            def do_login():
                if st.session_state.get("passcode_input") == "CBOI_ADMIN":
                    st.session_state.logged_in = True
                else:
                    st.session_state.login_error = "Invalid Passcode (Use: CBOI_ADMIN)"
                    
            st.text_input("Enter Passcode:", type="password", key="passcode_input", on_change=do_login)
            st.button("🔑 Login", type="primary", use_container_width=True, on_click=do_login)
            
            if st.session_state.get("login_error"):
                st.error(st.session_state.login_error)
                st.session_state.login_error = ""
        else:
            st.success("✅ Authenticated as **Credit Manager**")
            def do_logout():
                st.session_state.logged_in = False
            st.button("Logout", use_container_width=True, on_click=do_logout)

    st.markdown("---")
    st.caption("🏦 **Central Bank of India**  \nAutomated Credit Appraisal System  \nVersion 2.4 | Base RBLR @ 8.25%")

# Top Institutional Header Bar with embedded logo
logo_path = os.path.join(FRONTEND_DIR, "Logo.png")
logo_img_html = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img_f:
        encoded_logo = base64.b64encode(img_f.read()).decode("utf-8")
        logo_img_html = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 52px; margin-right: 18px; border-radius: 6px; background: white; padding: 4px;" alt="Central Bank of India Logo"/>'

st.markdown(f"""
<div class="cboi-brand-header">
    <div style="display: flex; align-items: center;">
        {logo_img_html}
        <div>
            <h1 class="cboi-brand-title">सेन्ट्रल बैंक ऑफ़ इंडिया | Central Bank of India</h1>
            <div class="cboi-brand-subtitle">Autonomous Intelligent Loan Appraisal & Corporate Financial Underwriting Platform</div>
        </div>
    </div>
    <div style="text-align: right;">
        <span class="chip-safe" style="font-size: 0.8rem; padding: 5px 12px;">🟢 Core Underwriting Engine Online</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Define Navigation Tabs based on Role & Auth
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

# =============================================================================
# TAB 1: APPLICANT PORTAL (SPLIT-SCREEN WORKSPACE WITH LIVE TELEMETRY)
# =============================================================================
with tab1:
    tab_apply, tab_track = st.tabs(["📝 Submit Loan Application", "🔍 Track Application Status"])
    
    with tab_apply:
        # --- TOP UTILITY BAR (DEMO LOADER & OCR) ---
        with st.container(border=True):
            top_col1, top_col2 = st.columns([1.6, 1.4], gap="medium")
            with top_col1:
                st.markdown("##### ⚡ 1-Click Benchmark Demo Case Loader")
                demo_choice = st.selectbox(
                    "Select a pre-configured profile to auto-populate all underwriting parameters:",
                    [
                        "-- Choose a Profile --",
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
                if demo_choice != "-- Choose a Profile --":
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
                            "occupation": "Business", "gross_monthly_income": 300000, "net_monthly_income": -250000, "total_assets": 5000000,
                            "credit_score": 550, "avg_credit_balance_6m": 10000, "existing_emi": 80000, "active_lines": 5, "inquiries_6m": 4,
                            "loan_amount": 3000000, "tenure_months": 48, "loan_type": "MSME Loan - Existing Unit", "property_value": 4000000, "security_type": "Property",
                            "current_ratio": 0.90, "debt_equity_ratio": 4.5, "sales_growth_rate": -5.0, "pat_margin": -2.0,
                            "sanction_compliance": "Non-compliant", "stock_statement_status": "Non-Submission", "debt_servicing_history": "Overdue > 3 months",
                            "inventory_compliance": "High deviation", "bills_culture": False, "bill_payment_record": "Overdue > 3 months",
                            "review_documents_timely": False, "lc_bg_status": "Devolvement / Invocation", "ancillary_relationship": "None"
                        }
                    st.toast(f"Populated {demo_choice.split('(')[0].strip()}", icon="⚡")

            with top_col2:
                st.markdown("##### 📸 Auto-Fill via Document(s) / OCR")
                uploaded_docs = st.file_uploader(
                    "Upload Application / Salary Slip / KYC / Balance Sheet (PDF, DOCX, XLSX, CSV, PNG, JPG):",
                    type=['png', 'jpg', 'jpeg', 'pdf', 'docx', 'xlsx', 'xls', 'csv'],
                    accept_multiple_files=True
                )
                if uploaded_docs:
                    current_doc_signatures = [f"{d.name}_{d.size}" for d in uploaded_docs]
                    last_signatures = st.session_state.get("last_uploaded_doc_signatures", [])
                    if current_doc_signatures != last_signatures:
                        with st.spinner(f"Extracting parameters from {len(uploaded_docs)} document(s) via OCR/Parser..."):
                            extracted_files = []
                            for udoc in uploaded_docs:
                                fname = udoc.name.lower()
                                fbytes = udoc.read()
                                try:
                                    if fname.endswith(('.pdf', '.docx', '.xlsx', '.xls', '.csv')):
                                        extracted = FinancialDocumentParser.parse_any_file(udoc.name, fbytes)
                                        latest_rev = extracted.get("revenue", [42000000])[-1]
                                        latest_cogs = extracted.get("cogs", [24000000])[-1]
                                        latest_opex = extracted.get("operating_expenses", [5200000])[-1]
                                        latest_nfa = extracted.get("net_fixed_assets", [19500000])[-1]
                                        latest_cash = extracted.get("cash_and_bank", [3100000])[-1]
                                        latest_inv = extracted.get("inventory", [5000000])[-1]
                                        latest_stb = extracted.get("short_term_borrowings", [5500000])[-1]
                                        latest_ltd = extracted.get("long_term_debt", [3500000])[-1]
                                        latest_cap = extracted.get("paid_up_capital", [6000000])[-1]

                                        doc_data = {
                                            "name": extracted.get("company_name", "Corporate Borrower"),
                                            "gross_monthly_income": int(latest_rev / 12),
                                            "net_monthly_income": int(max(0.0, latest_rev - latest_cogs - latest_opex) / 12),
                                            "total_assets": int(latest_nfa + latest_cash + latest_inv),
                                            "credit_score": extracted.get("credit_score", 760),
                                            "avg_credit_balance_6m": int(latest_cash),
                                            "loan_amount": int(extracted.get("requested_loan_amount", 5000000)),
                                            "tenure_months": int(extracted.get("tenure_months", 60)),
                                            "loan_type": extracted.get("loan_type", "MSME Loan - Existing Unit"),
                                            "current_ratio": float(latest_cash / max(1.0, latest_stb)),
                                            "debt_equity_ratio": float(latest_ltd / max(1.0, latest_cap))
                                        }
                                        st.session_state.ocr_data.update({k: v for k, v in doc_data.items() if v is not None})
                                        extracted_files.append(udoc.name)
                                    else:
                                        extracted = utils.extract_ocr_data(fbytes)
                                        ocr_extracted = {}
                                        if extracted.get("name"):
                                            ocr_extracted["name"] = extracted["name"]
                                        if extracted.get("gross_monthly_income"):
                                            ocr_extracted["gross_monthly_income"] = extracted["gross_monthly_income"]
                                        if extracted.get("net_monthly_income"):
                                            ocr_extracted["net_monthly_income"] = extracted["net_monthly_income"]
                                        if extracted.get("loan_amount"):
                                            ocr_extracted["loan_amount"] = extracted["loan_amount"]
                                        if extracted.get("pan_number"):
                                            ocr_extracted["pan_number"] = extracted["pan_number"]
                                        defaults = {
                                            "age": 42, "gender": "Male", "marital_status": "Married", "category": "GEN",
                                            "occupation": "Professional", "total_assets": 12000000, "credit_score": 790,
                                            "avg_credit_balance_6m": 450000, "existing_emi": 15000, "active_lines": 2,
                                            "inquiries_6m": 0, "loan_type": "Home Loan", "tenure_months": 240,
                                            "security_type": "Property", "property_value": 7500000
                                        }
                                        for dk, dv in defaults.items():
                                            if dk not in st.session_state.ocr_data:
                                                ocr_extracted[dk] = dv
                                        st.session_state.ocr_data.update(ocr_extracted)
                                        extracted_files.append(udoc.name)
                                except Exception as u_err:
                                    st.warning(f"Note: Could not parse {udoc.name}: {u_err}")
                                    extracted_files.append(udoc.name)

                            st.session_state.last_uploaded_doc_signatures = current_doc_signatures
                            st.session_state.ocr_done = True
                            st.toast(f"✅ Auto-filled from {len(extracted_files)} document(s): {', '.join(extracted_files[:3])}!", icon="📸")
                            st.rerun()
                else:
                    if st.session_state.get("last_uploaded_doc_signatures"):
                        st.session_state.last_uploaded_doc_signatures = None
                        st.session_state.ocr_done = False

        st.markdown("<br>", unsafe_allow_html=True)

        # --- 2-COLUMN SPLIT-SCREEN WORKSPACE ---
        col_form, col_telemetry = st.columns([1.35, 0.85], gap="large")
        
        with col_form:
            # STEP 1: BORROWER & ENTITY IDENTITY
            st.markdown('<div class="step-header">1️⃣ Borrower & Enterprise Identity</div>', unsafe_allow_html=True)
            with st.container(border=True):
                f_c1, f_c2 = st.columns([2, 1])
                name = f_c1.text_input("Applicant / Enterprise Legal Name", st.session_state.ocr_data.get('name', "John Doe"))
                age = f_c2.number_input("Age / Business Vintage (Yrs)", min_value=18, max_value=80, value=int(st.session_state.ocr_data.get('age', 35)))
                
                f_c3, f_c4, f_c5 = st.columns(3)
                gender_default = st.session_state.ocr_data.get('gender', 'Male')
                gender_opts = ["Male", "Female", "Other"]
                gender_idx = gender_opts.index(gender_default) if gender_default in gender_opts else 0
                gender = f_c3.selectbox("Gender", gender_opts, index=gender_idx)
                
                mar_default = st.session_state.ocr_data.get('marital_status', 'Married')
                mar_opts = ["Single", "Married", "Divorced", "Widowed"]
                mar_idx = mar_opts.index(mar_default) if mar_default in mar_opts else 1
                marital_status = f_c4.selectbox("Marital Status", mar_opts, index=mar_idx)
                
                cat_default = st.session_state.ocr_data.get('category', 'GEN')
                cat_opts = ["GEN", "OBC", "SC", "ST"]
                cat_idx = cat_opts.index(cat_default) if cat_default in cat_opts else 0
                category = f_c5.selectbox("Social Category", cat_opts, index=cat_idx)
                
                occ_default = st.session_state.ocr_data.get('occupation', 'Business')
                occ_opts = ["Salaried", "Self_Employed", "Business", "Professional", "Retired"]
                occ_idx = occ_opts.index(occ_default) if occ_default in occ_opts else 2
                occupation = st.selectbox("Constitution / Primary Occupation", occ_opts, index=occ_idx)

            # STEP 2: FINANCIAL CAPACITY & BUREAU PROFILE
            st.markdown('<div class="step-header">2️⃣ Audited Financial Capacity & Bureau Track Record</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fc_c1, fc_c2 = st.columns(2)
                gross_income = fc_c1.number_input("Gross Monthly Revenue / Income (₹)", min_value=0, value=max(0, int(float(st.session_state.ocr_data.get('gross_monthly_income', 150000)))), step=10000)
                net_income = fc_c2.number_input("Net Monthly Profit / Take-Home (₹)", value=int(float(st.session_state.ocr_data.get('net_monthly_income', 120000))), step=10000)
                
                fc_c3, fc_c4 = st.columns(2)
                total_assets = fc_c3.number_input("Total Balance Sheet Assets (₹)", min_value=0, value=max(0, int(float(st.session_state.ocr_data.get('total_assets', 15000000)))), step=500000)
                credit_score = fc_c4.number_input("CIBIL Bureau Score (300-900)", min_value=300, max_value=900, value=int(st.session_state.ocr_data.get('credit_score', 750)), step=10)
                
                fc_c5, fc_c6, fc_c7 = st.columns(3)
                avg_credit_balance_6m = fc_c5.number_input("Avg 6M Bank Balance (₹)", value=int(float(st.session_state.ocr_data.get('avg_credit_balance_6m', 500000))), step=10000)
                existing_emi = fc_c6.number_input("Existing Monthly EMIs (₹)", min_value=0, value=max(0, int(float(st.session_state.ocr_data.get('existing_emi', 25000)))), step=5000)
                active_lines = fc_c7.number_input("Active Credit Lines", min_value=0, value=max(0, int(st.session_state.ocr_data.get('active_lines', 2))), step=1)
                inquiries_6m = st.number_input("Hard Inquiries (Last 6M)", min_value=0, value=max(0, int(st.session_state.ocr_data.get('inquiries_6m', 0))), step=1)

            # STEP 3: FACILITY REQUEST, COLLATERAL & MSME SCORECARD
            st.markdown('<div class="step-header">3️⃣ Facility Request, Security & Regulatory Scorecard</div>', unsafe_allow_html=True)
            with st.container(border=True):
                fr_c1, fr_c2 = st.columns(2)
                loan_amount = fr_c1.number_input("Requested Facility Limit (₹)", min_value=100000, value=max(100000, int(float(st.session_state.ocr_data.get('loan_amount', 5000000)))), step=100000)
                tenure_months = fr_c2.number_input("Requested Tenure (Months)", min_value=12, value=max(12, int(st.session_state.ocr_data.get('tenure_months', 240))), step=12)
                
                fr_c3, fr_c4 = st.columns(2)
                ltype_default = st.session_state.ocr_data.get('loan_type', 'Home Loan')
                ltype_opts = ["Home Loan", "Auto Loan", "Personal Loan", "Education Loan", "MSME Loan - Existing Unit", "MSME Loan - New Unit"]
                ltype_idx = ltype_opts.index(ltype_default) if ltype_default in ltype_opts else 0
                loan_type = fr_c3.selectbox("Product Class / Facility Type", ltype_opts, index=ltype_idx, key="loan_type_select")
                
                sec_default = st.session_state.ocr_data.get('security_type', 'Property')
                sec_opts = ["Property", "Vehicle", "Liquid_Assets", "CGTMSE / Plant & Machinery", "None"]
                sec_idx = sec_opts.index(sec_default) if sec_default in sec_opts else 0
                security_type = fr_c4.selectbox("Primary Security Type", sec_opts, index=sec_idx)
                
                property_value = st.number_input("Primary Collateral / Property Realizable Value (₹)", min_value=0, value=max(0, int(float(st.session_state.ocr_data.get('property_value', 7000000)))), step=100000)

                # Reactive MSME Scoring Parameters
                msme_data = {}
                if "MSME" in loan_type:
                    st.markdown("---")
                    if "New" in loan_type:
                        st.caption("🏢 **Central Bank of India Form MSE II (New Units)**")
                        m_col1, m_col2, m_col3 = st.columns(3)
                        msme_data["projected_sales_growth"] = m_col1.number_input("Projected Sales Growth (%)", value=float(st.session_state.ocr_data.get('projected_sales_growth', 16.0)), step=1.0)
                        msme_data["projected_pat_margin"] = m_col2.number_input("Projected PAT Margin (%)", value=float(st.session_state.ocr_data.get('projected_pat_margin', 12.0)), step=0.5)
                        msme_data["projected_der"] = m_col3.number_input("Projected DER", value=float(st.session_state.ocr_data.get('projected_der', 1.8)), step=0.1)
                        
                        m_col4, m_col5, m_col6 = st.columns(3)
                        msme_data["inputs_access"] = m_col4.selectbox("Raw Materials Access", ["Locally Available / Tied up", "Source Identified", "Not Identified"])
                        msme_data["market_access"] = m_col5.selectbox("Market Off-take", ["Locally Available / Tied up", "Market Identified", "Unidentified"])
                        msme_data["promoter_experience"] = m_col6.selectbox("Promoter Qualification", ["Qualified and Experienced", "Qualified / Trained", "No qualification/experience"])
                        
                        m_col7, m_col8, m_col9 = st.columns(3)
                        msme_data["bank_relationship"] = m_col7.selectbox("Bank Relationship", ["Existing Customer", "Introduced by Govt Dept / Others"])
                        msme_data["premises_type"] = m_col8.selectbox("Operating Premises", ["Owned", "Leased / Rented"])
                        msme_data["collateral_coverage"] = m_col9.selectbox("Collateral / CGTMSE", ["Covered under CGTMSE Scheme", "Over 100% Tangible Collateral", "Up to 50% Collateral", "Below 50% Collateral", "Unsecured"])
                    else:
                        st.caption("🏢 **Central Bank of India Form MSE 1 (Existing Units)**")
                        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                        msme_data["current_ratio"] = m_col1.number_input("Current Ratio (CR)", value=max(0.0, float(st.session_state.ocr_data.get('current_ratio', 1.35))), step=0.05)
                        msme_data["debt_equity_ratio"] = m_col2.number_input("Debt-Equity (DER)", value=float(st.session_state.ocr_data.get('debt_equity_ratio', 1.9)), step=0.1)
                        msme_data["sales_growth_rate"] = m_col3.number_input("3-Yr Growth (%)", value=float(st.session_state.ocr_data.get('sales_growth_rate', 18.0)), step=1.0)
                        msme_data["pat_margin"] = m_col4.number_input("PAT Margin (%)", value=float(st.session_state.ocr_data.get('pat_margin', 11.0)), step=0.5)
                        
                        m_col5, m_col6, m_col7 = st.columns(3)
                        s_default = st.session_state.ocr_data.get('sanction_compliance', 'Compliant')
                        s_opts = ["Compliant", "Non-Compliant"]
                        s_idx = s_opts.index(s_default) if s_default in s_opts else 0
                        msme_data["sanction_compliance"] = m_col5.selectbox("Sanction Compliance", s_opts, index=s_idx)

                        stk_default = st.session_state.ocr_data.get('stock_statement_status', 'Timely')
                        stk_opts = ["Timely", "Delayed", "Non-Submission"]
                        stk_idx = stk_opts.index(stk_default) if stk_default in stk_opts else 0
                        msme_data["stock_statement_status"] = m_col6.selectbox("QIS / Stock Statements", stk_opts, index=stk_idx)

                        debt_default = st.session_state.ocr_data.get('debt_servicing_history', 'Within 1 month')
                        debt_opts = ["Within 1 month", "Within 2 months", "Within 3 months", "Overdue > 3 months"]
                        debt_idx = debt_opts.index(debt_default) if debt_default in debt_opts else 0
                        msme_data["debt_servicing_history"] = m_col7.selectbox("Debt Servicing Track", debt_opts, index=debt_idx)
                        
                        m_col8, m_col9, m_col10 = st.columns(3)
                        inv_default = st.session_state.ocr_data.get('inventory_compliance', 'Fair compliance')
                        inv_opts = ["Fair Compliance", "Compliance (15%-30% dev)"]
                        inv_idx = 0 if "fair" in str(inv_default).lower() else 1
                        msme_data["inventory_compliance"] = m_col8.selectbox("Inventory Norms", inv_opts, index=inv_idx)

                        bills_default = st.session_state.ocr_data.get('bills_culture', True)
                        bills_idx = 0 if bills_default else 1
                        msme_data["bills_culture"] = m_col9.selectbox("Bills Culture", ["Compliant", "Non-Compliant"], index=bills_idx) == "Compliant"

                        bpay_default = st.session_state.ocr_data.get('bill_payment_record', 'Prompt')
                        bpay_opts = ["Prompt", "Delayed", "Overdue > 3 months"]
                        bpay_idx = bpay_opts.index(bpay_default) if bpay_default in bpay_opts else 0
                        msme_data["bill_payment_record"] = m_col10.selectbox("Bill Payment Track", bpay_opts, index=bpay_idx)
                        
                        m_col11, m_col12, m_col13 = st.columns(3)
                        rev_default = st.session_state.ocr_data.get('review_documents_timely', True)
                        rev_idx = 0 if rev_default else 1
                        msme_data["review_documents_timely"] = m_col11.selectbox("Annual Review Docs", ["Timely (< 3 mos)", "Delayed"], index=rev_idx) == "Timely (< 3 mos)"

                        lc_default = st.session_state.ocr_data.get('lc_bg_status', 'Prompt / No Facility')
                        lc_opts = ["Prompt / No Facility", "Devolvement / Invocation"]
                        lc_idx = lc_opts.index(lc_default) if lc_default in lc_opts else 0
                        msme_data["lc_bg_status"] = m_col12.selectbox("LC / BG Commitments", lc_opts, index=lc_idx)

                        anc_default = st.session_state.ocr_data.get('ancillary_relationship', 'Substantial')
                        anc_opts = ["Substantial", "Moderate"]
                        anc_idx = anc_opts.index(anc_default) if anc_default in anc_opts else 0
                        msme_data["ancillary_relationship"] = m_col13.selectbox("Ancillary Association", anc_opts, index=anc_idx)
                        
                        collat_default = st.session_state.ocr_data.get('collateral_coverage', 'Covered under CGTMSE Scheme')
                        collat_opts = ["Covered under CGTMSE Scheme", "Over 100% Tangible Collateral", "Up to 50% Collateral", "Below 50% Collateral", "Unsecured"]
                        collat_idx = collat_opts.index(collat_default) if collat_default in collat_opts else 0
                        msme_data["collateral_coverage"] = st.selectbox("Collateral / Primary Security Backing", collat_opts, index=collat_idx)

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.button("🚀 Submit Application for Automated Appraisal", type="primary", use_container_width=True)

        # --- RIGHT COLUMN: LIVE REAL-TIME TELEMETRY CARD ---
        with col_telemetry:
            # Calculate Real-Time Metrics
            is_cgtmse_val = "CGTMSE" in str(security_type) or (msme_data and "CGTMSE" in str(msme_data.get("collateral_coverage", "")))
            
            # Estimate MSE Grade if MSME
            preview_grade = "Standard"
            if "MSME" in loan_type:
                synth_data = {
                    "current_ratio": msme_data.get("current_ratio", 1.35),
                    "debt_equity_ratio": msme_data.get("debt_equity_ratio", 1.9),
                    "sales_growth_rate": msme_data.get("sales_growth_rate", 18.0),
                    "pat_margin": msme_data.get("pat_margin", 11.0),
                    "sanction_compliance": msme_data.get("sanction_compliance", "Compliant"),
                    "stock_statement_status": msme_data.get("stock_statement_status", "Timely"),
                    "debt_servicing_history": msme_data.get("debt_servicing_history", "Within 1 month"),
                    "inventory_compliance": msme_data.get("inventory_compliance", "Fair Compliance"),
                    "bills_culture": msme_data.get("bills_culture", True),
                    "bill_payment_record": msme_data.get("bill_payment_record", "Prompt"),
                    "review_documents_timely": msme_data.get("review_documents_timely", True),
                    "lc_bg_status": msme_data.get("lc_bg_status", "Prompt / No Facility"),
                    "ancillary_relationship": msme_data.get("ancillary_relationship", "Substantial")
                }
                if "New" in loan_type:
                    sc = calculate_mse_new_score({**synth_data, **msme_data})
                else:
                    sc = calculate_mse_existing_score(synth_data)
                preview_grade = sc.get("grade", "CBI 4")

            live_roi = get_applicable_roi(loan_type, credit_score, mse_grade=preview_grade, cgtmse_covered=is_cgtmse_val)
            
            # Live EMI Calculation
            r = (live_roi / 100.0) / 12.0
            n = tenure_months
            if r > 0 and n > 0:
                live_emi = (loan_amount * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1)
            else:
                live_emi = loan_amount / max(1, n)
                
            # Live FOIR
            live_foir = ((existing_emi + live_emi) / max(1.0, float(gross_income))) * 100.0
            
            # Live LTV
            live_ltv = (loan_amount / float(property_value) * 100.0) if property_value > 0 else 0.0

            st.markdown("""
            <div class="telemetry-card">
                <div class="telemetry-header">⚡ Live Underwriting Telemetry</div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="telemetry-row">
                <span class="telemetry-label">Official Bank ROI:</span>
                <span class="telemetry-value" style="color: #38BDF8; font-size: 1.05rem;">{live_roi:.2f}% p.a.</span>
            </div>
            <div class="telemetry-row">
                <span class="telemetry-label">Monthly EMI:</span>
                <span class="telemetry-value">₹{live_emi:,.2f}</span>
            </div>
            <div class="telemetry-row">
                <span class="telemetry-label">Calculated FOIR:</span>
                <span class="telemetry-value">
                    <span class="{'chip-safe' if live_foir <= 50 else 'chip-danger'}">{live_foir:.1f}%</span>
                </span>
            </div>
            <div class="telemetry-row">
                <span class="telemetry-label">Collateral LTV:</span>
                <span class="telemetry-value">
                    <span class="{'chip-safe' if live_ltv <= 80 else 'chip-danger'}">{live_ltv:.1f}%</span>
                </span>
            </div>
            <div class="telemetry-row">
                <span class="telemetry-label">Regulatory Grade:</span>
                <span class="telemetry-value"><span class="chip-safe">{preview_grade}</span></span>
            </div>
            """, unsafe_allow_html=True)

            if is_cgtmse_val:
                st.markdown('<div style="margin-top: 10px;"><span class="chip-safe">✅ 25 bps CGTMSE Guarantee Concession Applied</span></div>', unsafe_allow_html=True)
                
            st.markdown("""
            <div style="margin-top: 16px; font-size: 0.78rem; opacity: 0.75;">
                📌 <em>All values automatically re-calculated from Central Bank of India RBLR lending grid as you type.</em>
            </div>
            </div>
            """, unsafe_allow_html=True)

        # Handle Submit Click
        if submitted:
            payload = {
                "name": name, "age": age, "gender": gender, "marital_status": marital_status,
                "category": category, "occupation": occupation, "gross_monthly_income": gross_income,
                "net_monthly_income": net_income, "total_assets": total_assets, "credit_score": credit_score,
                "avg_credit_balance_6m": avg_credit_balance_6m, "existing_emi": existing_emi,
                "active_lines": active_lines, "inquiries_6m": inquiries_6m, "loan_amount": loan_amount,
                "tenure_months": tenure_months, "loan_type": loan_type, "property_value": property_value,
                "security_type": security_type
            }
            if msme_data:
                payload.update(msme_data)
                
            with st.spinner("Submitting to Central Bank Automated Underwriting Engine..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/apply", json=payload).json()
                    st.session_state.thread_id = res.get("thread_id")
                    st.session_state.polling = True
                    st.success(f"Application Submitted! Tracking ID: `{st.session_state.thread_id}`")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to submit: {e}")

        # Polling Workflow
        if st.session_state.polling and st.session_state.thread_id:
            status_placeholder = st.empty()
            with status_placeholder.container():
                st.info("Tracking autonomous multi-agent underwriting progress...")
                try:
                    res = requests.get(f"{API_BASE_URL}/status/{st.session_state.thread_id}").json()
                    status = res.get("status")
                    
                    if status == "PROCESSING" or status == "INITIALIZING":
                        logs = res.get("agent_logs", [])
                        st.write(f"Agents executed: {len(logs)} / 10")
                        st.progress(min(len(logs) * 10, 100))
                        for log in logs[-3:]:
                            st.write(f"✅ {log['agent']}: {log['summary']}")
                        time.sleep(2)
                        st.rerun()
                    elif status == "WAITING_FOR_MANAGER":
                        st.session_state.polling = False
                        st.session_state.latest_result = res
                        st.success("Appraisal Complete! Awaiting Credit Manager Review.")
                        st.info("Log in as Credit Manager to approve.")
                    elif status == "COMPLETED":
                        st.session_state.polling = False
                        st.session_state.latest_result = res
                        st.success("Decision Finalized.")
                except Exception as e:
                    st.error(f"Status check error: {e}")
                    time.sleep(2)
                    st.rerun()

    with tab_track:
        st.markdown("### 🔍 Application Status & Document Retrieval")
        st.markdown("Enter your assigned **Tracking ID** to view real-time status or download your final Credit Appraisal Memorandum.")
        
        t_col1, t_col2 = st.columns([3, 1])
        track_id = t_col1.text_input("Application Tracking ID (UUID)", placeholder="e.g. 550e8400-e29b-41d4-a716-446655440000")
        check_btn = t_col2.button("🔍 Check Status", use_container_width=True)
        
        if check_btn and track_id:
            try:
                res = requests.get(f"{API_BASE_URL}/status/{track_id.strip()}").json()
                status = res.get("status")
                if status == "INITIALIZING":
                    st.info("Application is initializing.")
                elif status in ["PROCESSING", "WAITING_FOR_MANAGER"]:
                    st.warning("Application is currently under review by Credit Committee.")
                elif status == "COMPLETED":
                    st.success(f"Final Decision: **{res.get('decision_outcome')}**")
                    st.markdown("---")
                    st.markdown(res.get("short_report", ""), unsafe_allow_html=True)
                    docx_bytes = utils.generate_docx(res.get("short_report", ""))
                    st.download_button("📄 Download Official Report (Word .docx)", docx_bytes, "Applicant_Appraisal_Report.docx")
            except Exception as e:
                st.error("Invalid Tracking ID or network error.")

# =============================================================================
# TAB 2: CORPORATE FINANCIAL INTELLIGENCE & VALUATION HUB
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
                    "📁 Upload Custom Financials (PDF, Word DOCX, Excel XLSX, CSV, JSON)"
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
            uploaded_files = st.file_uploader(
                "Upload Audited Balance Sheet / P&L (PDF, Scanned PDF, Word DOCX, Excel XLSX/XLS, CSV, JSON, PNG, JPG):", 
                type=["pdf", "docx", "xlsx", "xls", "csv", "json", "png", "jpg", "jpeg"],
                accept_multiple_files=True
            )
            if uploaded_files:
                parsed_docs = []
                file_badges = []
                for uf in uploaded_files:
                    fname = uf.name
                    fbytes = uf.getvalue()
                    try:
                        parsed = FinancialDocumentParser.parse_any_file(fname, fbytes)
                        parsed_docs.append(parsed)
                        file_badges.append(f"📄 **{fname}**")
                    except Exception as parse_err:
                        st.warning(f"⚠️ Notice on **{fname}**: {parse_err}. Auto-normalizing document.")
                
                if parsed_docs:
                    raw_corp_data = FinancialDocumentParser.merge_multiple_documents(parsed_docs)
                    st.success(f"✅ Successfully ingested & synthesized **{len(parsed_docs)}** document(s) for **{raw_corp_data.get('company_name', 'Corporate Borrower')}**: " + ", ".join(file_badges))
                else:
                    st.info("Upload multi-year financial statements or select a benchmark corporate profile.")
                    raw_corp_data = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]
            else:
                st.info("Upload multi-year financial statements (PDF, Word, Excel, CSV, PNG, JPG) or select a benchmark corporate profile from above.")
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

        # --- TOP EXECUTIVE KPI BANNER (NATIVE STREAMLIT METRICS) ---
        latest_rev = spread["pnl"]["revenue"][-1]
        latest_pat = spread["pnl"]["pat"][-1]
        latest_tnw = spread["balance_sheet"]["tangible_net_worth"][-1]
        
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric(f"Audited Revenue ({spread['years'][-1]})", f"₹{latest_rev/1e7:.2f} Cr", delta=f"{ratios['efficiency']['sales_growth_rate_pct'][-1]:.1f}% YoY", help="Latest annual turnover")
        k2.metric("Tangible Net Worth", f"₹{latest_tnw/1e7:.2f} Cr", help="Net Worth = Equity + Reserves")
        k3.metric("PAT Margin", f"{ratios['profitability']['pat_margin_pct'][-1]:.1f}%", delta=f"ROCE: {ratios['profitability']['return_on_capital_employed_pct'][-1]:.1f}%", help="Net profit margin")
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
            num_yr = len(years)
            
            col_pnl, col_bs = st.columns(2)
            with col_pnl:
                st.markdown("##### 📈 Profit & Loss Statement (₹ Lakhs)")
                pnl_rows = [
                    ("Gross Turnover / Sales", [spread["pnl"]["revenue"][i]/1e5 for i in range(num_yr)]),
                    ("Cost of Goods Sold (COGS)", [spread["pnl"]["cogs"][i]/1e5 for i in range(num_yr)]),
                    ("Gross Profit", [spread["pnl"]["gross_profit"][i]/1e5 for i in range(num_yr)]),
                    ("Operating Expenses (Opex)", [spread["pnl"]["operating_expenses"][i]/1e5 for i in range(num_yr)]),
                    ("EBITDA (Operating Profit)", [spread["pnl"]["ebitda"][i]/1e5 for i in range(num_yr)]),
                    ("Depreciation & Amortization", [spread["pnl"]["depreciation"][i]/1e5 for i in range(num_yr)]),
                    ("EBIT (Operating Income)", [spread["pnl"]["ebit"][i]/1e5 for i in range(num_yr)]),
                    ("Interest / Finance Charges", [spread["pnl"]["interest_expense"][i]/1e5 for i in range(num_yr)]),
                    ("Profit After Tax (PAT)", [spread["pnl"]["pat"][i]/1e5 for i in range(num_yr)]),
                    ("Cash Accruals (PAT + Dep)", [spread["pnl"]["cash_accruals"][i]/1e5 for i in range(num_yr)])
                ]
                pnl_data = {"Line Item": [r[0] for r in pnl_rows]}
                for i, y in enumerate(years):
                    pnl_data[y] = [r[1][i] for r in pnl_rows]
                pnl_df = pd.DataFrame(pnl_data)
                st.dataframe(pnl_df.style.format({y: "{:,.2f}" for y in years}), use_container_width=True, hide_index=True)

            with col_bs:
                st.markdown("##### 🏛️ Balance Sheet (₹ Lakhs)")
                bs_rows = [
                    ("Cash & Bank Balances", [spread["balance_sheet"]["cash_and_bank"][i]/1e5 for i in range(num_yr)]),
                    ("Sundry Debtors (Receivables)", [spread["balance_sheet"]["sundry_debtors"][i]/1e5 for i in range(num_yr)]),
                    ("Inventory (Raw, WIP, FG)", [spread["balance_sheet"]["inventory"][i]/1e5 for i in range(num_yr)]),
                    ("Total Current Assets", [spread["balance_sheet"]["current_assets"][i]/1e5 for i in range(num_yr)]),
                    ("Net Fixed Assets (PPE)", [spread["balance_sheet"]["net_fixed_assets"][i]/1e5 for i in range(num_yr)]),
                    ("Total Assets", [spread["balance_sheet"]["total_assets"][i]/1e5 for i in range(num_yr)]),
                    ("Sundry Creditors (Payables)", [spread["balance_sheet"]["sundry_creditors"][i]/1e5 for i in range(num_yr)]),
                    ("Short-Term Bank Borrowings", [spread["balance_sheet"]["short_term_borrowings"][i]/1e5 for i in range(num_yr)]),
                    ("Total Current Liabilities", [spread["balance_sheet"]["current_liabilities"][i]/1e5 for i in range(num_yr)]),
                    ("Long-Term Term Debt", [spread["balance_sheet"]["long_term_debt"][i]/1e5 for i in range(num_yr)]),
                    ("Tangible Net Worth (TNW)", [spread["balance_sheet"]["tangible_net_worth"][i]/1e5 for i in range(num_yr)])
                ]
                bs_data = {"Line Item": [r[0] for r in bs_rows]}
                for i, y in enumerate(years):
                    bs_data[y] = [r[1][i] for r in bs_rows]
                bs_df = pd.DataFrame(bs_data)
                st.dataframe(bs_df.style.format({y: "{:,.2f}" for y in years}), use_container_width=True, hide_index=True)

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
            scorecard_items = mse_scorecard.get("parameter_scores") or mse_scorecard.get("breakdown") or []
            param_rows = []
            for p in scorecard_items:
                param_rows.append({
                    "Parameter Name": p.get("param") or p.get("parameter") or "Parameter",
                    "Assessed Value / Ratio": p.get("value") or p.get("description") or "",
                    "Score Awarded": p.get("score", 0),
                    "Max Marks": p.get("max") or p.get("max_score") or 10
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

# =============================================================================
# TAB 3: CREDIT MANAGER DASHBOARD
# =============================================================================
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
                        <div style="background-color: rgba(128,128,128,0.2); border-radius: 5px; width: 100%; height: 25px;">
                            <div style="background-color: {bar_color}; width: {min(pd_val, 100.0)}%; height: 100%; border-radius: 5px;"></div>
                        </div>
                    ''', unsafe_allow_html=True)
                    
                    st.caption(f"Risk Category: **{risk.get('risk_category', 'Unknown')}** | Explanation: {risk.get('explanation', '')}")
                    
                    # --- CRITICAL RISK DRIVERS ---
                    st.markdown("##### 🔍 Key Risk Drivers (Top 3 Impacting Factors):")
                    drivers = risk.get('drivers') or risk.get('top_factors') or []
                    if drivers:
                        for d in drivers:
                            feat_name = d.get('feature', 'Unknown')
                            shap_val = d.get('shap_value') or d.get('impact') or 0.0
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
