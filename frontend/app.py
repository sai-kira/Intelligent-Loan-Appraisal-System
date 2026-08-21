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

st.set_page_config(
    page_title="Central Bank of India - Intelligent Loan Appraisal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# INSTITUTIONAL DESIGN SYSTEM (CUSTOM CSS)
# =============================================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    color: #1E293B;
}

/* Institutional Header Bar */
.cboi-brand-header {
    background: linear-gradient(135deg, #002B49 0%, #004080 50%, #002B49 100%);
    padding: 20px 28px;
    border-radius: 14px;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px -4px rgba(0, 43, 73, 0.25);
    border-bottom: 4px solid #C59B27;
}

.cboi-brand-title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    margin: 0;
}

.cboi-brand-subtitle {
    font-size: 0.85rem;
    color: #E2E8F0;
    margin-top: 3px;
    font-weight: 500;
}

/* Live Telemetry Card */
.telemetry-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-top: 4px solid #002B49;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    position: sticky;
    top: 20px;
}

.telemetry-header {
    font-size: 0.95rem;
    font-weight: 700;
    color: #002B49;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 14px;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 8px;
}

.telemetry-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px dashed #F1F5F9;
    font-size: 0.86rem;
}

.telemetry-label {
    color: #64748B;
    font-weight: 500;
}

.telemetry-value {
    color: #0F172A;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

/* Glassmorphism KPI Tile */
.kpi-tile {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
    margin-bottom: 12px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-tile:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 43, 73, 0.08);
    border-color: #CBD5E1;
}
.kpi-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748B;
    margin-bottom: 4px;
}
.kpi-val {
    font-size: 1.45rem;
    font-weight: 800;
    color: #002B49;
    line-height: 1.2;
}
.kpi-sub {
    font-size: 0.74rem;
    margin-top: 4px;
    font-weight: 600;
}

/* Status Chips */
.chip-safe {
    background: #ECFDF5;
    color: #059669;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #A7F3D0;
    font-size: 0.72rem;
    font-weight: 700;
}
.chip-warn {
    background: #FFFBEB;
    color: #D97706;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #FDE68A;
    font-size: 0.72rem;
    font-weight: 700;
}
.chip-danger {
    background: #FEF2F2;
    color: #DC2626;
    padding: 3px 8px;
    border-radius: 12px;
    border: 1px solid #FECACA;
    font-size: 0.72rem;
    font-weight: 700;
}

/* Step Header Badge */
.step-header {
    background: #F8FAFC;
    border-left: 4px solid #002B49;
    padding: 8px 14px;
    font-size: 0.92rem;
    font-weight: 700;
    color: #002B49;
    border-radius: 0 8px 8px 0;
    margin: 14px 0 10px 0;
}

