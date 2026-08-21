"""
Comprehensive Test Suite & Database Seeder for Central Bank of India ILAS
Populates diverse benchmark applications across Retail & MSME portfolios,
runs end-to-end automated appraisals, manager approvals, and tests edge cases.
"""
import sys
import os
import time
import requests
import json
import unittest

API_BASE_URL = "http://127.0.0.1:8000"

BENCHMARK_PROFILES = [
    {
        "name": "Dr. Rajesh Sharma", "age": 42, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 350000, "net_monthly_income": 280000, "total_assets": 25000000,
        "credit_score": 790, "avg_credit_balance_6m": 800000, "existing_emi": 20000, "active_lines": 1, "inquiries_6m": 0,
        "loan_amount": 5000000, "tenure_months": 240, "loan_type": "Home Loan", "property_value": 8500000, "security_type": "Property",
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "Sunita Menon", "age": 36, "gender": "Female", "marital_status": "Single", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 180000, "net_monthly_income": 140000, "total_assets": 9000000,
        "credit_score": 765, "avg_credit_balance_6m": 350000, "existing_emi": 15000, "active_lines": 2, "inquiries_6m": 1,
        "loan_amount": 1200000, "tenure_months": 60, "loan_type": "Auto Loan", "property_value": 1600000, "security_type": "Vehicle",
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "Amitabh Verma", "age": 31, "gender": "Male", "marital_status": "Single", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 140000, "net_monthly_income": 115000, "total_assets": 4500000,
        "credit_score": 750, "avg_credit_balance_6m": 250000, "existing_emi": 8000, "active_lines": 1, "inquiries_6m": 1,
        "loan_amount": 400000, "tenure_months": 36, "loan_type": "Personal Loan", "property_value": 0, "security_type": "None",
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "Pooja Hegde", "age": 23, "gender": "Female", "marital_status": "Single", "category": "OBC",
        "occupation": "Professional", "gross_monthly_income": 80000, "net_monthly_income": 65000, "total_assets": 2000000,
        "credit_score": 730, "avg_credit_balance_6m": 150000, "existing_emi": 0, "active_lines": 0, "inquiries_6m": 0,
        "loan_amount": 2500000, "tenure_months": 84, "loan_type": "Education Loan", "property_value": 3500000, "security_type": "Property",
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "Apex Precision Engineering Pvt Ltd", "age": 48, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 450000, "net_monthly_income": 380000, "total_assets": 18000000,
        "credit_score": 780, "avg_credit_balance_6m": 600000, "existing_emi": 35000, "active_lines": 3, "inquiries_6m": 0,
        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - Existing Unit", "property_value": 8000000, "security_type": "Property",
        "current_ratio": 1.45, "debt_equity_ratio": 1.5, "sales_growth_rate": 22.0, "pat_margin": 16.0,
        "sanction_compliance": "Compliant", "stock_statement_status": "Timely", "debt_servicing_history": "Within 1 month",
        "inventory_compliance": "Fair Compliance", "bills_culture": True, "bill_payment_record": "Prompt",
        "review_documents_timely": True, "lc_bg_status": "Prompt / No Facility", "ancillary_relationship": "Substantial",
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "Surat Silk & Synthetics Mills", "age": 52, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 380000, "net_monthly_income": 290000, "total_assets": 12000000,
        "credit_score": 715, "avg_credit_balance_6m": 400000, "existing_emi": 40000, "active_lines": 3, "inquiries_6m": 1,
        "loan_amount": 4500000, "tenure_months": 60, "loan_type": "MSME Loan - Existing Unit", "property_value": 6500000, "security_type": "Property",
        "current_ratio": 1.25, "debt_equity_ratio": 2.6, "sales_growth_rate": 12.0, "pat_margin": 8.0,
        "sanction_compliance": "Compliant", "stock_statement_status": "Monthly", "debt_servicing_history": "Within 2 months",
        "inventory_compliance": "Fair Compliance", "bills_culture": True, "bill_payment_record": "Prompt",
        "review_documents_timely": True, "lc_bg_status": "Prompt / No Facility", "ancillary_relationship": "Moderate",
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "BioGreen Agro Processing LLP", "age": 39, "gender": "Female", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 400000, "net_monthly_income": 320000, "total_assets": 14000000,
        "credit_score": 755, "avg_credit_balance_6m": 500000, "existing_emi": 20000, "active_lines": 2, "inquiries_6m": 1,
        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - New Unit", "property_value": 6500000, "security_type": "CGTMSE / Plant & Machinery",
        "projected_sales_growth": 18.0, "projected_pat_margin": 14.0, "projected_der": 1.8,
        "inputs_access": "Locally Available / Tied up", "market_access": "Locally Available / Tied up",
        "promoter_experience": "Qualified and Experienced", "bank_relationship": "Existing Customer",
        "premises_type": "Owned", "collateral_coverage": "Covered under CGTMSE Scheme", "cgtmse_covered": True,
        "expected_decision": "APPROVED", "manager_action": "APPROVED"
    },
    {
        "name": "Sunrise Biofuels Startup", "age": 33, "gender": "Male", "marital_status": "Single", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 120000, "net_monthly_income": 85000, "total_assets": 3000000,
        "credit_score": 620, "avg_credit_balance_6m": 100000, "existing_emi": 45000, "active_lines": 4, "inquiries_6m": 3,
        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - New Unit", "property_value": 2000000, "security_type": "None",
        "projected_sales_growth": 3.0, "projected_pat_margin": 2.0, "projected_der": 4.5,
        "inputs_access": "Not Identified", "market_access": "Unidentified",
        "promoter_experience": "No qualification/experience", "bank_relationship": "Introduced by Govt Dept / Others",
        "premises_type": "Leased / Rented", "collateral_coverage": "Unsecured", "cgtmse_covered": False,
        "expected_decision": "REJECTED", "manager_action": "REJECTED"
    },
    {
        "name": "Defaulter Steels LLP", "age": 50, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 300000, "net_monthly_income": -250000, "total_assets": 5000000,
        "credit_score": 550, "avg_credit_balance_6m": 10000, "existing_emi": 80000, "active_lines": 5, "inquiries_6m": 4,
        "loan_amount": 3000000, "tenure_months": 48, "loan_type": "MSME Loan - Existing Unit", "property_value": 4000000, "security_type": "Property",
        "current_ratio": 0.90, "debt_equity_ratio": 4.5, "sales_growth_rate": -5.0, "pat_margin": -2.0,
        "sanction_compliance": "Non-compliant", "stock_statement_status": "Non-Submission", "debt_servicing_history": "Overdue > 3 months",
        "inventory_compliance": "High deviation", "bills_culture": False, "bill_payment_record": "Overdue > 3 months",
        "review_documents_timely": False, "lc_bg_status": "Devolvement / Invocation", "ancillary_relationship": "None",
        "expected_decision": "REJECTED", "manager_action": "REJECTED"
    },
    {
        "name": "Vikas High-FOIR Retail", "age": 29, "gender": "Male", "marital_status": "Single", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 50000, "net_monthly_income": 40000, "total_assets": 1000000,
        "credit_score": 680, "avg_credit_balance_6m": 25000, "existing_emi": 30000, "active_lines": 3, "inquiries_6m": 2,
        "loan_amount": 3000000, "tenure_months": 120, "loan_type": "Home Loan", "property_value": 3200000, "security_type": "Property",
        "expected_decision": "REJECTED", "manager_action": "REJECTED"
    }
]

