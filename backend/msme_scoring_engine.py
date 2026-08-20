"""
Central Bank of India - Manual Scoring Engine for Micro and Small Enterprises (MSME)
Approved by IBA - Common Loan Application and Appraisal Guidelines (Exposure up to Rs 2 Crore)
"""

from typing import Dict, Any, List

def assign_cbi_risk_grade(score: int, is_defaulter: bool = False) -> Dict[str, Any]:
    """
    Assigns official Central Bank of India MSE Risk Grade (CBI 1 to CBI 10)
    as per Risk_Grades_Table.docx and Central Bank of India Credit Policy.
    Hurdle Rate: Above 50 marks.
    Defaulter Rule: Total score automatically becomes 0 (CBI 10).
    """
    if is_defaulter:
        score = 0
        
    score = max(0, min(100, score))
    hurdle_rate_met = (score > 50)
    
    if score > 90:
        grade = "CBI 1"
        risk_profile = "Exceptional Safety (Prime MSME Borrower)"
        recommendation = "Recommended for Sanction with Fast-Track terms & Prime Pricing"
    elif score >= 81:
        grade = "CBI 2"
        risk_profile = "Very High Safety (Very Low Credit Risk)"
        recommendation = "Recommended for Sanction with Standard Prime terms"
    elif score >= 71:
        grade = "CBI 3"
        risk_profile = "High Safety (Low Credit Risk)"
        recommendation = "Recommended for Sanction with Standard terms"
    elif score >= 61:
        grade = "CBI 4"
        risk_profile = "Adequate Safety (Moderate Risk)"
        recommendation = "Recommended for Sanction with Standard terms"
    elif score >= 56:
        grade = "CBI 5"
        risk_profile = "Moderate Safety (Standard Risk Borrower)"
        recommendation = "Recommended for Sanction with Special Covenants (Min CR >= 1.20, DER <= 3.0, Monthly QIS by 15th, >= 80% Sales Routing)"
    elif score >= 51:
        grade = "CBI 6"
        risk_profile = "Minimum Hurdle Rate Met (Elevated Risk)"
        recommendation = "Recommended for Sanction with Enhanced Covenants & Stock Audit Monitoring"
    elif score >= 46:
        grade = "CBI 7"
        risk_profile = "Inadequate Safety (Sub-Hurdle Rate / High Risk)"
        recommendation = "Ineligible under Standard Delegation (Fails Hurdle Rate > 50). Requires 100%+ Collateral / CGTMSE or Zonal Exception."
    elif score >= 41:
        grade = "CBI 8"
        risk_profile = "High Risk / Weak Repayment Capacity (Sub-Hurdle Rate)"
        recommendation = "Ineligible under Standard Delegation (Fails Hurdle Rate > 50). Requires Executive Override."
    elif score >= 36:
        grade = "CBI 9"
        risk_profile = "Very High Risk / Vulnerable (Sub-Hurdle Rate)"
        recommendation = "Ineligible under Standard Delegation (Fails Hurdle Rate > 50). High Default Probability."
    else:
        grade = "CBI 10"
        risk_profile = "Substantial Risk / Default Imminent / Bank Defaulter"
        recommendation = "Rejected / Ineligible (Automatic Rejection under CBoI MSME Policy)."
        
    return {
        "final_score": score,
        "grade": grade,
        "risk_profile": risk_profile,
        "recommendation": recommendation,
        "hurdle_rate_met": hurdle_rate_met,
        "hurdle_benchmark": 50
    }

