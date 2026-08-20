def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """
    Calculates the Equated Monthly Installment (EMI) for a loan.
    Formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    
    if annual_rate == 0:
        return principal / tenure_months
        
    monthly_rate = (annual_rate / 100) / 12
    emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    return round(emi, 2)

def calculate_foir(existing_obligations: float, new_emi: float, gross_monthly_income: float) -> float:
    """
    Calculates the Fixed Obligation to Income Ratio (FOIR).
    Formula: (Existing EMIs + New EMI) / Gross Monthly Income
    """
    if gross_monthly_income <= 0:
        return 999.99 # Max cap risk if no income
    
    total_obligations = existing_obligations + new_emi
    foir = (total_obligations / gross_monthly_income) * 100
    return round(foir, 2)

def check_ltv_compliance(loan_amount: float, property_value: float, loan_type: str = "Home Loan") -> dict:
    """
    Checks if the Loan-to-Value (LTV) ratio complies with RBI/CBoI norms.
    """
    if loan_type == "Personal Loan" or "Unsecured" in loan_type:
        return {"compliant": True, "ltv": 0.0, "max_allowed": 0.0, "reason": "Unsecured loan - LTV Not Applicable (Compliant)"}
        
    if property_value <= 0:
        return {"compliant": False, "ltv": 0.0, "max_allowed": 0.0, "reason": "Property/Collateral value must be > 0 for secured loans"}
        
    ltv = (loan_amount / property_value) * 100
    
    if loan_type == "Home Loan":
        if loan_amount <= 3_000_000:
            max_allowed = 90.0
        elif loan_amount <= 7_500_000:
            max_allowed = 80.0
        else:
            max_allowed = 75.0
    elif loan_type == "Gold Loan":
        max_allowed = 75.0
    else:
        # Generic fallback for other secured loans
        max_allowed = 80.0
        
    is_compliant = ltv <= max_allowed
    
    reason = "Compliant" if is_compliant else f"LTV of {ltv:.2f}% exceeds the maximum allowed {max_allowed}% for {loan_type}s."
    
    return {
        "compliant": is_compliant,
        "ltv": round(ltv, 2),
        "max_allowed": max_allowed,
        "reason": reason
    }