def run_deep_system_testing():
    print("=" * 80)
    print("🏦 Central Bank of India ILAS - Holistic Deep System Testing & Seeding")
    print("=" * 80)
    
    # 1. Health check
    print("\n1. Testing Backend API Health...")
    try:
        profiles_res = requests.get(f"{API_BASE_URL}/financials/profiles", timeout=5).json()
        print(f"   ✅ Backend API is responsive. Pre-loaded corporate profiles: {len(profiles_res)}")
    except Exception as e:
        print(f"   ❌ Backend API is unreachable: {e}")
        return False

    # 2. Process all benchmark applications
    print(f"\n2. Submitting & Appraising {len(BENCHMARK_PROFILES)} Benchmark Applications...")
    seeded_threads = []
    
    for idx, p in enumerate(BENCHMARK_PROFILES, 1):
        print(f"   [{idx}/{len(BENCHMARK_PROFILES)}] Submitting: {p['name']} ({p['loan_type']} - ₹{p['loan_amount']:,.2f})...")
        payload = {k: v for k, v in p.items() if k not in ["expected_decision", "manager_action"]}
        
        apply_res = requests.post(f"{API_BASE_URL}/apply", json=payload, timeout=10).json()
        thread_id = apply_res.get("thread_id")
        if not thread_id:
            print(f"   ❌ Failed to submit {p['name']}: {apply_res}")
            continue
            
        # Poll for completion / WAITING_FOR_MANAGER
        max_retries = 30
        status_data = None
        for _ in range(max_retries):
            time.sleep(1)
            s_res = requests.get(f"{API_BASE_URL}/status/{thread_id}", timeout=5).json()
            if s_res.get("status") in ["WAITING_FOR_MANAGER", "COMPLETED"]:
                status_data = s_res
                break
                
        if not status_data:
            print(f"   ❌ Timed out waiting for appraisal of {p['name']}")
            continue
            
        rec_decision = status_data.get("decision_outcome")
        print(f"      ▶ Appraisal Outcome: {rec_decision} | Risk Category: {status_data.get('risk_score', {}).get('risk_category')}")
        
        # Verify Chapter 4 presence for MSME
        if "MSME" in p["loan_type"]:
            det_rep = status_data.get("detailed_report", "")
            has_ch4 = "## 4. 🏢 Corporate Financial Intelligence" in det_rep or "Corporate Financial Intelligence" in det_rep
            if has_ch4:
                print("      ✅ Chapter 4 Corporate Financial Intelligence verified in detailed memo.")
            else:
                print("      ⚠️ Chapter 4 missing in detailed memo!")
                
        # Perform Manager Decision (HITL Approval / Rejection)
        mgr_action = p.get("manager_action", "APPROVED")
        appr_res = requests.post(f"{API_BASE_URL}/approve/{thread_id}", json={"decision": mgr_action}, timeout=10)
        if appr_res.status_code == 200:
            print(f"      ✅ Manager Decision Executed: {mgr_action}")
        else:
            print(f"      ❌ Manager Decision Failed: {appr_res.text}")
            
        seeded_threads.append(thread_id)

    # 3. Test History and Analytics Endpoint
    print("\n3. Testing Executive Portfolio Analytics & Application History...")
    hist_res = requests.get(f"{API_BASE_URL}/history", timeout=5).json()
    print(f"   ✅ Applications History DB Records Count: {len(hist_res)}")
    
    # 4. Test Override Functionality on first record
    if hist_res:
        test_thread = hist_res[0]["thread_id"]
        print(f"\n4. Testing Manager Audit Override on Thread: {test_thread}...")
        override_payload = {
            "decision": "APPROVED",
            "justification": "Approved under Zonal Manager Delegation with additional 100% liquid collateral lien."
        }
        ov_res = requests.post(f"{API_BASE_URL}/override/{test_thread}", json=override_payload, timeout=5)
        if ov_res.status_code == 200:
            print("   ✅ Manager Override successfully executed and audited.")
        else:
            print(f"   ❌ Override failed: {ov_res.text}")

    print("\n" + "=" * 80)
    print(f"🎉 Database Seeding & Deep System Testing Completed: {len(seeded_threads)} Applications Active!")
    print("=" * 80)
    return True

if __name__ == "__main__":
    run_deep_system_testing()
