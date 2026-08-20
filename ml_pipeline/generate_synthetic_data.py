import pandas as pd
import numpy as np
import os
import scipy.stats as stats

# Set random seed for reproducibility
np.random.seed(42)

def generate_synthetic_cboi_data(num_records=5000, output_dir="data"):
    """
    Generates synthetic loan application data modeling the CBoI Common Application 
    and the GR9 Synthetic Loan Data Generation Strategy document.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating {num_records} synthetic loan records across multiple tables...")
    
    # --- 1. RETAIL LOAN CUSTOMERS (Applicant & Income Details) ---
    customer_ids = [f"RET-{str(i).zfill(5)}" for i in range(1, num_records + 1)]
    
    # Age: Normal dist truncated 21 to 65
    ages = np.clip(np.random.normal(38, 10, num_records), 21, 65).astype(int)
    genders = np.random.choice(['M', 'F'], size=num_records, p=[0.7, 0.3])
    marital_status = np.random.choice(['Married', 'Unmarried'], size=num_records, p=[0.65, 0.35])
    categories = np.random.choice(['GEN', 'OBC', 'SC', 'ST', 'Minority'], size=num_records, p=[0.5, 0.25, 0.1, 0.05, 0.1])
    
    # Occupations
    occupations = np.random.choice(['Salaried', 'Self-Employed Professional', 'Self-Employed Non-Professional'], size=num_records, p=[0.6, 0.2, 0.2])
    
    # Gross Income: Log-Normal distribution (as per GR9)
    # Mean log roughly 11.5 (approx 1 lakh), right skewed
    gross_monthly_income = np.random.lognormal(mean=11.2, sigma=0.6, size=num_records)
    gross_monthly_income = np.clip(gross_monthly_income, 25000, 500000).round(-3)
    
    # Statutory Deductions (approx 10-20% of gross for salaried, less for self-employed)
    deduction_rates = np.where(occupations == 'Salaried', np.random.uniform(0.1, 0.25, num_records), np.random.uniform(0.05, 0.15, num_records))
    monthly_deductions = (gross_monthly_income * deduction_rates).round(-3)
    net_monthly_income = gross_monthly_income - monthly_deductions
    
    # Average Credit Balance (Bank Accounts)
    avg_credit_balance = (net_monthly_income * np.random.uniform(0.5, 3.0, num_records)).round(-3)
    
    customers_df = pd.DataFrame({
        'CUSTOMER_ID': customer_ids,
        'AGE': ages,
        'GENDER': genders,
        'MARITAL_STATUS': marital_status,
        'CATEGORY': categories,
        'OCCUPATION': occupations,
        'GROSS_MONTHLY_INC': gross_monthly_income,
        'MONTHLY_DEDUCTIONS': monthly_deductions,
        'NET_MONTHLY_INC': net_monthly_income,
        'AVG_CREDIT_BAL_6M': avg_credit_balance
    })
    
    # --- 2. CREDIT BUREAU INFORMATION ---
    # Credit Score: Beta distribution shifted to 300-900 (as per GR9)
    # Parameters chosen to skew towards higher scores (~750)
    beta_samples = np.random.beta(a=5, b=2, size=num_records)
    credit_scores = 300 + (beta_samples * 600)
    credit_scores = np.clip(credit_scores, 300, 900).astype(int)
    
    bureau_df = pd.DataFrame({
        'BUREAU_ID': [f"BUR-{str(i).zfill(5)}" for i in range(1, num_records + 1)],
        'CUSTOMER_ID': customer_ids,
        'CREDIT_SCORE': credit_scores,
        'ACTIVE_LINES': np.random.poisson(lam=2, size=num_records),
        'INQUIRIES_6M': np.random.poisson(lam=0.5, size=num_records)
    })
    
    # --- 3. EXISTING LIABILITIES & ASSETS (Other Borrowings) ---
    # Existing EMI (correlated with income, 0 to 40% FOIR)
    existing_emi_ratios = np.random.uniform(0, 0.4, size=num_records)
    existing_emis = (gross_monthly_income * existing_emi_ratios).round(-3)
    
    # Total Assets (Cash, deposits, immovable properties)
    total_assets = (gross_monthly_income * 12 * np.random.uniform(1.5, 10.0, num_records)).round(-4)
    
    liabilities_assets_df = pd.DataFrame({
        'CUSTOMER_ID': customer_ids,
        'EXISTING_EMI': existing_emis,
        'TOTAL_ASSETS': total_assets,
        'TOTAL_OBLIGATIONS': existing_emis * np.random.uniform(10, 36, num_records) # Guessing remaining debt
    })
    
    # --- 4. LOAN MASTER ---
    loan_ids = [f"LN-HM-{str(i).zfill(5)}" for i in range(1, num_records + 1)]
    loan_types = np.random.choice(['Home Loan', 'Personal Loan', 'Vehicle Loan'], size=num_records, p=[0.5, 0.3, 0.2])
    
    # Base Loan amounts conditionally linked to Income (as per GR9)
    # Example: Home loans = 30-60x monthly income, Personal = 5-15x, Vehicle = 10-20x
    multipliers = np.where(loan_types == 'Home Loan', np.random.uniform(30, 60, num_records),
                  np.where(loan_types == 'Personal Loan', np.random.uniform(5, 15, num_records),
                           np.random.uniform(10, 20, num_records)))
    
    sanction_amounts = (gross_monthly_income * multipliers).round(-4)
    
    # Tenures
    tenures = np.where(loan_types == 'Home Loan', np.random.choice([120, 180, 240, 300], num_records),
              np.where(loan_types == 'Personal Loan', np.random.choice([12, 24, 36, 48, 60], num_records),
                       np.random.choice([36, 48, 60, 72, 84], num_records)))
    
    # Interest rates (repo linked, e.g. 8.5% to 14% based on product)
    int_rates = np.where(loan_types == 'Home Loan', np.random.uniform(8.5, 9.5, num_records),
                np.where(loan_types == 'Personal Loan', np.random.uniform(11.0, 14.0, num_records),
                         np.random.uniform(9.0, 11.0, num_records)))
                         
    loan_master_df = pd.DataFrame({
        'LOAN_ID': loan_ids,
        'CUSTOMER_ID': customer_ids,
        'LOAN_TYPE': loan_types,
        'SANCTION_AMT': sanction_amounts,
        'INT_RATE': int_rates.round(2),
        'TENURE_MTHS': tenures
    })
    
    # --- 5. COLLATERAL (Required for Home/Vehicle loans) ---
    collateral_ids = [f"COL-{str(i).zfill(5)}" for i in range(1, num_records + 1)]
    
    # Property values generated such that LTV is mostly compliant but some are outliers
    # LTV usually 70-90%
    ltv_ratios = np.random.uniform(0.65, 0.95, num_records)
    assessed_values = np.where(loan_types == 'Personal Loan', 0, (sanction_amounts / ltv_ratios).round(-4))
    
    collateral_df = pd.DataFrame({
        'COLLATERAL_ID': collateral_ids,
        'LOAN_ID': loan_ids,
        'SECURITY_TYPE': np.where(loan_types == 'Home Loan', 'Mortgage', np.where(loan_types == 'Vehicle Loan', 'Hypothecation', 'None')),
        'ASSESSED_VAL': assessed_values
    })
    
    # --- 6. TARGET VARIABLES (Risk Scores & Approvals as per GR9 Part 5) ---
    # We create a PD (Probability of Default) logic mimicking a real ML model.
    # Higher EMI/NMI, Higher LTV, Lower CIBIL = High Risk.
    
    # Calculate Proposed EMI
    r = loan_master_df['INT_RATE'] / (12 * 100)
    n = loan_master_df['TENURE_MTHS']
    p = loan_master_df['SANCTION_AMT']
    proposed_emis = (p * r * (1 + r)**n) / ((1 + r)**n - 1)
    
    total_emis = liabilities_assets_df['EXISTING_EMI'] + proposed_emis
    foir = (total_emis / customers_df['GROSS_MONTHLY_INC']) # Fixed Obligation to Income Ratio
    
    # Simulated PD logic (0.0 to 1.0)
    pd_scores = np.zeros(num_records)
    
    # Penalty for low credit score
    pd_scores += np.where(bureau_df['CREDIT_SCORE'] < 600, 0.4, 0.0)
    pd_scores += np.where((bureau_df['CREDIT_SCORE'] >= 600) & (bureau_df['CREDIT_SCORE'] < 700), 0.15, 0.0)
    pd_scores -= np.where(bureau_df['CREDIT_SCORE'] > 750, 0.1, 0.0) # Bonus
    
    # Penalty for high FOIR (over 50%)
    pd_scores += np.where(foir > 0.50, 0.3, 0.0)
    pd_scores += np.where(foir > 0.65, 0.2, 0.0)
    
    # Penalty for high LTV (over 80% for Home Loans)
    actual_ltvs = np.where(collateral_df['ASSESSED_VAL'] > 0, (loan_master_df['SANCTION_AMT'] / collateral_df['ASSESSED_VAL']), 0)
    pd_scores += np.where((loan_types == 'Home Loan') & (actual_ltvs > 0.80), 0.2, 0.0)
    
    # Random noise (Stochastic noise term from GR9)
    pd_scores += np.random.normal(0.05, 0.05, num_records)
    pd_scores = np.clip(pd_scores, 0.0, 1.0)
    
    # Officer Decisions (Approve/Reject)
    # Approve: PD < 20% and FOIR < 50%
    # Reject: PD > 40% OR Credit Score < 600 OR FOIR > 55%
    decisions = []
    default_status = [] # The actual Y target for ML to predict
    
    for i in range(num_records):
        pd_val = pd_scores[i]
        foir_val = foir.iloc[i]
        cibil = bureau_df['CREDIT_SCORE'].iloc[i]
        
        # Real-world Default outcome based on PD probability
        is_default = 1 if np.random.rand() < pd_val else 0
        default_status.append(is_default)
        
        if pd_val > 0.40 or cibil < 600 or foir_val > 0.55:
            decisions.append('Reject')
        elif pd_val < 0.20 and foir_val < 0.50:
            decisions.append('Approve')
        else:
            decisions.append('Review')
            
    risk_df = pd.DataFrame({
        'LOAN_ID': loan_ids,
        'SIMULATED_PD': pd_scores.round(4),
        'OFFICER_DECISION': decisions,
        'DEFAULT_STATUS': default_status, # ML Target Variable
        'CALCULATED_FOIR': foir.round(4),
        'CALCULATED_LTV': actual_ltvs.round(4)
    })
    
    # Save all files
    customers_df.to_csv(f"{output_dir}/customers.csv", index=False)
    bureau_df.to_csv(f"{output_dir}/bureau.csv", index=False)
    liabilities_assets_df.to_csv(f"{output_dir}/liabilities_assets.csv", index=False)
    loan_master_df.to_csv(f"{output_dir}/loan_master.csv", index=False)
    collateral_df.to_csv(f"{output_dir}/collateral.csv", index=False)
    risk_df.to_csv(f"{output_dir}/risk_labels.csv", index=False)
    
    print(f"Generated {len(customers_df)} records.")
    print(f"Overall Default Rate: {np.mean(default_status) * 100:.2f}%")
    print(f"Data saved to {output_dir}/ directory.")

if __name__ == "__main__":
    generate_synthetic_cboi_data(num_records=10000)
