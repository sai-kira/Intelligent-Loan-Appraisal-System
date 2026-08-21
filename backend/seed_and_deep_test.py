"""
Database Seeder & Deep System Verification for Central Bank of India ILAS
Populates benchmark applications into the underwriting queue in 'WAITING_FOR_MANAGER' state
so the Credit Manager can review and approve/reject them in Tab 3.
"""
import sys
import os
import time
import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

BENCHMARK_PROFILES = [
    {
        "name": "Dr. Rajesh Sharma", "age": 42, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 350000, "net_monthly_income": 280000, "total_assets": 25000000,
        "credit_score": 790, "avg_credit_balance_6m": 800000, "existing_emi": 20000, "active_lines": 1, "inquiries_6m": 0,
        "loan_amount": 5000000, "tenure_months": 240, "loan_type": "Home Loan", "property_value": 8500000, "security_type": "Property"
    },
    {
        "name": "Sunita Menon", "age": 36, "gender": "Female", "marital_status": "Single", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 180000, "net_monthly_income": 140000, "total_assets": 9000000,
        "credit_score": 765, "avg_credit_balance_6m": 350000, "existing_emi": 15000, "active_lines": 2, "inquiries_6m": 1,
        "loan_amount": 1200000, "tenure_months": 60, "loan_type": "Auto Loan", "property_value": 1600000, "security_type": "Vehicle"
    },
    {
        "name": "Amitabh Verma", "age": 31, "gender": "Male", "marital_status": "Single", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 140000, "net_monthly_income": 115000, "total_assets": 4500000,
        "credit_score": 750, "avg_credit_balance_6m": 250000, "existing_emi": 8000, "active_lines": 1, "inquiries_6m": 1,
        "loan_amount": 400000, "tenure_months": 36, "loan_type": "Personal Loan", "property_value": 0, "security_type": "None"
    },
    {
        "name": "Pooja Hegde", "age": 23, "gender": "Female", "marital_status": "Single", "category": "OBC",
        "occupation": "Professional", "gross_monthly_income": 80000, "net_monthly_income": 65000, "total_assets": 2000000,
        "credit_score": 730, "avg_credit_balance_6m": 150000, "existing_emi": 0, "active_lines": 0, "inquiries_6m": 0,
        "loan_amount": 2500000, "tenure_months": 84, "loan_type": "Education Loan", "property_value": 3500000, "security_type": "Property"
    },
    {
        "name": "Apex Precision Engineering Pvt Ltd", "age": 48, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 450000, "net_monthly_income": 380000, "total_assets": 18000000,
        "credit_score": 780, "avg_credit_balance_6m": 600000, "existing_emi": 35000, "active_lines": 3, "inquiries_6m": 0,
        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - Existing Unit", "property_value": 8000000, "security_type": "Property",
        "current_ratio": 1.45, "debt_equity_ratio": 1.5, "sales_growth_rate": 22.0, "pat_margin": 16.0,
        "sanction_compliance": "Compliant", "stock_statement_status": "Timely", "debt_servicing_history": "Within 1 month",
        "inventory_compliance": "Fair Compliance", "bills_culture": True, "bill_payment_record": "Prompt",
        "review_documents_timely": True, "lc_bg_status": "Prompt / No Facility", "ancillary_relationship": "Substantial"
    },
    {
        "name": "Surat Silk & Synthetics Mills", "age": 52, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 380000, "net_monthly_income": 290000, "total_assets": 12000000,
        "credit_score": 715, "avg_credit_balance_6m": 400000, "existing_emi": 40000, "active_lines": 3, "inquiries_6m": 1,
        "loan_amount": 4500000, "tenure_months": 60, "loan_type": "MSME Loan - Existing Unit", "property_value": 6500000, "security_type": "Property",
        "current_ratio": 1.25, "debt_equity_ratio": 2.6, "sales_growth_rate": 12.0, "pat_margin": 8.0,
        "sanction_compliance": "Compliant", "stock_statement_status": "Monthly", "debt_servicing_history": "Within 2 months",
        "inventory_compliance": "Fair Compliance", "bills_culture": True, "bill_payment_record": "Prompt",
        "review_documents_timely": True, "lc_bg_status": "Prompt / No Facility", "ancillary_relationship": "Moderate"
    },
    {
        "name": "BioGreen Agro Processing LLP", "age": 39, "gender": "Female", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 400000, "net_monthly_income": 320000, "total_assets": 14000000,
        "credit_score": 755, "avg_credit_balance_6m": 500000, "existing_emi": 20000, "active_lines": 2, "inquiries_6m": 1,
        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - New Unit", "property_value": 6500000, "security_type": "CGTMSE / Plant & Machinery",
        "projected_sales_growth": 18.0, "projected_pat_margin": 14.0, "projected_der": 1.8,
        "inputs_access": "Locally Available / Tied up", "market_access": "Locally Available / Tied up",
        "promoter_experience": "Qualified and Experienced", "bank_relationship": "Existing Customer",
        "premises_type": "Owned", "collateral_coverage": "Covered under CGTMSE Scheme", "cgtmse_covered": True
    },
    {
        "name": "Sunrise Biofuels Startup", "age": 33, "gender": "Male", "marital_status": "Single", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 120000, "net_monthly_income": 85000, "total_assets": 3000000,
        "credit_score": 620, "avg_credit_balance_6m": 100000, "existing_emi": 45000, "active_lines": 4, "inquiries_6m": 3,
        "loan_amount": 5000000, "tenure_months": 60, "loan_type": "MSME Loan - New Unit", "property_value": 2000000, "security_type": "None",
        "projected_sales_growth": 3.0, "projected_pat_margin": 2.0, "projected_der": 4.5,
        "inputs_access": "Not Identified", "market_access": "Unidentified",
        "promoter_experience": "No qualification/experience", "bank_relationship": "Introduced by Govt Dept / Others",
        "premises_type": "Leased / Rented", "collateral_coverage": "Unsecured", "cgtmse_covered": False
    },
    {
        "name": "Defaulter Steels LLP", "age": 50, "gender": "Male", "marital_status": "Married", "category": "GEN",
        "occupation": "Business", "gross_monthly_income": 300000, "net_monthly_income": -250000, "total_assets": 5000000,
        "credit_score": 550, "avg_credit_balance_6m": 10000, "existing_emi": 80000, "active_lines": 5, "inquiries_6m": 4,
        "loan_amount": 3000000, "tenure_months": 48, "loan_type": "MSME Loan - Existing Unit", "property_value": 4000000, "security_type": "Property",
        "current_ratio": 0.90, "debt_equity_ratio": 4.5, "sales_growth_rate": -5.0, "pat_margin": -2.0,
        "sanction_compliance": "Non-compliant", "stock_statement_status": "Non-Submission", "debt_servicing_history": "Overdue > 3 months",
        "inventory_compliance": "High deviation", "bills_culture": False, "bill_payment_record": "Overdue > 3 months",
        "review_documents_timely": False, "lc_bg_status": "Devolvement / Invocation", "ancillary_relationship": "None"
    },
    {
        "name": "Vikas High-FOIR Retail", "age": 29, "gender": "Male", "marital_status": "Single", "category": "GEN",
        "occupation": "Salaried", "gross_monthly_income": 50000, "net_monthly_income": 40000, "total_assets": 1000000,
        "credit_score": 680, "avg_credit_balance_6m": 25000, "existing_emi": 30000, "active_lines": 3, "inquiries_6m": 2,
        "loan_amount": 3000000, "tenure_months": 120, "loan_type": "Home Loan", "property_value": 3200000, "security_type": "Property"
    }
]

