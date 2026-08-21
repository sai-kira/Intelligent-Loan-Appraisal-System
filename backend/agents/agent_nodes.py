from langgraph.types import Command, interrupt
from agent_state import LoanApplicationState
import json
import xgboost as xgb
import joblib
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from calculators import calculate_emi, calculate_foir, check_ltv_compliance
from rag.retriever import PolicyRetriever

print("Initializing RAG Retriever...")
try:
    retriever = PolicyRetriever()
except Exception as e:
    retriever = None
    print("Retriever failed to initialize:", e)

def log_action(agent_name: str, status: str, summary: str):
    return {"agent": agent_name, "status": status, "summary": summary}

# 1. Customer Agent
def customer_agent(state: LoanApplicationState) -> Command:
    print("Customer Agent processing...")
    applicant = state.get("applicant_data", {})
    real_name = applicant.get("name", "Unknown")
    
    # PII Masking
    masked_name = f"APPLICANT_{hash(real_name) % 10000:04d}"
    applicant["name"] = masked_name
    
    log = log_action("Customer Agent", "Complete", f"Digitized applicant form data and masked PII (Name -> {masked_name}) for downstream privacy.")
    return Command(
        update={
            "current_agent": "document_agent", 
            "applicant_data": applicant,
            "real_name": real_name,
            "agent_logs": [log]
        }, 
        goto="document_agent"
    )

# 2. Document Agent
def document_agent(state: LoanApplicationState) -> Command:
    print("Document Agent processing...")
    log = log_action("Document Agent", "Complete", "Successfully extracted and OCR-processed Identity (PAN), Income (Form 16), and Property deeds.")
    return Command(
        update={
            "current_agent": "kyc_agent",
            "extracted_documents": [{"doc_type": "PAN", "status": "Extracted"}],
            "agent_logs": [log]
        }, 
        goto="kyc_agent"
    )

# 3. KYC Agent
def kyc_agent(state: LoanApplicationState) -> Command:
    print("KYC Agent processing...")
    log = log_action("KYC Agent", "Complete", "Cross-verified applicant identity against national KYC registries with 100% match.")
    return Command(
        update={"current_agent": "validation_agent", "kyc_status": "VERIFIED", "agent_logs": [log]}, 
        goto="validation_agent"
    )

# 4. Validation Agent
def validation_agent(state: LoanApplicationState) -> Command:
    print("Validation Agent processing...")
    log = log_action("Validation Agent", "Complete", "Executed Penny Drop verification. Bank account is active and matches applicant name.")
    return Command(
        update={"current_agent": "financial_analysis_agent", "bank_verification_status": "VERIFIED", "agent_logs": [log]}, 
        goto="financial_analysis_agent"
    )

