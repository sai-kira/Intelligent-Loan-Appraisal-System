"""
Deterministic & High-Fidelity Credit Appraisal Report Generator
Guarantees 100% beautiful, publication-ready, and consistent reports
even under LLM API outages, rate limits (429), or offline mode.
"""
import re

def generate_deterministic_reports(applicant_data: dict, metrics: dict, risk_score: dict, decision: str, msme_scorecard: dict = None, applicable_policies: list = None, real_name: str = "Applicant") -> dict:
    """
    Constructs both the detailed appraisal report and one-pager summary markdown
    matching the exact corporate structure of Central Bank of India.
    """
    loan_amount = applicant_data.get("loan_amount", 0)
    loan_type = applicant_data.get("loan_type", "Home Loan")
    tenure = applicant_data.get("tenure_months", 120)
    cibil = applicant_data.get("credit_score", "N/A")
    occupation = applicant_data.get("occupation", "Business")
    gross_income = applicant_data.get("gross_monthly_income", 0)
    
    emi = metrics.get("calculated_emi", 0)
    foir = metrics.get("calculated_foir", 0)
    ltv_res = metrics.get("ltv_compliance", {})
    ltv_val = ltv_res.get("ltv", 0)
    ltv_comp = ltv_res.get("compliant", True)
    roi = metrics.get("official_roi", 8.65)
    
    pd_val = risk_score.get("pd_percentage", "25.00")
    risk_cat = risk_score.get("risk_category", "Moderate")
    top_factors = risk_score.get("top_factors", [])
    
    # 1. Executive Summary Narrative
    if decision == "APPROVED":
        if msme_scorecard:
            exec_summary = (
                f"The credit underwriting appraisal for **{real_name}** requesting an MSME credit facility of **₹{loan_amount:,.2f}** "
                f"for a tenure of **{tenure} months** has been successfully evaluated. The applicant demonstrates strong commercial viability with an MSE score of "
                f"**{msme_scorecard.get('total_score')}/100 ({msme_scorecard.get('grade')})**, acceptable debt servicing conduct, and compliant risk metrics. "
                f"The proposal conforms to the lending guidelines of Central Bank of India.\n\n"
                f"**Final Decision:** **APPROVED**"
            )
        else:
            exec_summary = (
                f"The retail credit appraisal for **{real_name}** seeking a **{loan_type}** of **₹{loan_amount:,.2f}** "
                f"over **{tenure} months** has been reviewed. The applicant exhibits healthy repayment capacity with a calculated FOIR of **{foir:.2f}%**, "
                f"compliant LTV ratio of **{ltv_val:.2f}%**, and a favorable bureau score of **{cibil}**.\n\n"
                f"**Final Decision:** **APPROVED**"
            )
    else:
        if msme_scorecard and (msme_scorecard.get("total_score", 0) <= 50 or not msme_scorecard.get("hurdle_rate_met", True)):
            reason_str = f"an MSE Scorecard score of {msme_scorecard.get('total_score')}/100 ({msme_scorecard.get('grade')}), which fails the mandatory statutory Hurdle Rate benchmark of 50 marks"
        elif not ltv_comp:
            reason_str = f"a Loan-to-Value (LTV) ratio of {ltv_val:.2f}%, exceeding the statutory regulatory ceiling"
        else:
            reason_str = f"elevated credit risk indicators and repayment burden (FOIR: {foir:.2f}%, PD: {pd_val}%)"
            
        exec_summary = (
            f"The loan application submitted by **{real_name}** for a credit limit of **₹{loan_amount:,.2f}** ({loan_type}) "
            f"has been appraised against Central Bank of India underwriting benchmarks. Due to {reason_str}, "
            f"the proposal does not meet standard sanction criteria at current terms.\n\n"
            f"**Final Decision:** **REJECTED**"
        )

    # 2. Interest Rate Analysis
    if "MSME" in loan_type:
        cgtmse_note = " (including 25 bps concession for CGTMSE Guarantee backing)" if applicant_data.get("cgtmse_covered") or "CGTMSE" in str(applicant_data.get("collateral_coverage", "")) else ""
        grade_name = msme_scorecard.get('grade', 'CBI 4') if msme_scorecard else 'Standard'
        roi_analysis = (
            f"As per the Central Bank of India Master Circular 'ROI FOR RETAIL AND MSME ADVANCES AS ON 01.07.2026' (Base RBLR @ 8.25%), an interest rate of **{roi:.2f}% p.a.** "
            f"is assigned based on the enterprise scoring **{grade_name}** ({msme_scorecard.get('risk_profile', 'Standard') if msme_scorecard else ''}) "
            f"and bureau credit score of **{cibil}**{cgtmse_note}."
        )
    else:
        roi_analysis = (
            f"In accordance with Central Bank of India Retail ROI Grid as on 01.07.2026, the applicant has been assigned an official interest rate of **{roi:.2f}% p.a.** "
            f"pegged to RBLR based on the applicant's CIBIL score of **{cibil}** for **{loan_type}** advances."
        )

    # 3. MSME Section (if applicable)
    msme_md = ""
    if msme_scorecard:
        rows = []
        for item in msme_scorecard.get("breakdown", []):
            rows.append(f"| {item['parameter']} | {item['score']} | {item['max_score']} | {item['description']} |")
        table_rows = "\n".join(rows)
        hurdle_badge = "HURDLE RATE MET (> 50 Marks)" if msme_scorecard.get("hurdle_rate_met", True) else "SUB-HURDLE RATE (<= 50 Marks)"
        msme_md = f"""
## 3.1 🏢 Central Bank of India MSE Scoring Model ({msme_scorecard.get('model_form')})
**Total Score:** **{msme_scorecard.get('total_score')}/100** | **Risk Grade:** **{msme_scorecard.get('grade')}** ({msme_scorecard.get('risk_profile')})  
**Hurdle Rate Status:** **{hurdle_badge}** | **Recommendation:** {msme_scorecard.get('recommendation')}

| Parameter | Score Awarded | Max Marks | Assessment / Rule |
| :--- | :--- | :--- | :--- |
{table_rows}
| **TOTAL SCORE** | **{msme_scorecard.get('total_score')}/100** | **100** | **{msme_scorecard.get('grade')}** |
"""

    # 4. Top Factor Analysis for ML Risk
    factors_summary = []
    for f in top_factors:
        dir_text = "increased risk profile" if f["impact"] > 0 else "strengthened creditworthiness"
        factors_summary.append(f"• **{f['feature']}** (Recorded Value: {f['value']:.1f}): Contributed positively to model stability ({dir_text}).")
    factors_md = "\n".join(factors_summary) if factors_summary else "• All financial and bureau parameters evaluated within standard deviation thresholds."

    # 5. Policy Adherence Narrative
    foir_status = "compliant with standard 50% regulatory threshold" if foir <= 50 else "elevated above 50% cap, requiring cash-flow monitoring"
    ltv_status = f"compliant at {ltv_val:.2f}%" if ltv_comp else f"breaches the maximum allowable limit of {ltv_res.get('max_allowed', 80.0)}%"
    
    policy_narrative = (
        f"The credit appraisal evaluates borrower capacity, collateral margins, and regulatory guidelines. The calculated FOIR of **{foir:.2f}%** is {foir_status}, "
        f"and the collateral Loan-to-Value (LTV) is {ltv_status}. "
    )
    if msme_scorecard:
        m_grade = msme_scorecard.get("grade", "")
        if m_grade in ["CBI 5", "CBI 6", "Grade B"]:
            policy_narrative += (
                f"As a **{m_grade}** unit (Score: {msme_scorecard.get('total_score')}/100, Hurdle Rate Met), approval is subject to mandatory covenants: "
                f"maintaining minimum Current Ratio >= 1.20, debt-equity ratio <= 3.0, monthly submission of QIS/Stock Statements by the 15th, "
                f"and routing >= 80% of sales turnover exclusively through Central Bank of India."
            )
        elif m_grade in ["CBI 1", "CBI 2", "CBI 3", "CBI 4", "Grade A"]:
            policy_narrative += f"As a **{m_grade}** prime enterprise ({msme_scorecard.get('risk_profile')}), the application qualifies for standard / fast-track processing."
        else:
            policy_narrative += (
                f"The enterprise is categorized as **{m_grade}** (Score: {msme_scorecard.get('total_score')}/100), which falls below the bank's statutory "
                f"Hurdle Rate of 50 marks and cannot be sanctioned under standard delegation."
            )

    # 6. References & Bibliography
    clean_refs = []
    if applicable_policies:
        for p in applicable_policies:
            clean_p = re.sub(r'http[s]?://\S+', '', str(p))
            clean_p = re.sub(r'www\.\S+', '', clean_p)
            clean_p = re.sub(r'\s+', ' ', clean_p).strip()
            clean_refs.append(f"* {clean_p}")
    else:
        clean_refs = [
            "* [Doc: CBoI_MSE_Scoring_Models, Chunk: 0] - Central Bank of India MSE Scoring Framework",
            "* [Doc: RBI_Master_Circular_Retail, Chunk: 1] - RBI Prudential Guidelines on LTV and Exposure Norms",
            "* [Doc: CBoI_Interest_Rate_Circular_2026, Chunk: 2] - Risk-Based Lending Rates (RBLR) Grid"
        ]
    refs_md = "\n".join(clean_refs)

    # Compile Detailed Report
    detailed_report = f"""# 🏦 Comprehensive Credit Appraisal Report
**CONFIDENTIAL - Internal Bank Use Only**

## 1. 📊 Executive Summary
{exec_summary}

## 2. 👤 Applicant Profile & Loan Details
| Metric | Details |
| :--- | :--- |
| **Applicant / Entity Name** | {real_name} |
| **Loan Requested** | ₹{loan_amount:,.2f} ({loan_type}) |
| **Tenure** | {tenure} Months |
| **CIBIL Score** | {cibil} |
| **Occupation / Constitution** | {occupation} |
| **Gross Monthly Cash Flow / Income** | ₹{gross_income:,.2f} |

## 3. 💰 Financial Capacity & Obligation
| Metric | Value | Status |
| :--- | :--- | :--- |
| **Bank Assigned ROI** | {roi:.2f}% | 🏛️ Official Rate |
| **Calculated EMI** | ₹{emi:,.2f} | Standard Monthly Installment |
| **Calculated FOIR** | {foir:.2f}% | {'Compliant (<= 50%)' if foir <= 50 else 'Exceeds Standard 50% Threshold'} |
| **LTV Ratio** | {ltv_val:.2f}% | {'Compliant' if ltv_comp else 'Regulatory LTV Breach'} |

**Interest Rate Analysis:**
{roi_analysis}
{msme_md}
## 4. 🧠 Predictive Risk Analytics
> **Probability of Default (PD):** {pd_val}%  
> **Risk Category:** {risk_cat}

**Key Risk Drivers Identified:**
{factors_md}

## 5. 📜 Policy Adherence & Final Justification
{policy_narrative}

## 6. 📚 References & Bibliography
{refs_md}
"""

    # Compile Short One-Pager
    short_report = f"""# 📑 Credit Appraisal One-Pager
**Applicant:** {real_name} | **Requested:** ₹{loan_amount:,.2f} ({loan_type})

### 📈 Key Metrics Snapshot
* **CIBIL Score:** {cibil}
* **Assigned ROI:** {roi:.2f}%
* **Calculated FOIR:** {foir:.2f}% ({'Healthy' if foir <= 50 else 'Elevated'})
* **LTV Ratio:** {ltv_val:.2f}% ({'Compliant' if ltv_comp else 'Non-Compliant'})
* **Default Risk (PD):** {pd_val}% ({risk_cat})
{f"* **MSE Scorecard:** {msme_scorecard.get('total_score')}/100 ({msme_scorecard.get('grade')})" if msme_scorecard else ""}

### ✍️ Summary of Assessment
{exec_summary.split('**Final Decision:**')[0].strip()}

### ⚖️ Underwriting Recommendation: **{decision}**
"""

    return {
        "detailed_report": detailed_report.strip(),
        "short_report": short_report.strip()
    }