def calculate_mse_existing_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Form MSE 1: Scoring Model for Existing Units / Borrowers with credit exposure up to Rs 2 Crore.
    Maximum Score: 100 Marks.
    """
    breakdown = []
    total_score = 0
    is_defaulter = False
    
    # 1. Terms & Conditions Compliance
    sanction_compliance = data.get("sanction_compliance", "Compliant")
    if sanction_compliance in ["Compliant", "Yes", True]:
        p1_score = 5
        p1_desc = "Full compliance with sanction terms and conditions"
    else:
        p1_score = -5
        p1_desc = "Non-compliance due to borrower non-cooperation"
    breakdown.append({"parameter": "Sanction Compliance", "score": p1_score, "max_score": 5, "description": p1_desc})
    total_score += p1_score

    # 2. Current Ratio (CR)
    cr = float(data.get("current_ratio", 1.33))
    if cr >= 1.33:
        p2_score = 5
        p2_desc = f"CR {cr:.2f} >= 1.33 (Benchmark standard met)"
    elif cr >= 1.20:
        p2_score = 4
        p2_desc = f"CR {cr:.2f} between 1.20 to 1.32"
    elif cr >= 1.10:
        p2_score = 3
        p2_desc = f"CR {cr:.2f} between 1.10 to 1.19"
    elif cr >= 1.00:
        p2_score = 1
        p2_desc = f"CR {cr:.2f} between 1.00 to 1.09"
    else:
        p2_score = 0
        p2_desc = f"CR {cr:.2f} < 1.00 (Inadequate liquidity)"
    breakdown.append({"parameter": "Current Ratio (Liquidity)", "score": p2_score, "max_score": 5, "description": p2_desc})
    total_score += p2_score

    # 3. Debt Equity Ratio (DER) past 2 years
    der = float(data.get("debt_equity_ratio", 2.0))
    if der <= 2.0:
        p3_score = 10
        p3_desc = f"DER {der:.2f} <= 2.0 (Sound capital structure)"
    elif der <= 3.0:
        p3_score = 8
        p3_desc = f"DER {der:.2f} between 2.0 to 3.0"
    elif der <= 4.0:
        p3_score = 5
        p3_desc = f"DER {der:.2f} between 3.0 to 4.0"
    elif der <= 5.0:
        p3_score = 3
        p3_desc = f"DER {der:.2f} between 4.0 to 5.0"
    else:
        p3_score = 0
        p3_desc = f"DER {der:.2f} > 5.0 (High leverage)"
    breakdown.append({"parameter": "Debt Equity Ratio (Leverage)", "score": p3_score, "max_score": 10, "description": p3_desc})
    total_score += p3_score

    # 4. Net Sales Growth Rate (Past 3 Years)
    growth = float(data.get("sales_growth_rate", 15.0))
    if growth > 20.0:
        p4_score = 10
        p4_desc = f"Net Sales Growth {growth:.1f}% > 20% p.a."
    elif growth >= 15.0:
        p4_score = 8
        p4_desc = f"Net Sales Growth {growth:.1f}% (15% to 20%)"
    elif growth >= 10.0:
        p4_score = 5
        p4_desc = f"Net Sales Growth {growth:.1f}% (10% to 15%)"
    elif growth > 0.0:
        p4_score = 3
        p4_desc = f"Net Sales Growth {growth:.1f}% (Positive)"
    else:
        p4_score = 0
        p4_desc = f"Net Sales Growth {growth:.1f}% (Negative / Declining)"
    breakdown.append({"parameter": "Net Sales Growth (3 Years)", "score": p4_score, "max_score": 10, "description": p4_desc})
    total_score += p4_score

    # 5. PAT / Net Sales Margin
    pat_margin = float(data.get("pat_margin", 10.0))
    if pat_margin > 15.0:
        p5_score = 10
        p5_desc = f"PAT Margin {pat_margin:.1f}% > 15%"
    elif pat_margin >= 10.0:
        p5_score = 8
        p5_desc = f"PAT Margin {pat_margin:.1f}% (10% to 15%)"
    elif pat_margin >= 5.0:
        p5_score = 5
        p5_desc = f"PAT Margin {pat_margin:.1f}% (5% to 10%)"
    elif pat_margin > 0.0:
        p5_score = 3
        p5_desc = f"PAT Margin {pat_margin:.1f}% (Positive)"
    else:
        p5_score = 0
        p5_desc = f"PAT Margin {pat_margin:.1f}% <= 0% (Loss Making)"
    breakdown.append({"parameter": "PAT / Net Sales Margin", "score": p5_score, "max_score": 10, "description": p5_desc})
    total_score += p5_score

    # 6. Stock Statement & QIS Returns Submission
    stock_status = data.get("stock_statement_status", "Timely")
    if stock_status in ["Timely", "Regular", "Monthly"]:
        p6_score = 10
        p6_desc = "Regular and timely submission of stock statements"
    elif stock_status in ["Delayed", "Quarterly"]:
        p6_score = 5
        p6_desc = "Delayed submission of stock statements"
    else:
        p6_score = 0
        p6_desc = "Non-submission of stock statements / QIS returns"
    breakdown.append({"parameter": "Stock Statement / QIS Compliance", "score": p6_score, "max_score": 10, "description": p6_desc})
    total_score += p6_score

    # 7. Interest & Installment Servicing (Existing Borrowing Arrangements)
    servicing = data.get("debt_servicing_history", "Within 1 month")
    if servicing == "Within 1 month":
        p7_score = 10
        p7_desc = "Serviced within 1 month (Standard Asset - Prime)"
    elif servicing == "Within 2 months":
        p7_score = 7
        p7_desc = "Serviced within 2 months (SMA-0 / SMA-1)"
    elif servicing == "Within 3 months":
        p7_score = 5
        p7_desc = "Serviced within 3 months (SMA-2)"
    else:
        p7_score = 0
        p7_desc = "Defaulter to Bank / Overdue > 3 months (NPA - Defaulter Override)"
        is_defaulter = True
    breakdown.append({"parameter": "Interest & Installment Servicing", "score": p7_score, "max_score": 10, "description": p7_desc})
    total_score += p7_score

    # 8. Level of Inventory Norms Compliance
    inventory = data.get("inventory_compliance", "Fair Compliance")
    if inventory in ["Strict", "Low deviation", "No deviation"]:
        p8_score = 10
        p8_desc = "Within holding norms / deviation <= 10%"
    elif inventory in ["Fair Compliance", "Moderate deviation"]:
        p8_score = 5
        p8_desc = "Fair compliance (deviation <= 15%)"
    elif inventory in ["Compliance (15%-30% dev)", "High deviation"]:
        p8_score = 3
        p8_desc = "Compliance with deviation 15% to 30%"
    else:
        p8_score = 0
        p8_desc = "High deviation > 30% from holding norms"
    breakdown.append({"parameter": "Inventory Norms Compliance", "score": p8_score, "max_score": 10, "description": p8_desc})
    total_score += p8_score

    # 9. Compliance to Bills Culture
    bills_culture = data.get("bills_culture", True)
    p9_score = 5 if bills_culture else 0
    p9_desc = "Trade bill usage" if bills_culture else "No bills culture"
    breakdown.append({"parameter": "Compliance to Bills Culture", "score": p9_score, "max_score": 5, "description": p9_desc})
    total_score += p9_score

    # 10. Payment of Bills on Due Dates
    bill_payment = data.get("bill_payment_record", "Prompt")
    if bill_payment == "Prompt":
        p10_score = 10
        p10_desc = "Payment of bills prompt on due dates"
    elif bill_payment == "Delayed":
        p10_score = 5
        p10_desc = "Delayed up to 1 month"
    else:
        p10_score = 0
        p10_desc = "Delayed > 1 month / Overdue"
    breakdown.append({"parameter": "Bill Payment Discipline", "score": p10_score, "max_score": 10, "description": p10_desc})
    total_score += p10_score

    # 11. Submission of Financial Documents for Annual Review
    review_docs = data.get("review_documents_timely", True)
    p11_score = 5 if review_docs else 0
    p11_desc = "Within 3 months of due date" if review_docs else "Delayed submission > 3 months"
    breakdown.append({"parameter": "Annual Review Documents Submission", "score": p11_score, "max_score": 5, "description": p11_desc})
    total_score += p11_score

    # 12. LC / BG Commitments Fulfillment
    lc_bg = data.get("lc_bg_status", "Prompt / No Facility")
    if lc_bg in ["Prompt / No Facility", "Prompt", "No Facility"]:
        p12_score = 5
        p12_desc = "Prompt fulfillment of LC/BG or no facility enjoyed (+5 default bonus)"
    else:
        p12_score = -10
        p12_desc = "Devolvement of LCs / Invocation of Bank Guarantees"
    breakdown.append({"parameter": "LC / BG Commitments Fulfillment", "score": p12_score, "max_score": 5, "description": p12_desc})
    total_score += p12_score

    # 13. Ancillary Business & Bank Association
    ancillary = data.get("ancillary_relationship", "Substantial")
    p13_score = 10 if ancillary in ["Substantial", "Good", "Yes"] else 5
    breakdown.append({"parameter": "Ancillary Business & Bank Association", "score": p13_score, "max_score": 10, "description": "Strong banking relationship & deposits"})
    total_score += p13_score

    # Apply CBI Risk Grading Matrix & Defaulter Override
    cbi_res = assign_cbi_risk_grade(total_score, is_defaulter=is_defaulter)

    return {
        "model_form": "Form MSE 1 (Existing Units)",
        "total_score": cbi_res["final_score"],
        "max_score": 100,
        "grade": cbi_res["grade"],
        "risk_profile": cbi_res["risk_profile"],
        "recommendation": cbi_res["recommendation"],
        "hurdle_rate_met": cbi_res["hurdle_rate_met"],
        "hurdle_benchmark": cbi_res["hurdle_benchmark"],
        "is_defaulter": is_defaulter,
        "breakdown": breakdown
    }

def calculate_mse_new_score(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Form MSE II: Scoring Model for New Units / Greenfield Enterprises (Credit Exposure up to Rs 2 Crore).
    Maximum Score: 100 Marks.
    """
    breakdown = []
    total_score = 0

    # 1. Projected 3-Year Avg Net Sales Growth
    proj_growth = float(data.get("projected_sales_growth", 15.0))
    if proj_growth > 15.0:
        p1_score = 15
        p1_desc = f"Projected Sales Growth {proj_growth:.1f}% > 15% p.a."
    elif proj_growth >= 10.0:
        p1_score = 10
        p1_desc = f"Projected Sales Growth {proj_growth:.1f}% (10% to 15%)"
    elif proj_growth >= 5.0:
        p1_score = 5
        p1_desc = f"Projected Sales Growth {proj_growth:.1f}% (5% to 10%)"
    else:
        p1_score = 0
        p1_desc = f"Projected Sales Growth {proj_growth:.1f}% < 5%"
    breakdown.append({"parameter": "Projected Net Sales Growth (3-Yr Avg)", "score": p1_score, "max_score": 15, "description": p1_desc})
    total_score += p1_score

    # 2. Projected PAT / Net Sales Average
    proj_pat = float(data.get("projected_pat_margin", 10.0))
    if proj_pat > 15.0:
        p2_score = 15
        p2_desc = f"Projected PAT Margin {proj_pat:.1f}% > 15%"
    elif proj_pat >= 10.0:
        p2_score = 10
        p2_desc = f"Projected PAT Margin {proj_pat:.1f}% (10% to 15%)"
    elif proj_pat >= 5.0:
        p2_score = 5
        p2_desc = f"Projected PAT Margin {proj_pat:.1f}% (5% to 10%)"
    elif proj_pat > 0.0:
        p2_score = 3
        p2_desc = f"Projected PAT Margin {proj_pat:.1f}% (Positive)"
    else:
        p2_score = 0
        p2_desc = f"Projected PAT Margin {proj_pat:.1f}% <= 0%"
    breakdown.append({"parameter": "Projected PAT / Net Sales Margin", "score": p2_score, "max_score": 15, "description": p2_desc})
    total_score += p2_score

    # 3. Projected Debt Equity Ratio (First 3 Years)
    proj_der = float(data.get("projected_der", 2.0))
    if proj_der <= 2.0:
        p3_score = 10
        p3_desc = f"Projected DER {proj_der:.2f} <= 2.0 (Conservative)"
    elif proj_der <= 3.0:
        p3_score = 8
        p3_desc = f"Projected DER {proj_der:.2f} (2.0 to 3.0)"
    elif proj_der <= 4.0:
        p3_score = 5
        p3_desc = f"Projected DER {proj_der:.2f} (3.0 to 4.0)"
    else:
        p3_score = 0
        p3_desc = f"Projected DER {proj_der:.2f} > 4.0"
    breakdown.append({"parameter": "Projected Debt Equity Ratio", "score": p3_score, "max_score": 10, "description": p3_desc})
    total_score += p3_score

    # 4. Access to Inputs (Labor / Raw Materials / Power)
    inputs = data.get("inputs_access", "Locally Available / Tied up")
    if inputs == "Locally Available / Tied up":
        p4_score = 10
        p4_desc = "Raw material, power, and labor locally secured"
    elif inputs == "Source Identified":
        p4_score = 5
        p4_desc = "Not locally available but reliable sources identified"
    else:
        p4_score = 0
        p4_desc = "Inputs neither locally available nor identified"
    breakdown.append({"parameter": "Access to Production Inputs", "score": p4_score, "max_score": 10, "description": p4_desc})
    total_score += p4_score

    # 5. Access to Market for Products
    market = data.get("market_access", "Locally Available / Tied up")
    if market == "Locally Available / Tied up":
        p5_score = 10
        p5_desc = "Off-take agreements / local demand secured"
    elif market == "Market Identified":
        p5_score = 5
        p5_desc = "Potential market channels identified"
    else:
        p5_score = 0
        p5_desc = "Distribution channels unidentified"
    breakdown.append({"parameter": "Market Access & Off-take", "score": p5_score, "max_score": 10, "description": p5_desc})
    total_score += p5_score

    # 6. Promoter Experience & Industry Qualification
    promoter_exp = data.get("promoter_experience", "Qualified and Experienced")
    if promoter_exp == "Qualified and Experienced":
        p6_score = 10
        p6_desc = "Technically qualified and domain experienced"
    elif promoter_exp == "Qualified / Trained":
        p6_score = 5
        p6_desc = "Qualified/trained but limited industry experience"
    else:
        p6_score = 0
        p6_desc = "No prior qualification, training, or experience"
    breakdown.append({"parameter": "Promoter Industry Experience", "score": p6_score, "max_score": 10, "description": p6_desc})
    total_score += p6_score

    # 7. Relationship with Bank
    relationship = data.get("bank_relationship", "Existing Customer")
    if relationship == "Existing Customer":
        p7_score = 10
        p7_desc = "Existing Central Bank of India customer"
    else:
        p7_score = 5
        p7_desc = "Introduced by Govt Dept / DIC / Others"
    breakdown.append({"parameter": "Bank Relationship & Sourcing", "score": p7_score, "max_score": 10, "description": p7_desc})
    total_score += p7_score

    # 8. Factory / Unit Premises
    premises = data.get("premises_type", "Owned")
    if premises in ["Owned", "Freehold"]:
        p8_score = 5
        p8_desc = "Unit/factory premises owned by enterprise"
    else:
        p8_score = 3
        p8_desc = "Unit/factory taken on registered lease/rental"
    breakdown.append({"parameter": "Factory / Operating Premises", "score": p8_score, "max_score": 5, "description": p8_desc})
    total_score += p8_score

    # 9. Collateral Security / CGTMSE Coverage
    collateral = data.get("collateral_coverage", "Covered under CGTMSE Scheme")
    if collateral == "Over 100% Tangible Collateral":
        p9_score = 15
        p9_desc = "Tangible collateral/guarantees > 100% of loan"
    elif collateral in ["Up to 100% Collateral", "Covered under CGTMSE Scheme", "CGTMSE Covered"]:
        p9_score = 10
        p9_desc = "Collateral up to 100% or 100% covered under CGTMSE Scheme"
    elif collateral == "Up to 50% Collateral":
        p9_score = 5
        p9_desc = "Collateral available up to 50%"
    elif collateral == "Below 50% Collateral":
        p9_score = 3
        p9_desc = "Collateral below 50%"
    else:
        p9_score = 0
        p9_desc = "Unsecured without CGTMSE backing"
    breakdown.append({"parameter": "Collateral & Credit Guarantee (CGTMSE)", "score": p9_score, "max_score": 15, "description": p9_desc})
    total_score += p9_score

    # Apply CBI Risk Grading Matrix
    cbi_res = assign_cbi_risk_grade(total_score, is_defaulter=False)

    return {
        "model_form": "Form MSE II (New Units)",
        "total_score": cbi_res["final_score"],
        "max_score": 100,
        "grade": cbi_res["grade"],
        "risk_profile": cbi_res["risk_profile"],
        "recommendation": cbi_res["recommendation"],
        "hurdle_rate_met": cbi_res["hurdle_rate_met"],
        "hurdle_benchmark": cbi_res["hurdle_benchmark"],
        "is_defaulter": False,
        "breakdown": breakdown
    }
