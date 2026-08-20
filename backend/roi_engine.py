def get_applicable_roi(loan_type: str, credit_score: int, mse_grade: str = "Grade B", cgtmse_covered: bool = False) -> float:
    """
    Returns the official Bank Interest Rate (ROI) based on the 
    'ROI FOR RETAIL AND MSME ADVANCES AS ON 01.07.2026' master circular.
    """
    
    # Handle missing or invalid credit scores gracefully
    if not isinstance(credit_score, (int, float)) or credit_score < 300:
        credit_score = 300
        
    if loan_type == "Home Loan":
        if credit_score >= 800:
            return 7.20
        elif 775 <= credit_score <= 799:
            return 7.40
        elif 750 <= credit_score <= 774:
            return 7.90
        elif 725 <= credit_score <= 749:
            return 8.70
        elif 700 <= credit_score <= 724:
            return 8.75
        else:
            return 9.00 # High Risk Penalty Rate
            
    elif loan_type == "Auto Loan":
        if credit_score >= 800:
            return 7.65
        elif 775 <= credit_score <= 799:
            return 7.95
        elif 750 <= credit_score <= 774:
            return 8.20
        elif 725 <= credit_score <= 749:
            return 9.05
        elif 700 <= credit_score <= 724:
            return 9.25
        else:
            return 9.50 # High Risk Penalty Rate
            
    elif loan_type == "Personal Loan":
        # Cent Personal Loan is a flat 11.25% (RBLR 8.25 + LR 3.00)
        return 11.25
        
    elif loan_type == "Education Loan":
        # Education loans to Students-A category with collateral is RBLR-0.35% = 7.90%
        return 7.90
        
    elif "MSME" in loan_type:
        # Official CBoI MSME Lending Matrix as on 01.07.2026 based on CBI Risk Grades
        grade_upper = str(mse_grade).upper().strip()
        
        if grade_upper in ["CBI 1", "CBI 2"]:
            rate = 8.40 if credit_score >= 775 else 8.65
        elif grade_upper == "CBI 3" or grade_upper == "GRADE A":
            rate = 8.65 if credit_score >= 750 else 8.75
        elif grade_upper in ["CBI 4", "CBI 5"]:
            rate = 8.90 if credit_score >= 725 else 9.10
        elif grade_upper == "CBI 6" or grade_upper == "GRADE B":
            rate = 9.25 if credit_score >= 700 else 9.35
        elif grade_upper in ["CBI 7", "CBI 8"]:
            rate = 9.65 if credit_score >= 680 else 10.15
        elif grade_upper in ["CBI 9", "CBI 10", "GRADE C"]:
            rate = 12.65
        else:
            rate = 9.35 # Fallback standard

        # 25 bps concession if backed by CGTMSE Credit Guarantee
        if cgtmse_covered:
            rate -= 0.25
        return round(rate, 2)

    else:
        # Fallback generic rate
        return 8.50