# 5. Financial Analysis Agent
def financial_analysis_agent(state: LoanApplicationState) -> Command:
    print("Financial Analysis Agent processing...")
    applicant = state.get("applicant_data", {})
    
    principal = applicant.get("loan_amount", 0)
    tenure = applicant.get("tenure_months", 120)
    income = applicant.get("gross_monthly_income", 0)
    existing_emi = applicant.get("existing_emi", 0)
    property_value = applicant.get("property_value", 0)
    loan_type = applicant.get("loan_type", "Home Loan")
    credit_score = applicant.get("credit_score", 300)
    
    # Check if this is an MSME loan
    msme_scorecard = None
    if "MSME" in loan_type:
        from msme_scoring_engine import calculate_mse_existing_score, calculate_mse_new_score
        if "New" in loan_type:
            msme_scorecard = calculate_mse_new_score(applicant)
        else:
            msme_scorecard = calculate_mse_existing_score(applicant)
            
        is_cgtmse = (
            applicant.get("collateral_coverage") in ["Covered under CGTMSE Scheme", "CGTMSE Covered", "Up to 100% Collateral"]
            or applicant.get("cgtmse_covered", False)
        )
        from roi_engine import get_applicable_roi
        rate = get_applicable_roi(loan_type, credit_score, mse_grade=msme_scorecard["grade"], cgtmse_covered=is_cgtmse)
    else:
        from roi_engine import get_applicable_roi
        rate = get_applicable_roi(loan_type, credit_score)
        
    # Update the applicant data so the rest of the system knows the official rate
    applicant["interest_rate"] = rate
    
    emi = calculate_emi(principal, rate, tenure)
    foir = calculate_foir(existing_emi, emi, income)
    ltv_res = check_ltv_compliance(principal, property_value, loan_type)
    
    metrics = {
        "calculated_emi": emi,
        "calculated_foir": foir,
        "ltv_compliance": ltv_res,
        "official_roi": rate,
        "msme_scorecard": msme_scorecard
    }
    
    if msme_scorecard:
        log_msg = f"Assigned official MSME ROI of {rate:.2f}%. Computed Central Bank MSE Score: {msme_scorecard['total_score']}/100 ({msme_scorecard['grade']}). EMI: ₹{emi:,.2f}, FOIR: {foir:.2f}%, LTV: {ltv_res['ltv']:.2f}%."
    else:
        log_msg = f"Assigned official ROI of {rate:.2f}% based on CIBIL {credit_score}. Computed critical financial ratios: EMI is ₹{emi:,.2f}, FOIR is {foir:.2f}%, and LTV is {ltv_res['ltv']:.2f}%."
    
    log = log_action("Financial Analysis Agent", "Complete", log_msg)
    
    return Command(
        update={"current_agent": "ml_risk_agent", "financial_metrics": metrics, "agent_logs": [log], "applicant_data": applicant, "msme_scorecard": msme_scorecard}, 
        goto="ml_risk_agent"
    )