def seed_applications():
    print("=" * 80)
    print("🏦 Central Bank of India ILAS - Seeding Underwriting Pipeline")
    print("=" * 80)
    
    seeded_threads = []
    
    for idx, p in enumerate(BENCHMARK_PROFILES, 1):
        print(f"[{idx}/{len(BENCHMARK_PROFILES)}] Ingesting & Appraising: {p['name']} ({p['loan_type']})...")
        apply_res = requests.post(f"{API_BASE_URL}/apply", json=p, timeout=10).json()
        thread_id = apply_res.get("thread_id")
        if not thread_id:
            print(f"   ❌ Failed to submit {p['name']}: {apply_res}")
            continue
            
        # Poll for completion into WAITING_FOR_MANAGER
        for _ in range(30):
            time.sleep(1)
            s_res = requests.get(f"{API_BASE_URL}/status/{thread_id}", timeout=5).json()
            if s_res.get("status") in ["WAITING_FOR_MANAGER", "COMPLETED"]:
                print(f"   ✅ AI Multi-Agent Appraisal Complete -> State: {s_res.get('status')} | Recommendation: {s_res.get('decision_outcome')}")
                break
                
        seeded_threads.append(thread_id)

    # Approve 3 applications so History & Portfolio Analytics has historical data, leave the other 7 in Active Pipeline!
    if len(seeded_threads) >= 3:
        requests.post(f"{API_BASE_URL}/approve/{seeded_threads[0]}", json={"decision": "APPROVED"})
        requests.post(f"{API_BASE_URL}/approve/{seeded_threads[1]}", json={"decision": "APPROVED"})
        requests.post(f"{API_BASE_URL}/approve/{seeded_threads[7]}", json={"decision": "REJECTED"})
        print("\n✅ Processed 3 historical applications for analytics baseline; 7 applications left pending in Active Underwriting Pipeline for Manager approval.")

    print(f"\n🎉 Successfully seeded {len(seeded_threads)} applications!")

if __name__ == "__main__":
    seed_applications()
