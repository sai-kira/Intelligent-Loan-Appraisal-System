from calculators import calculate_emi, calculate_foir, check_ltv_compliance

def test_calculators():
    print("Testing EMI (10L loan, 8% interest, 10 years)")
    emi = calculate_emi(1_000_000, 8.0, 120)
    print(f"EMI: {emi}") # Expected: ~12132
    
    print("\nTesting FOIR (Gross 70k, Existing 10k, New EMI 15k)")
    foir = calculate_foir(10000, 15000, 70000)
    print(f"FOIR: {foir}%") # Expected: 35.71%
    
    print("\nTesting LTV - Home Loan 50L loan on 60L property")
    ltv_res = check_ltv_compliance(5_000_000, 6_000_000)
    print(f"LTV Result: {ltv_res}") # Should be 83.33%, which exceeds 80% limit.
    
    print("\nTesting LTV - Home Loan 20L loan on 25L property")
    ltv_res2 = check_ltv_compliance(2_000_000, 2_500_000)
    print(f"LTV Result: {ltv_res2}") # Should be 80.0%, allowed is 90%.

if __name__ == "__main__":
    test_calculators()