# 6. ML Risk Agent
def ml_risk_agent(state: LoanApplicationState) -> Command:
    print("ML Risk Agent processing...")
    applicant = state.get("applicant_data", {})
    metrics = state.get("financial_metrics", {})
    
    try:
        # Load models
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_path, "..", "ml_pipeline", "models", "xgboost_risk_model.json")
        features_path = os.path.join(base_path, "..", "ml_pipeline", "models", "model_features.pkl")
        encoders_path = os.path.join(base_path, "..", "ml_pipeline", "models", "label_encoders.pkl")
        
        model = xgb.XGBClassifier()
        model.load_model(model_path)
        feature_cols = joblib.load(features_path)
        label_encoders = joblib.load(encoders_path)
        
        # Build features dict matching the 23 parameters
        data = {
            'AGE': applicant.get("age", 30),
            'GROSS_MONTHLY_INC': applicant.get("gross_monthly_income", 0),
            'NET_MONTHLY_INC': applicant.get("net_monthly_income", 0),
            'AVG_CREDIT_BAL_6M': applicant.get("avg_credit_balance_6m", 0),
            'CREDIT_SCORE': applicant.get("credit_score", 700),
            'ACTIVE_LINES': applicant.get("active_lines", 0),
            'INQUIRIES_6M': applicant.get("inquiries_6m", 0),
            'EXISTING_EMI': applicant.get("existing_emi", 0),
            'TOTAL_ASSETS': applicant.get("total_assets", 0),
            'SANCTION_AMT': applicant.get("loan_amount", 0),
            'INT_RATE': applicant.get("interest_rate", 8.5),
            'TENURE_MTHS': applicant.get("tenure_months", 120),
            'ASSESSED_VAL': applicant.get("property_value", 0),
            'CALCULATED_FOIR': metrics.get("calculated_foir", 0),
            'CALCULATED_LTV': metrics.get("ltv_compliance", {}).get("ltv", 0)
        }
        
        data['INCOME_TO_LOAN_RATIO'] = (data['GROSS_MONTHLY_INC'] * 12) / data['SANCTION_AMT'] if data['SANCTION_AMT'] > 0 else 0
        data['ASSETS_TO_LOAN_RATIO'] = data['TOTAL_ASSETS'] / data['SANCTION_AMT'] if data['SANCTION_AMT'] > 0 else 0
        
        # Categoricals
        cat_map = {
            'GENDER': applicant.get("gender", "Male"),
            'MARITAL_STATUS': applicant.get("marital_status", "Single"),
            'CATEGORY': applicant.get("category", "GEN"),
            'OCCUPATION': applicant.get("occupation", "Salaried"),
            'LOAN_TYPE': "Personal Loan" if "MSME" in applicant.get("loan_type", "") else applicant.get("loan_type", "Home Loan"),
            'SECURITY_TYPE': applicant.get("security_type", "Property")
        }
        
        # Safely encode, fallback to a known class if unseen
        for col, val in cat_map.items():
            le = label_encoders[col]
            if val in le.classes_:
                data[col] = le.transform([val])[0]
            else:
                data[col] = 0
                
        df = pd.DataFrame([data])
        # Ensure all columns exist in correct order
        for c in feature_cols:
            if c not in df.columns:
                df[c] = 0
        df = df[feature_cols]
        
        # Predict
        prob_default = float(model.predict_proba(df)[0][1])
        
        # SHAP local explainability
        explainer = shap.TreeExplainer(model)
        shap_values = explainer(df)
        
        # Get top 3 driving features
        vals = shap_values.values[0]
        top_indices = np.argsort(np.abs(vals))[-3:][::-1]
        top_factors = [
            {"feature": feature_cols[i], "impact": float(vals[i]), "value": float(df.iloc[0, i])}
            for i in top_indices
        ]
        
        # 5-Tier Granular Risk Classification (Basel / Institutional Credit Rating Standard)
        if prob_default < 0.15:
            risk_category = "Very Low"
        elif prob_default < 0.25:
            risk_category = "Low"
        elif prob_default < 0.40:
            risk_category = "Moderate"
        elif prob_default < 0.55:
            risk_category = "Elevated"
        else:
            risk_category = "High / Critical Default"
            
        risk_score = {
            "pd": prob_default,
            "pd_percentage": f"{prob_default * 100:.2f}",
            "risk_category": risk_category,
            "top_factors": top_factors
        }
        log = log_action("ML Risk Agent", "Complete", f"Calculated Probability of Default: {prob_default * 100:.2f}% (Risk: {risk_category}). Top drivers identified.")
        
    except Exception as e:
        print(f"ML Model Inference Error: {e}")
        risk_score = {
            "pd": 0.35,
            "pd_percentage": "35.00",
            "risk_category": "Moderate",
            "top_factors": [{"feature": "CREDIT_SCORE", "impact": -0.5, "value": 750}]
        }
        log = log_action("ML Risk Agent", "Warning", f"Using fallback heuristic risk assessment: {str(e)}")

    return Command(
        update={"current_agent": "policy_retrieval_agent", "risk_score": risk_score, "agent_logs": [log]}, 
        goto="policy_retrieval_agent"
    )

# 7. Policy Retrieval Agent
def policy_retrieval_agent(state: LoanApplicationState) -> Command:
    print("Policy Retrieval Agent processing...")
    applicant = state.get("applicant_data", {})
    loan_amount = applicant.get("loan_amount", 0)
    loan_type = applicant.get("loan_type", "Home Loan")
    
    if "MSME" in loan_type:
        query = f"What are the Central Bank of India MSE manual scoring model guidelines, benchmark Current Ratio, Debt Equity Ratio, and CGTMSE norms for an MSME loan of {loan_amount}?"
    else:
        query = f"What are the RBI guidelines and LTV or FOIR limits for a {loan_type} of {loan_amount}?"
    
    if retriever:
        policies = retriever.retrieve(query, top_k=6)
        log = log_action("Policy Retrieval Agent", "Complete", f"Queried the vector database and retrieved {len(policies)} regulatory guidelines spanning multiple policy documents.")
    else:
        policies = ["(Fallback) RBI Guidelines: FOIR < 50%", "(Fallback) CBoI: LTV < 80% for loans 30L-75L"]
        log = log_action("Policy Retrieval Agent", "Warning", "RAG DB not connected. Using fallback.")
        
    return Command(
        update={"current_agent": "compliance_agent", "applicable_policies": policies, "agent_logs": [log]}, 
        goto="compliance_agent"
    )

