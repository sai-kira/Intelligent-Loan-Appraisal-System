"""
Unit Test for MSME Scoring Engine (Form MSE 1 & Form MSE II)
Testing CBI 1 to CBI 10 Risk Grades and Hurdle Rate Benchmarks from Risk_Grades_Table.docx
"""
from msme_scoring_engine import calculate_mse_existing_score, calculate_mse_new_score, assign_cbi_risk_grade

def test_cbi_grades_mapping():
    print("--- TESTING CBI 1 TO CBI 10 RISK GRADES MAPPING ---")
    assert assign_cbi_risk_grade(95)["grade"] == "CBI 1"
    assert assign_cbi_risk_grade(95)["hurdle_rate_met"] is True
    
    assert assign_cbi_risk_grade(85)["grade"] == "CBI 2"
    assert assign_cbi_risk_grade(85)["hurdle_rate_met"] is True

    assert assign_cbi_risk_grade(75)["grade"] == "CBI 3"
    assert assign_cbi_risk_grade(75)["hurdle_rate_met"] is True

    assert assign_cbi_risk_grade(65)["grade"] == "CBI 4"
    assert assign_cbi_risk_grade(65)["hurdle_rate_met"] is True

    assert assign_cbi_risk_grade(58)["grade"] == "CBI 5"
    assert assign_cbi_risk_grade(58)["hurdle_rate_met"] is True

    assert assign_cbi_risk_grade(52)["grade"] == "CBI 6"
    assert assign_cbi_risk_grade(52)["hurdle_rate_met"] is True

    # Hurdle rate boundary: 50 is Sub-Hurdle, 51 is Passing
    assert assign_cbi_risk_grade(50)["grade"] == "CBI 7"
    assert assign_cbi_risk_grade(50)["hurdle_rate_met"] is False

    assert assign_cbi_risk_grade(43)["grade"] == "CBI 8"
    assert assign_cbi_risk_grade(43)["hurdle_rate_met"] is False

    assert assign_cbi_risk_grade(38)["grade"] == "CBI 9"
    assert assign_cbi_risk_grade(38)["hurdle_rate_met"] is False

    assert assign_cbi_risk_grade(25)["grade"] == "CBI 10"
    assert assign_cbi_risk_grade(25)["hurdle_rate_met"] is False

    # Defaulter override check
    res_def = assign_cbi_risk_grade(98, is_defaulter=True)
    assert res_def["final_score"] == 0
    assert res_def["grade"] == "CBI 10"
    assert res_def["hurdle_rate_met"] is False
    print("CBI 1 to CBI 10 Grade Mapping & Hurdle Rate Rules Verified!\n")

def test_existing_unit():
    print("--- TESTING FORM MSE 1 (EXISTING UNITS) ---")
    
    # 1. Prime unit: high score (CBI 1)
    prime_data = {
        "current_ratio": 1.45,
        "debt_equity_ratio": 1.5,
        "sales_growth_rate": 22.0,
        "pat_margin": 16.0,
        "sanction_compliance": "Compliant",
        "stock_statement_status": "Timely",
        "debt_servicing_history": "Within 1 month",
        "inventory_compliance": "Fair Compliance",
        "bills_culture": True,
        "bill_payment_record": "Prompt",
        "review_documents_timely": True,
        "lc_bg_status": "Prompt / No Facility",
        "ancillary_relationship": "Substantial"
    }
    res_prime = calculate_mse_existing_score(prime_data)
    print(f"Prime Unit Score: {res_prime['total_score']}/100 | Grade: {res_prime['grade']} | Hurdle Met: {res_prime['hurdle_rate_met']}")
    assert res_prime["total_score"] >= 90
    assert res_prime["grade"] in ["CBI 1", "CBI 2"]
    assert res_prime["hurdle_rate_met"] is True

    # 2. Defaulter unit: automatic zero score (CBI 10)
    distressed_data = {
        "current_ratio": 0.85,
        "debt_equity_ratio": 5.5,
        "sales_growth_rate": -5.0,
        "pat_margin": -2.0,
        "sanction_compliance": "Non-compliant",
        "stock_statement_status": "Non-Submission",
        "debt_servicing_history": "Overdue > 3 months", # Bank Defaulter
        "inventory_compliance": "High deviation",
        "bills_culture": False,
        "bill_payment_record": "Overdue > 3 months",
        "review_documents_timely": False,
        "lc_bg_status": "Devolvement / Invocation",
        "ancillary_relationship": "None"
    }
    res_dist = calculate_mse_existing_score(distressed_data)
    print(f"Defaulter Unit Score: {res_dist['total_score']}/100 | Grade: {res_dist['grade']} | Hurdle Met: {res_dist['hurdle_rate_met']}")
    assert res_dist["total_score"] == 0, f"Expected 0 for defaulter, got {res_dist['total_score']}"
    assert res_dist["grade"] == "CBI 10"
    assert res_dist["hurdle_rate_met"] is False
    print("Form MSE 1 Tests Passed Successfully!\n")

def test_new_unit():
    print("--- TESTING FORM MSE II (NEW UNITS) ---")
    
    # 1. Strong Greenfield Unit (CBI 1 / CBI 2)
    strong_data = {
        "projected_sales_growth": 18.0,
        "projected_pat_margin": 14.0,
        "projected_der": 1.8,
        "inputs_access": "Locally Available / Tied up",
        "market_access": "Locally Available / Tied up",
        "promoter_experience": "Qualified and Experienced",
        "bank_relationship": "Existing Customer",
        "premises_type": "Owned",
        "collateral_coverage": "Covered under CGTMSE Scheme"
    }
    res_strong = calculate_mse_new_score(strong_data)
    print(f"Strong Greenfield Score: {res_strong['total_score']}/100 | Grade: {res_strong['grade']} | Hurdle Met: {res_strong['hurdle_rate_met']}")
    assert res_strong["total_score"] >= 80
    assert res_strong["grade"] in ["CBI 1", "CBI 2"]
    assert res_strong["hurdle_rate_met"] is True

    # 2. Weak Greenfield Unit (CBI 10)
    weak_data = {
        "projected_sales_growth": 3.0,
        "projected_pat_margin": 2.0,
        "projected_der": 4.5,
        "inputs_access": "Not Identified",
        "market_access": "Unidentified",
        "promoter_experience": "No qualification/experience",
        "bank_relationship": "Introduced by Govt Dept / Others",
        "premises_type": "Leased / Rented",
        "collateral_coverage": "Unsecured"
    }
    res_weak = calculate_mse_new_score(weak_data)
    print(f"Weak Greenfield Score: {res_weak['total_score']}/100 | Grade: {res_weak['grade']} | Hurdle Met: {res_weak['hurdle_rate_met']}")
    assert res_weak["total_score"] <= 35
    assert res_weak["grade"] == "CBI 10"
    assert res_weak["hurdle_rate_met"] is False
    print("Form MSE II Tests Passed Successfully!\n")

if __name__ == "__main__":
    test_cbi_grades_mapping()
    test_existing_unit()
    test_new_unit()
    print("ALL 10-TIER MSME SCORING & HURDLE RATE TESTS PASSED!")