/* Document Memo Canvas */
.memo-canvas {
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
    padding: 28px 32px;
    box-shadow: 0 6px 25px rgba(0, 0, 0, 0.05);
    line-height: 1.6;
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

import base64

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
                st.markdown("##### 📸 Auto-Fill via Document OCR")
                uploaded_file = st.file_uploader("Upload scanned form / salary slip / KYC (PNG/JPG):", type=['png', 'jpg', 'jpeg'])
                if uploaded_file is not None and not st.session_state.ocr_done:
                    with st.spinner("Extracting with EasyOCR..."):
                        extracted = utils.extract_ocr_data(uploaded_file.read())
                        st.session_state.ocr_data = extracted
                        st.session_state.ocr_done = True
                        st.success("Fields extracted from scan successfully!")
                        st.rerun()

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
                <span class="telemetry-value" style="color: #003366; font-size: 1.05rem;">{live_roi:.2f}% p.a.</span>
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
            <div style="margin-top: 16px; font-size: 0.78rem; color: #64748B;">
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
        st.markdown("### 🏢 Corporate Financial Intelligence, Forensic Audit & Valuation Hub")
        st.caption("3-Year Multi-Year CMA Spreading, 5-Pillar Diagnostics, Forensic Accounting (Altman Z'' & Beneish M-Score), Macro Stress Testing & DCF Enterprise Valuation")

        col_sel1, col_sel2 = st.columns([3, 2])
        with col_sel1:
            corp_choice = st.selectbox(
                "Select Corporate Entity or Ingest Statements:",
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
            proposed_corp_loan = st.number_input("Requested Credit Limit (₹):", min_value=100000.0, max_value=500000000.0, value=5000000.0, step=500000.0)

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
                    st.success("Custom financials parsed successfully!")
                except Exception as e:
                    st.error(f"Error parsing uploaded file: {e}")
                    raw_corp_data = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]
            else:
                st.info("Ingest custom financials or select a benchmark corporate profile.")
                raw_corp_data = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]

        raw_corp_data["requested_loan_amount"] = proposed_corp_loan

        # Core Mathematical Computations
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

        latest_rev = spread["pnl"]["revenue"][-1]
        latest_pat = spread["pnl"]["pat"][-1]
        latest_tnw = spread["balance_sheet"]["tangible_net_worth"][-1]
        
        # 6 Modern Glassmorphic KPI Cards
        st.markdown("<br>", unsafe_allow_html=True)
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        with k1:
            st.markdown(f'''
            <div class="kpi-tile">
                <div class="kpi-title">Audited Revenue</div>
                <div class="kpi-val">₹{latest_rev/1e7:.2f} Cr</div>
                <div class="kpi-sub"><span class="chip-safe">▲ {ratios['efficiency']['sales_growth_rate_pct'][-1]:.1f}% YoY</span></div>
            </div>
            ''', unsafe_allow_html=True)
        with k2:
            st.markdown(f'''
            <div class="kpi-tile">
                <div class="kpi-title">Tangible Net Worth</div>
                <div class="kpi-val">₹{latest_tnw/1e7:.2f} Cr</div>
                <div class="kpi-sub" style="color: #64748B;">Equity & Reserves</div>
            </div>
            ''', unsafe_allow_html=True)
        with k3:
            st.markdown(f'''
            <div class="kpi-tile">
                <div class="kpi-title">PAT Margin</div>
                <div class="kpi-val">{ratios['profitability']['pat_margin_pct'][-1]:.1f}%</div>
                <div class="kpi-sub"><span class="{'chip-safe' if ratios['profitability']['pat_margin_pct'][-1] >= 10 else 'chip-warn'}">ROCE: {ratios['profitability']['return_on_capital_employed_pct'][-1]:.1f}%</span></div>
            </div>
            ''', unsafe_allow_html=True)
        with k4:
            st.markdown(f'''
            <div class="kpi-tile">
                <div class="kpi-title">Altman Z''-Score</div>
                <div class="kpi-val">{altman_z['z_score']:.2f}</div>
                <div class="kpi-sub"><span class="{'chip-safe' if 'Safe' in altman_z['zone'] else ('chip-warn' if 'Grey' in altman_z['zone'] else 'chip-danger')}">{altman_z['zone']}</span></div>
            </div>
            ''', unsafe_allow_html=True)
        with k5:
            st.markdown(f'''
            <div class="kpi-tile">
                <div class="kpi-title">Enterprise Value</div>
                <div class="kpi-val">₹{dcf['enterprise_value']/1e7:.2f} Cr</div>
                <div class="kpi-sub" style="color: #64748B;">LTV_EV: {dcf['loan_to_enterprise_value_pct']:.1f}%</div>
            </div>
            ''', unsafe_allow_html=True)
        with k6:
            st.markdown(f'''
            <div class="kpi-tile">
                <div class="kpi-title">MSE Risk Grade</div>
                <div class="kpi-val">{mse_scorecard['grade']}</div>
                <div class="kpi-sub"><span class="chip-safe">{mse_scorecard['total_score']}/100 Marks</span></div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Diagnostic Sub-Tabs
        c_tab1, c_tab2, c_tab3, c_tab4, c_tab5, c_tab6 = st.tabs([
            "📁 3-Year CMA Statements",
            "📊 5-Pillar Diagnostics & MPBF",
            "🔍 Forensic Distress Audit",
            "🧪 3-Year Stress Simulator",
            "💎 DCF Valuation & Sizing",
            "🏛️ Form MSE 1 Scorecard"
        ])

        with c_tab1:
            col_pnl, col_bs = st.columns(2)
            with col_pnl:
                st.markdown("##### 📈 Profit & Loss Statement (₹ Lakhs)")
                pnl_df = pd.DataFrame({
                    "Line Item": ["Turnover", "COGS", "Gross Profit", "Operating Expenses", "EBITDA", "Depreciation", "EBIT", "Interest", "EBT", "Tax", "PAT", "Cash Accruals"],
                    "FY24": [spread["pnl"]["revenue"][0]/1e5, spread["pnl"]["cogs"][0]/1e5, spread["pnl"]["gross_profit"][0]/1e5, spread["pnl"]["operating_expenses"][0]/1e5, spread["pnl"]["ebitda"][0]/1e5, spread["pnl"]["depreciation"][0]/1e5, spread["pnl"]["ebit"][0]/1e5, spread["pnl"]["interest_expense"][0]/1e5, spread["pnl"]["ebt"][0]/1e5, spread["pnl"]["tax"][0]/1e5, spread["pnl"]["pat"][0]/1e5, spread["pnl"]["cash_accruals"][0]/1e5],
                    "FY25": [spread["pnl"]["revenue"][1]/1e5, spread["pnl"]["cogs"][1]/1e5, spread["pnl"]["gross_profit"][1]/1e5, spread["pnl"]["operating_expenses"][1]/1e5, spread["pnl"]["ebitda"][1]/1e5, spread["pnl"]["depreciation"][1]/1e5, spread["pnl"]["ebit"][1]/1e5, spread["pnl"]["interest_expense"][1]/1e5, spread["pnl"]["ebt"][1]/1e5, spread["pnl"]["tax"][1]/1e5, spread["pnl"]["pat"][1]/1e5, spread["pnl"]["cash_accruals"][1]/1e5],
                    "FY26": [spread["pnl"]["revenue"][2]/1e5, spread["pnl"]["cogs"][2]/1e5, spread["pnl"]["gross_profit"][2]/1e5, spread["pnl"]["operating_expenses"][2]/1e5, spread["pnl"]["ebitda"][2]/1e5, spread["pnl"]["depreciation"][2]/1e5, spread["pnl"]["ebit"][2]/1e5, spread["pnl"]["interest_expense"][2]/1e5, spread["pnl"]["ebt"][2]/1e5, spread["pnl"]["tax"][2]/1e5, spread["pnl"]["pat"][2]/1e5, spread["pnl"]["cash_accruals"][2]/1e5]
                })
                st.dataframe(pnl_df, use_container_width=True, hide_index=True)

            with col_bs:
                st.markdown("##### 🏛️ Balance Sheet (₹ Lakhs)")
                bs_df = pd.DataFrame({
                    "Component": ["Cash & Bank", "Sundry Debtors", "Inventory", "Current Assets", "Net Fixed Assets", "Total Assets", "Sundry Creditors", "Short Term Debt", "Current Liabilities", "Long Term Debt", "Paid-Up Capital", "Tangible Net Worth"],
                    "FY24": [spread["balance_sheet"]["cash_and_bank"][0]/1e5, spread["balance_sheet"]["sundry_debtors"][0]/1e5, spread["balance_sheet"]["inventory"][0]/1e5, spread["balance_sheet"]["current_assets"][0]/1e5, spread["balance_sheet"]["net_fixed_assets"][0]/1e5, spread["balance_sheet"]["total_assets"][0]/1e5, spread["balance_sheet"]["sundry_creditors"][0]/1e5, spread["balance_sheet"]["short_term_borrowings"][0]/1e5, spread["balance_sheet"]["current_liabilities"][0]/1e5, spread["balance_sheet"]["long_term_debt"][0]/1e5, spread["balance_sheet"]["paid_up_capital"][0]/1e5, spread["balance_sheet"]["tangible_net_worth"][0]/1e5],
                    "FY25": [spread["balance_sheet"]["cash_and_bank"][1]/1e5, spread["balance_sheet"]["sundry_debtors"][1]/1e5, spread["balance_sheet"]["inventory"][1]/1e5, spread["balance_sheet"]["current_assets"][1]/1e5, spread["balance_sheet"]["net_fixed_assets"][1]/1e5, spread["balance_sheet"]["total_assets"][1]/1e5, spread["balance_sheet"]["sundry_creditors"][1]/1e5, spread["balance_sheet"]["short_term_borrowings"][1]/1e5, spread["balance_sheet"]["current_liabilities"][1]/1e5, spread["balance_sheet"]["long_term_debt"][1]/1e5, spread["balance_sheet"]["paid_up_capital"][1]/1e5, spread["balance_sheet"]["tangible_net_worth"][1]/1e5],
                    "FY26": [spread["balance_sheet"]["cash_and_bank"][2]/1e5, spread["balance_sheet"]["sundry_debtors"][2]/1e5, spread["balance_sheet"]["inventory"][2]/1e5, spread["balance_sheet"]["current_assets"][2]/1e5, spread["balance_sheet"]["net_fixed_assets"][2]/1e5, spread["balance_sheet"]["total_assets"][2]/1e5, spread["balance_sheet"]["sundry_creditors"][2]/1e5, spread["balance_sheet"]["short_term_borrowings"][2]/1e5, spread["balance_sheet"]["current_liabilities"][2]/1e5, spread["balance_sheet"]["long_term_debt"][2]/1e5, spread["balance_sheet"]["paid_up_capital"][2]/1e5, spread["balance_sheet"]["tangible_net_worth"][2]/1e5]
                })
                st.dataframe(bs_df, use_container_width=True, hide_index=True)

        with c_tab2:
            st.markdown("##### 📊 5-Pillar Ratio Analysis & Working Capital Sizing (MPBF)")
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                ratio_summary_df = pd.DataFrame({
                    "Pillar": ["Liquidity", "Liquidity", "Solvency", "Solvency", "Solvency", "Profitability", "Profitability", "Efficiency"],
                    "Metric": ["Current Ratio (CR)", "Quick Ratio (QR)", "Debt-to-Equity (DER)", "TOL / TNW", "DSCR", "EBITDA Margin %", "PAT Margin %", "Cash Conversion Cycle"],
                    "FY24": [f"{ratios['liquidity']['current_ratio'][0]:.2f}", f"{ratios['liquidity']['quick_ratio'][0]:.2f}", f"{ratios['solvency']['debt_to_equity'][0]:.2f}", f"{ratios['solvency']['tol_to_tnw'][0]:.2f}", f"{ratios['solvency']['debt_service_coverage_ratio'][0]:.2f}x", f"{ratios['profitability']['ebitda_margin_pct'][0]:.1f}%", f"{ratios['profitability']['pat_margin_pct'][0]:.1f}%", f"{ratios['efficiency']['cash_conversion_cycle_days'][0]:.0f}d"],
                    "FY25": [f"{ratios['liquidity']['current_ratio'][1]:.2f}", f"{ratios['liquidity']['quick_ratio'][1]:.2f}", f"{ratios['solvency']['debt_to_equity'][1]:.2f}", f"{ratios['solvency']['tol_to_tnw'][1]:.2f}", f"{ratios['solvency']['debt_service_coverage_ratio'][1]:.2f}x", f"{ratios['profitability']['ebitda_margin_pct'][1]:.1f}%", f"{ratios['profitability']['pat_margin_pct'][1]:.1f}%", f"{ratios['efficiency']['cash_conversion_cycle_days'][1]:.0f}d"],
                    "FY26": [f"{ratios['liquidity']['current_ratio'][2]:.2f}", f"{ratios['liquidity']['quick_ratio'][2]:.2f}", f"{ratios['solvency']['debt_to_equity'][2]:.2f}", f"{ratios['solvency']['tol_to_tnw'][2]:.2f}", f"{ratios['solvency']['debt_service_coverage_ratio'][2]:.2f}x", f"{ratios['profitability']['ebitda_margin_pct'][2]:.1f}%", f"{ratios['profitability']['pat_margin_pct'][2]:.1f}%", f"{ratios['efficiency']['cash_conversion_cycle_days'][2]:.0f}d"],
                    "Benchmark": [">= 1.33", ">= 1.00", "<= 2.00", "<= 3.00", ">= 1.20x", ">= 12.0%", ">= 8.0%", "<= 90 Days"]
                })
                st.dataframe(ratio_summary_df, use_container_width=True, hide_index=True)

            with r_col2:
                st.markdown("##### 💼 Working Capital Sizing (MPBF)")
                mpbf = ratios["mpbf_working_capital"]
                st.info(f"• **Tandon Method I:** ₹{mpbf['tandon_method_1']/1e5:,.2f} Lakhs\n• **Tandon Method II:** ₹{mpbf['tandon_method_2']/1e5:,.2f} Lakhs\n• **Nayak Turnover Model (20%):** ₹{mpbf['nayak_turnover_method']/1e5:,.2f} Lakhs\n• 🏦 **Recommended Limit:** **₹{mpbf['recommended_limit']/1e5:,.2f} Lakhs**")

        with c_tab3:
            st.markdown("##### 🔍 Forensic Accounting & Early Warning Distress Indicators")
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                st.markdown(f"**Altman Z''-Score:** `{altman_z['z_score']:.2f}` — Status: **{altman_z['zone'].upper()}**")
                st.caption(f"{altman_z['risk_level']}")
            with f_col2:
                st.markdown(f"**Beneish M-Score:** `{beneish_m['m_score']:.2f}` — Threshold: `-1.78`")
                st.caption(f"{beneish_m['risk_assessment']}")

        with c_tab4:
            st.markdown("##### 🧪 Macro Stress Testing Simulator")
            shock_rev = st.slider("Revenue Shock (%):", -40, 10, -20, 5)
            shock_cogs = st.slider("COGS Inflation (%):", 0, 30, 15, 5)
            shock_rate = st.slider("Interest Rate Spike (bps):", 0, 400, 200, 50)
            
            stress_res = FinancialForecaster.simulate_stress_scenario(spread, shock_rev/100.0, shock_cogs/100.0, shock_rate)
            st.markdown(f"• **Stressed DSCR:** `{stress_res['stressed_dscr']:.2f}x` | **Solvency Verdict:** **{stress_res['solvency_status']}**")

        with c_tab5:
            st.markdown("##### 💎 Discounted Cash Flow (DCF) Valuation & Debt Capacity")
            st.markdown(f"• **Enterprise Value:** ₹{dcf['enterprise_value']/1e7:,.2f} Cr\n• **Equity Value:** ₹{dcf['equity_value']/1e7:,.2f} Cr\n• **Loan-to-Enterprise Value (LTV_EV):** `{dcf['loan_to_enterprise_value_pct']:.1f}%` ({dcf['leverage_assessment']})")

        with c_tab6:
            st.markdown(f"##### 🏛️ Central Bank Form MSE 1 Auto-Populated Scorecard (Grade: {mse_scorecard['grade']})")
            rows = []
            scorecard_items = mse_scorecard.get("parameter_scores") or mse_scorecard.get("breakdown") or []
            for item in scorecard_items:
                param_name = item.get("param") or item.get("parameter") or "Parameter"
                score_val = item.get("score", 0)
                max_score_val = item.get("max") or item.get("max_score") or 10
                diag_val = item.get("value") or item.get("description") or ""
                rows.append({"Parameter": param_name, "Score Awarded": score_val, "Max Marks": max_score_val, "Diagnostic Benchmark / Metric": diag_val})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Push This Corporate Profile to Loan Application Form", type="primary", use_container_width=True):
            st.session_state.ocr_data = {
                "name": raw_corp_data["company_name"],
                "age": 45, "gender": "Male", "marital_status": "Married", "category": "GEN", "occupation": "Business",
                "gross_monthly_income": int(latest_rev / 12),
                "net_monthly_income": int(latest_pat / 12),
                "total_assets": int(spread["balance_sheet"]["total_assets"][-1]),
                "credit_score": int(credit_score),
                "avg_credit_balance_6m": int(spread["balance_sheet"]["cash_and_bank"][-1]),
                "existing_emi": int(spread["pnl"]["interest_expense"][-1] / 12),
                "active_lines": 3, "inquiries_6m": 0,
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
        st.markdown("### 🛡️ Credit Underwriting Management & Portfolio Control")
        
        manager_tab1, manager_tab2, manager_tab3 = st.tabs([
            "🔴 Active Underwriting Pipeline", 
            "📊 Executive Portfolio Analytics & Risk Intelligence", 
            "📂 Complete Application History & Overrides"
        ])
        
        # MANAGER TAB 1: PIPELINE
        with manager_tab1:
            st.markdown("##### ⚡ Human-In-The-Loop (HITL) Review Queue")
            try:
                pending_res = requests.get(f"{API_BASE_URL}/pending").json()
                if pending_res and len(pending_res) > 0:
                    st.info(f"You have **{len(pending_res)} application(s)** awaiting credit manager review.")
                    pending_df = pd.DataFrame(pending_res)
                    pending_df['loan_amount'] = pending_df['loan_amount'].apply(lambda x: f"₹{x:,.2f}")
                    st.dataframe(pending_df, use_container_width=True, hide_index=True)
                    
                    selected_pending = st.selectbox("Select Application ID to Review:", pending_df['thread_id'])
                    if st.button("Load Selected Application"):
                        st.session_state.thread_id = selected_pending
                        res = requests.get(f"{API_BASE_URL}/status/{selected_pending}").json()
                        st.session_state.latest_result = res
                        st.rerun()
                else:
                    st.success("No applications are currently awaiting manager approval.")
            except Exception as e:
                st.error(f"Failed to load pipeline: {e}")

            if st.session_state.latest_result:
                result = st.session_state.latest_result
                st.markdown("---")
                st.markdown(f"#### 📄 Application Review: `{st.session_state.thread_id}`")
                
                # Top Status Badge
                dec = result.get('decision_outcome', 'PENDING')
                st.markdown(f'''
                <div style="background: {'#ECFDF5' if 'APPROV' in str(dec).upper() else '#FEF2F2'}; border: 1px solid {'#A7F3D0' if 'APPROV' in str(dec).upper() else '#FECACA'}; padding: 12px 16px; border-radius: 8px; margin-bottom: 14px;">
                    <strong>System Recommendation:</strong> <span style="font-weight: 800; color: {'#059669' if 'APPROV' in str(dec).upper() else '#DC2626'};">{dec}</span>
                </div>
                ''', unsafe_allow_html=True)
                
                # Detailed Report Viewer inside Executive Canvas
                detailed_rep = result.get("detailed_report", "")
                if detailed_rep:
                    with st.expander("📑 View Full Credit Appraisal Memorandum (Chapter 1 to 7)", expanded=True):
                        st.markdown(f'<div class="memo-canvas">{detailed_rep}</div>', unsafe_allow_html=True)
                        docx_bytes = utils.generate_docx(detailed_rep)
                        st.download_button("📄 Download Official Word (.docx) Memorandum", docx_bytes, "Appraisal_Memorandum.docx", type="primary")

                if result.get("status") == "WAITING_FOR_MANAGER":
                    st.markdown("---")
                    st.markdown("##### ✍️ Final Manager Decision & Action")
                    col_a, col_b = st.columns(2)
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

        # MANAGER TAB 2: PORTFOLIO ANALYTICS
        with manager_tab2:
            st.markdown("##### 📊 Executive Portfolio Analytics & Risk Concentration")
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
                    
                    col_scope1, col_scope2 = st.columns([3, 1])
                    with col_scope1:
                        analytics_scope = st.radio(
                            "Select Portfolio Scope:",
                            ["🟢 Sanctioned Book (Approved Only)", "🌐 Full Pipeline (All Applications)"],
                            horizontal=True
                        )
                    with col_scope2:
                        if st.button("🔄 Refresh", use_container_width=True):
                            st.rerun()

                    df_view = df_p[df_p["is_approved"]] if "Sanctioned Book" in analytics_scope else df_p
                    scope_lbl = "Sanctioned Advances" if "Sanctioned Book" in analytics_scope else "Underwriting Pipeline"

                    # KPI Counters
                    tot_exp = df_view["loan_amount"].sum() if not df_view.empty else 0.0
                    avg_cibil = df_view["credit_score"].mean() if not df_view.empty else 0.0
                    avg_roi = df_view["official_roi"].mean() if not df_view.empty else 0.0
                    
                    pk1, pk2, pk3, pk4 = st.columns(4)
                    pk1.metric("Active Book Volume", f"₹{tot_exp/1e7:.2f} Cr", help="Total exposure")
                    pk2.metric("Portfolio Facilities", f"{len(df_view)}", help="Active advances count")
                    pk3.metric("Weighted Avg CIBIL", f"{avg_cibil:.0f}", help="Average bureau standing")
                    pk4.metric("Weighted Avg Lending Rate", f"{avg_roi:.2f}%", help="Pegged to RBLR")

                    st.markdown("<br>", unsafe_allow_html=True)
                    c_chart1, c_chart2 = st.columns(2)
                    with c_chart1:
                        msme_df = df_view[df_view["cbi_grade"] != "N/A"]
                        if not msme_df.empty:
                            fig_bar = px.bar(msme_df["cbi_grade"].value_counts().reset_index(), x="cbi_grade", y="count", title=f"Risk Grade Distribution ({scope_lbl})", color="cbi_grade", color_discrete_sequence=px.colors.qualitative.Bold)
                            fig_bar.update_layout(height=340, margin=dict(l=10, r=10, t=35, b=10))
                            st.plotly_chart(fig_bar, use_container_width=True)
                    with c_chart2:
                        if not df_view.empty:
                            fig_pie = px.pie(df_view, values="loan_amount", names="loan_type", hole=0.45, title=f"Exposure Allocation by Product ({scope_lbl})")
                            fig_pie.update_layout(height=340, margin=dict(l=10, r=10, t=35, b=10))
                            st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("No applications in database yet.")
            except Exception as e:
                st.error(f"Error loading analytics: {e}")

        # MANAGER TAB 3: HISTORY & OVERRIDES
        with manager_tab3:
            st.markdown("##### 📂 Application Database & Audit Override Log")
            try:
                hist_res = requests.get(f"{API_BASE_URL}/history").json()
                if hist_res and isinstance(hist_res, list) and len(hist_res) > 0:
                    h_df = pd.DataFrame(hist_res)
                    h_df['created_at'] = pd.to_datetime(h_df['created_at'])
                    h_df['loan_amount'] = h_df['loan_amount'].apply(lambda x: f"₹{x:,.2f}")
                    st.dataframe(h_df[['created_at', 'thread_id', 'applicant_name', 'loan_amount', 'risk_category', 'decision']], use_container_width=True, hide_index=True)
                    
                    st.markdown("---")
                    selected_thread = st.selectbox("Select Application ID to Inspect:", h_df['thread_id'])
                    if selected_thread:
                        row = h_df[h_df['thread_id'] == selected_thread].iloc[0]
                        rep_show = row.get('detailed_report')
                        if rep_show:
                            with st.expander(f"📑 View Complete Memorandum ({row['applicant_name']})", expanded=True):
                                st.markdown(f'<div class="memo-canvas">{rep_show}</div>', unsafe_allow_html=True)
                                docx_b = utils.generate_docx(rep_show)
                                st.download_button("📄 Download Official Memorandum (.docx)", docx_b, f"Memo_{selected_thread}.docx")
                else:
                    st.info("No applications found in database.")
            except Exception as e:
                st.error(f"Failed to fetch history: {e}")