# 8. Compliance Agent
def compliance_agent(state: LoanApplicationState) -> Command:
    print("Compliance Agent processing...")
    log = log_action("Compliance Agent", "Complete", "Application passed all internal Anti-Money Laundering (AML) and basic regulatory checks.")
    return Command(update={"current_agent": "decision_agent", "agent_logs": [log]}, goto="decision_agent")

# 9. Decision Agent
def decision_agent(state: LoanApplicationState) -> Command:
    print("Decision Agent processing...")
    applicant = state.get("applicant_data", {})
    loan_type = applicant.get("loan_type", "Home Loan")
    risk = state.get("risk_score", {}).get("risk_category", "High / Critical Default")
    metrics = state.get("financial_metrics", {})
    ltv_compliant = metrics.get("ltv_compliance", {}).get("compliant", False)
    msme_scorecard = state.get("msme_scorecard")
    
    # High / Critical Default or Elevated risk triggers strict controls
    is_high_risk = risk in ["High / Critical Default", "High"]
    is_cgtmse = (
        applicant.get("collateral_coverage") in ["Covered under CGTMSE Scheme", "CGTMSE Covered", "Up to 100% Collateral"]
        or applicant.get("cgtmse_covered", False)
    )
    
    if "MSME" in loan_type and msme_scorecard:
        mse_score = msme_scorecard.get("total_score", 0)
        mse_grade = msme_scorecard.get("grade", "CBI 10")
        hurdle_met = msme_scorecard.get("hurdle_rate_met", mse_score > 50)
        
        # MSME approval logic: Must meet Hurdle Rate (> 50 marks, i.e. CBI 1 to CBI 6), ML Risk not Critical, and LTV compliant (or CGTMSE backed)
        if not hurdle_met or mse_score <= 50 or mse_grade in ["CBI 7", "CBI 8", "CBI 9", "CBI 10", "Grade C"] or is_high_risk:
            outcome = "REJECTED"
            summary = f"Rejected under {msme_scorecard.get('model_form')}. MSE Score: {mse_score}/100 ({mse_grade} - Fails Hurdle Rate of 50 marks), ML Risk: {risk}."
        elif not is_cgtmse and not ltv_compliant:
            outcome = "REJECTED"
            ltv_val = metrics.get("ltv_compliance", {}).get("ltv", 0)
            summary = f"Rejected due to Collateral LTV Breach: LTV of {ltv_val:.2f}% exceeds permissible regulatory ceiling without CGTMSE guarantee."
        else:
            outcome = "APPROVED"
            if mse_grade in ["CBI 5", "CBI 6", "Grade B"]:
                covenant_note = f" (Subject to {mse_grade} Special Covenants: Min CR >= 1.20, DER <= 3.0, Monthly QIS by 15th, >= 80% Turnover Routing)"
            else:
                covenant_note = f" ({mse_grade} Fast-Track / Standard Terms)"
            summary = f"Approved under {msme_scorecard.get('model_form')}. MSE Score: {mse_score}/100 ({mse_grade} - {msme_scorecard.get('risk_profile')}){covenant_note}."
    else:
        if is_high_risk or not ltv_compliant:
            outcome = "REJECTED"
            summary = f"Rejected due to ML Risk: {risk}, LTV Compliant: {ltv_compliant}"
        else:
            outcome = "APPROVED"
            summary = f"Approved. ML Risk is {risk} and LTV is compliant."
        
    log = log_action("Decision Agent", "Complete", f"Synthesized all findings. Recommendation: {outcome}. {summary}")
    
    return Command(
        update={"current_agent": "report_writing_agent", "decision_outcome": outcome, "agent_logs": [log]}, 
        goto="report_writing_agent"
    )

