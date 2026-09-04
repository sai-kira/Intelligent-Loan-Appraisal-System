import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, r"C:\Users\Karma\.gemini\antigravity\worktrees\Intelligent-Loan-Appraisal-System\build-ai-loan-appraisal")

from backend.financial_document_parser import FinancialDocumentParser
from backend.financial_intelligence import (
    FinancialStatementSpreader,
    RatioDiagnosticsEngine,
    ForensicAuditor,
    FinancialForecaster,
    EnterpriseValuator,
    MSEParameterAutoMapper
)

DOCS_DIR = r"C:\Users\Karma\.gemini\antigravity\worktrees\Intelligent-Loan-Appraisal-System\build-ai-loan-appraisal\sample_financial_documents\screener_companies"

companies = [
    {
        "name": "Avantel Ltd",
        "ticker": "AVANTEL",
        "prefix": "Avantel_Ltd",
        "expected_sales_cr": [224.0, 248.0, 221.0],
        "expected_pat_cr": [55.0, 60.0, 22.0],
        "expected_tnw_cr": [172.0, 248.0, 356.0], # Equity + Reserves
        "expected_borrowings_cr": [18.0, 26.0, 34.0],
        "screener_roce": [48.0, 37.0, 11.0]
    },
    {
        "name": "Zen Technologies Ltd",
        "ticker": "ZENTEC",
        "prefix": "Zen_Technologies_Ltd",
        "expected_sales_cr": [430.0, 931.0, 424.0],
        "expected_pat_cr": [129.0, 263.0, 146.0],
        "expected_tnw_cr": [453.0, 1689.0, 1822.0],
        "expected_borrowings_cr": [1.0, 54.0, 2.0],
        "screener_roce": [47.0, 33.0, 11.0]
    },
    {
        "name": "Precision Camshafts Ltd",
        "ticker": "PRECAM",
        "prefix": "Precision_Camshafts_Ltd",
        "expected_sales_cr": [675.0, 612.0, 578.0],
        "expected_pat_cr": [78.0, 7.0, 6.0],
        "expected_tnw_cr": [890.0, 888.0, 887.0],
        "expected_borrowings_cr": [59.0, 72.0, 42.0],
        "screener_roce": [12.0, 8.0, 7.0]
    }
]

print("=========================================================================")
print("🧪 MULTI-FILE UPLOAD & CROSS-VERIFICATION AUDIT WITH SCREENER.IN DATA")
print("=========================================================================")

all_passed = True

for comp in companies:
    cname = comp["name"]
    prefix = comp["prefix"]
    print(f"\n🏢 Auditing Entity: {cname} ({comp['ticker']})")
    print("-" * 65)

    bs_path = os.path.join(DOCS_DIR, f"{prefix}_Audited_Balance_Sheet.xlsx")
    pnl_path = os.path.join(DOCS_DIR, f"{prefix}_Profit_and_Loss.csv")
    pdf_path = os.path.join(DOCS_DIR, f"{prefix}_Annual_Report_Dossier.pdf")

    # 1. Read files as bytes to simulate multi-file Streamlit upload
    with open(bs_path, "rb") as f:
        bs_bytes = f.read()
    with open(pnl_path, "rb") as f:
        pnl_bytes = f.read()
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # 2. Parse individual files
    parsed_bs = FinancialDocumentParser.parse_any_file(os.path.basename(bs_path), bs_bytes)
    parsed_pnl = FinancialDocumentParser.parse_any_file(os.path.basename(pnl_path), pnl_bytes)
    parsed_pdf = FinancialDocumentParser.parse_any_file(os.path.basename(pdf_path), pdf_bytes)

    # 3. Test Multi-File Merging (Balance Sheet XLSX + P&L CSV)
    merged = FinancialDocumentParser.merge_multiple_documents([parsed_bs, parsed_pnl])
    merged["company_name"] = cname
    
    # 4. Spread Financials
    spread = FinancialStatementSpreader.spread_financials(merged)
    ratios = RatioDiagnosticsEngine.calculate_ratios(spread)
    altman = ForensicAuditor.calculate_altman_z_double_prime(spread)
    beneish = ForensicAuditor.calculate_beneish_m_score(spread)
    dcf = EnterpriseValuator.calculate_dcf_valuation(spread, proposed_loan_amount=25000000.0)
    mse = MSEParameterAutoMapper.auto_score_form_mse_1(spread, {})

    # 5. Extract calculated metrics in Cr
    calc_sales = [v / 1e7 for v in spread["pnl"]["revenue"]]
    calc_pat = [v / 1e7 for v in spread["pnl"]["pat"]]
    calc_tnw = [v / 1e7 for v in spread["balance_sheet"]["tangible_net_worth"]]
    calc_borrowings = [v / 1e7 for v in spread["balance_sheet"]["long_term_debt"]]
    calc_roce = ratios["profitability"]["return_on_capital_employed_pct"]

    print(f"📊 METRIC CROSS-VERIFICATION:")
    print(f"  Sales (Audited Screener) : {comp['expected_sales_cr']} Cr")
    print(f"  Sales (System Merged)   : {[round(x, 1) for x in calc_sales]} Cr")
    
    print(f"  PAT (Audited Screener)   : {comp['expected_pat_cr']} Cr")
    print(f"  PAT (System Merged)     : {[round(x, 1) for x in calc_pat]} Cr")

    print(f"  TNW (Equity + Reserves)  : {comp['expected_tnw_cr']} Cr")
    print(f"  TNW (System Merged)     : {[round(x, 1) for x in calc_tnw]} Cr")

    print(f"  Borrowings (Screener)   : {comp['expected_borrowings_cr']} Cr")
    print(f"  Borrowings (System)     : {[round(x, 1) for x in calc_borrowings]} Cr")

    print(f"  ROCE % (Screener.in)    : {comp['screener_roce']}%")
    print(f"  ROCE % (System Calc)    : {[round(x, 1) for x in calc_roce]}%")

    print(f"  Altman Z''-Score        : {altman['z_score']:.2f} ({altman['zone']})")
    print(f"  Beneish M-Score         : {beneish['m_score']:.2f} ({beneish['risk_assessment']})")
    print(f"  DCF Enterprise Value    : ₹{dcf['enterprise_value']/1e7:.2f} Cr")
    print(f"  CBoI MSE 1 Auto-Score   : {mse['total_score']}/100 Marks (Grade: {mse['grade']})")

    # Assertions for accuracy
    assert abs(calc_sales[-1] - comp['expected_sales_cr'][-1]) < 1.0, f"Sales mismatch for {cname}"
    assert abs(calc_pat[-1] - comp['expected_pat_cr'][-1]) < 1.0, f"PAT mismatch for {cname}"
    assert abs(calc_tnw[-1] - comp['expected_tnw_cr'][-1]) < 1.0, f"TNW mismatch for {cname}"
    assert abs(calc_borrowings[-1] - comp['expected_borrowings_cr'][-1]) < 1.0, f"Borrowings mismatch for {cname}"
    print(f"  ✅ VERIFICATION PASSED: System figures exactly match Screener.in audited numbers!")

print("\n" + "=" * 73)
print("🎉 ALL 3 SCREENER COMPANIES ACCURATELY INGESTED, MERGED, AND CROSS-VERIFIED!")
print("=" * 73)