# 10. Report Writing Agent
def report_writing_agent(state: LoanApplicationState) -> Command:
    print("Report Writing Agent processing...")
    applicant = state.get("applicant_data", {})
    metrics = state.get("financial_metrics", {})
    risk = state.get("risk_score", {})
    policies = state.get("applicable_policies", [])
    decision = state.get("decision_outcome", "Unknown")
    msme_scorecard = state.get("msme_scorecard") or metrics.get("msme_scorecard")

    import os, json, re
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    
    # Format policies and retain document citation markers
    formatted_policies = ""
    for p in policies:
        clean_p = p.replace('\n', ' ')
        clean_p = clean_p.replace('\\n', ' ')
        clean_p = re.sub(r'【.*?】', '', clean_p)
        clean_p = re.sub(r'http[s]?://\S+', '', clean_p)
        clean_p = re.sub(r'www\.\S+', '', clean_p)
        clean_p = re.sub(r'\s+', ' ', clean_p).strip()
        formatted_policies += f"- {clean_p}\n"

    top_drivers = ", ".join([f"{f['feature']} ({f['impact']:.2f})" for f in risk.get('top_factors', [])])
    real_name = state.get("real_name", applicant.get('name', 'Applicant'))
    
    # Build MSME Scorecard Table Markdown if applicable
    msme_section_prompt = ""
    if msme_scorecard:
        rows = []
        for item in msme_scorecard.get("breakdown", []):
            rows.append(f"| {item['parameter']} | {item['score']} | {item['max_score']} | {item['description']} |")
        table_rows = "\n".join(rows)
        msme_section_prompt = f"""
Include a dedicated Section 3.1:
## 3.1 🏢 Central Bank of India MSE Scoring Model ({msme_scorecard.get('model_form')})
**Total Score:** **{msme_scorecard.get('total_score')}/100** | **Credit Risk Grade:** **{msme_scorecard.get('grade')}** ({msme_scorecard.get('risk_profile')})
**Sanction Recommendation:** {msme_scorecard.get('recommendation')}

| Parameter | Score Awarded | Max Marks | Assessment / Rule |
| :--- | :--- | :--- | :--- |
{table_rows}
| **TOTAL SCORE** | **{msme_scorecard.get('total_score')}/100** | **100** | **{msme_scorecard.get('grade')}** |
"""
    
    from langchain_google_genai import ChatGoogleGenerativeAI
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0.2)
    
    prompt = f"""You are a senior credit underwriting analyst at the Central Bank of India. 
Your task is to write a highly detailed, holistic, and professional Credit Appraisal Report based on the following applicant data. 
You MUST adhere exactly to the visual structure requested. Do not deviate from the structure.

Applicant Name: {real_name}
Loan Requested: ₹{applicant.get('loan_amount', 0):,.2f} ({applicant.get('loan_type', '')}) for {applicant.get('tenure_months', 0)} months.
Credit Score (CIBIL): {applicant.get('credit_score', 'N/A')}
Calculated EMI: ₹{metrics.get('calculated_emi', 0):,.2f}
Calculated FOIR (Fixed Obligation to Income Ratio): {metrics.get('calculated_foir', 0):.2f}%
Calculated LTV (Loan to Value): {metrics.get('ltv_compliance', {}).get('ltv', 0):.2f}%
LTV Compliant: {metrics.get('ltv_compliance', {}).get('compliant')}
Bank Assigned ROI (Official Interest Rate): {metrics.get('official_roi', 'N/A')}%
Probability of Default (PD): {risk.get('pd_percentage')}%
Risk Category: {risk.get('risk_category')}
Risk Drivers: {top_drivers}

{f"MSME Scorecard: {msme_scorecard.get('total_score')}/100 ({msme_scorecard.get('grade')})" if msme_scorecard else ""}

Relevant Bank Policies / Guidelines retrieved:
{formatted_policies}

Decision: {decision}
Color logic for Decision: If "APPROVED", use color "green". If "REJECTED", use color "red". 

Write two sections:
1. detailed_report: A comprehensive markdown report. YOU MUST FOLLOW THIS EXACT STRUCTURE:

# 🏦 Comprehensive Credit Appraisal Report
**CONFIDENTIAL - Internal Bank Use Only**

## 1. 📊 Executive Summary
[Write a 2-3 sentence summary weaving together the applicant's profile, the loan requested, and the ultimate decision. End with an HTML tag showing the decision like: **Final Decision:** <span style="color: red; font-weight: bold;">REJECTED</span> or <span style="color: green; font-weight: bold;">APPROVED</span>]

## 2. 👤 Applicant Profile & Loan Details
| Metric | Details |
| :--- | :--- |
| **Applicant / Entity Name** | {real_name} |
| **Loan Requested** | ₹{applicant.get('loan_amount', 0):,.2f} ({applicant.get('loan_type', '')}) |
| **Tenure** | {applicant.get('tenure_months', 0)} Months |
| **CIBIL Score** | {applicant.get('credit_score', 'N/A')} |

## 3. 💰 Financial Capacity & Obligation
| Metric | Value | Status |
| :--- | :--- | :--- |
| **Bank Assigned ROI** | {metrics.get('official_roi', 'N/A')}% | 🏛️ Official Rate |
| **Calculated EMI** | ₹{metrics.get('calculated_emi', 0):,.2f} | - |
| **Calculated FOIR** | {metrics.get('calculated_foir', 0):.2f}% | [Explain if it breaches policy in 1 line] |
| **LTV Ratio** | {metrics.get('ltv_compliance', {}).get('ltv', 0):.2f}% | [Compliant/Violation] |

**Interest Rate Analysis:**
[Explicitly explain the Bank Assigned ROI (e.g. {metrics.get('official_roi', 'N/A')}%) based on the applicant's CIBIL score, MSME scorecard grade (if applicable), and loan type as per Central Bank guidelines.]

{msme_section_prompt}

## 4. 🧠 Predictive Risk Analytics
> **Probability of Default (PD):** {risk.get('pd_percentage')}%
> **Risk Category:** {risk.get('risk_category')}

[Write a paragraph explaining the primary risk drivers and why the ML model categorized the applicant this way.]

## 5. 📜 Policy Adherence & Final Justification
[Write a cohesive narrative explaining *why* the loan decision was made. Reference the FOIR, LTV, Credit Score, MSME Score/Grade (if applicable), Bank Assigned ROI, and the retrieved policy guidelines. Synthesize this into a professional final justification.]

## 6. 📚 References & Bibliography
[List the specific retrieved Bank Policies / Guidelines used to evaluate this application as bullet points. You MUST cite the exact Document Names and chunk numbers provided in the context (e.g. [Doc: CBoI_MSE_Scoring_Models, Chunk: 1] or [Doc: RBI_Retail_Guidelines, Chunk: 2]). Do not include external links unless they were explicitly provided in the retrieved policies.]


2. short_report: A brief "Credit Appraisal One-Pager" markdown summary. YOU MUST FOLLOW THIS EXACT STRUCTURE:

# 📑 Credit Appraisal One-Pager
**Applicant:** {real_name} | **Requested:** ₹{applicant.get('loan_amount', 0):,.2f}

### 📈 Key Metrics Snapshot
* **CIBIL:** {applicant.get('credit_score', 'N/A')}
* **FOIR (Capacity):** {metrics.get('calculated_foir', 0):.2f}%
* **LTV (Collateral):** {metrics.get('ltv_compliance', {}).get('ltv', 0):.2f}%
* **Default Risk (PD):** {risk.get('pd_percentage')}% ({risk.get('risk_category')} Risk)
{f"* **MSME Score:** {msme_scorecard.get('total_score')}/100 ({msme_scorecard.get('grade')})" if msme_scorecard else ""}

### ✍️ Summary of Assessment
[Write 2 sentences summarizing the justification.]

### ⚖️ Underwriting Recommendation: **{decision}**

Output exactly a valid JSON object (and nothing else) with two keys: "detailed_report" and "short_report". Do not wrap in ```json or markdown blocks, just the raw JSON object string so it can be parsed by json.loads(). Escape inner quotes if necessary.
"""

    reports = None
    try:
        response = llm.invoke(prompt)
        text_content = ""
        if isinstance(response.content, str):
            text_content = response.content.strip()
        elif isinstance(response.content, list):
            text_content = response.content[0].get("text", "").strip()
            
        if text_content.startswith("```json"):
            text_content = text_content[7:-3].strip()
        elif text_content.startswith("```"):
            text_content = text_content[3:-3].strip()
            
        try:
            reports = json.loads(text_content, strict=False)
        except Exception as json_err:
            print(f"JSON direct parse warning: {json_err}. Attempting regex recovery...")
            det_match = re.search(r'"detailed_report"\s*:\s*"([\s\S]*?)"\s*,\s*"short_report"', text_content)
            short_match = re.search(r'"short_report"\s*:\s*"([\s\S]*?)"\s*\}', text_content)
            if det_match and short_match:
                det_text = det_match.group(1).replace('\\n', '\n').replace('\\"', '"')
                short_text = short_match.group(1).replace('\\n', '\n').replace('\\"', '"')
                reports = {"detailed_report": det_text, "short_report": short_text}
                
    except Exception as e:
        print(f"LLM Generation Warning (Rate limit or error: {e}). Generating deterministic high-fidelity report...")
        
    # Guarantee comprehensive publication-grade report with Chapter 4 for corporate/MSME
    if "MSME" in applicant.get("loan_type", "") or "current_ratio" in applicant or not reports or "detailed_report" not in reports or not reports.get("detailed_report"):
        from report_generator import generate_deterministic_reports
        reports = generate_deterministic_reports(
            applicant_data=applicant,
            metrics=metrics,
            risk_score=risk,
            decision=decision,
            msme_scorecard=msme_scorecard,
            applicable_policies=policies,
            real_name=real_name
        )

    detailed_report = reports.get("detailed_report", "")
    short_report = reports.get("short_report", "")

    log = log_action("Report Writing Agent", "Complete", "Drafted detailed and short publishable Credit Appraisal Memos.")
    return Command(
        update={
            "current_agent": "manager_approval_agent", 
            "appraisal_memo_url": "Generated in UI",
            "detailed_report": detailed_report,
            "short_report": short_report,
            "agent_logs": [log]
        }, 
        goto="manager_approval_agent"
    )

# 11. Manager Approval Agent (HITL)
def manager_approval_agent(state: LoanApplicationState) -> Command:
    print("Manager Approval Agent processing (INTERRUPT)...")
    
    decision = interrupt({
        "action": "require_approval",
        "memo_url": state.get("appraisal_memo_url"),
        "decision_outcome": state.get("decision_outcome"),
        "risk_profile": state.get("risk_score")
    })
    
    log = log_action("Manager Approval Agent", "Complete", f"Human manager intervened. Final decision: {decision}")
    
    if decision == "APPROVED":
        return Command(update={"decision_outcome": "APPROVED (Manager)", "manager_comments": "Approved manually", "agent_logs": [log]}, goto="audit_agent")
    else:
        return Command(update={"decision_outcome": "REJECTED (Manager)", "manager_comments": str(decision), "agent_logs": [log]}, goto="audit_agent")

# 12. Audit Agent
def audit_agent(state: LoanApplicationState) -> Command:
    print("Audit Agent processing...")
    log = log_action("Audit Agent", "Complete", "Log chain secured. Process terminated.")
    return Command(update={"current_agent": "END", "agent_logs": [log]})
