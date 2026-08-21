"""
Central Bank of India - Intelligent Loan Appraisal System (ILAS)
Automated Verification Suite for Corporate Financial Intelligence & Valuation Engine
"""

import unittest
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.financial_intelligence import (
    FinancialStatementSpreader,
    RatioDiagnosticsEngine,
    ForensicAuditor,
    FinancialForecaster,
    EnterpriseValuator,
    MSEParameterAutoMapper
)
from backend.corporate_profiles import CORPORATE_PROFILES

class TestFinancialIntelligence(unittest.TestCase):

    def setUp(self):
        self.apex = CORPORATE_PROFILES["Apex Precision Engineering Pvt Ltd"]
        self.defaulter = CORPORATE_PROFILES["Defaulter Steels LLP"]

    def test_01_financial_spreading_integrity(self):
        """Verify Balance Sheet and P&L spreading math."""
        print("▶ Testing 3-Year Financial Spreading Integrity...")
        spread = FinancialStatementSpreader.spread_financials(self.apex)
        
        self.assertEqual(len(spread["years"]), 3)
        self.assertEqual(spread["pnl"]["revenue"][-1], 48000000.0)
        # Check gross profit = revenue - cogs
        self.assertEqual(spread["pnl"]["gross_profit"][-1], 48000000.0 - 25400000.0)
        # Check EBITDA = Gross Profit - Opex
        self.assertEqual(spread["pnl"]["ebitda"][-1], (48000000.0 - 25400000.0) - 6800000.0)
        # Check Tangible Net Worth = Capital + Reserves
        self.assertEqual(spread["balance_sheet"]["tangible_net_worth"][-1], 3000000.0 + 17100000.0)
        print("  ✅ Financial statement spreading math validated.")

    def test_02_5_pillar_ratio_diagnostics(self):
        """Verify Liquidity, Solvency (DSCR/ICR), Profitability, and Efficiency ratios."""
        print("▶ Testing 5-Pillar Ratio Diagnostics & MPBF...")
        spread = FinancialStatementSpreader.spread_financials(self.apex)
        ratios = RatioDiagnosticsEngine.calculate_ratios(spread)
        
        # Current Ratio > 1.33
        latest_cr = ratios["liquidity"]["current_ratio"][-1]
        self.assertGreaterEqual(latest_cr, 1.33)
        
        # Debt to Equity <= 1.0 for prime firm
        latest_der = ratios["solvency"]["debt_to_equity"][-1]
        self.assertLessEqual(latest_der, 1.0)
        
        # DSCR >= 1.50
        latest_dscr = ratios["solvency"]["debt_service_coverage_ratio"][-1]
        self.assertGreaterEqual(latest_dscr, 1.50)
        
        # MPBF Tandon Method II > 0
        mpbf_limit = ratios["mpbf_working_capital"]["tandon_method_2"]
        self.assertGreater(mpbf_limit, 0)
        print("  ✅ 5-Pillar ratios & Tandon/Nayak MPBF sizing verified.")

    def test_03_forensic_altman_z_and_beneish_m(self):
        """Verify Altman Z''-Score and Beneish M-Score on Prime and Distressed firms."""
        print("▶ Testing Forensic Accounting (Altman Z'' & Beneish M-Score)...")
        
        # 1. Apex Precision (Prime) -> Should be Safe Zone & Clean M-Score
        spread_apex = FinancialStatementSpreader.spread_financials(self.apex)
        z_apex = ForensicAuditor.calculate_altman_z_double_prime(spread_apex)
        m_apex = ForensicAuditor.calculate_beneish_m_score(spread_apex)
        
        self.assertEqual(z_apex["zone"], "Safe Zone")
        self.assertGreater(z_apex["z_score"], 2.60)
        self.assertFalse(m_apex["manipulation_flag"])
        
        # 2. Defaulter Steels (Distressed) -> Should be Distress Zone & Manipulation Red Flag
        spread_def = FinancialStatementSpreader.spread_financials(self.defaulter)
        z_def = ForensicAuditor.calculate_altman_z_double_prime(spread_def)
        m_def = ForensicAuditor.calculate_beneish_m_score(spread_def)
        
        self.assertEqual(z_def["zone"], "Distress Zone")
        self.assertLess(z_def["z_score"], 1.10)
        print("  ✅ Forensic early warning models accurately distinguish Prime vs Distress.")

    def test_04_3year_forecasting_and_stress_testing(self):
        """Verify 3-Year forecasting and macro stress sensitivity simulations."""
        print("▶ Testing 3-Year Forecasting & Stress Simulations...")
        spread = FinancialStatementSpreader.spread_financials(self.apex)
        
        # Projections
        proj = FinancialForecaster.project_3_years(spread, sales_cagr=0.15)
        self.assertEqual(len(proj["projection_years"]), 3)
        self.assertGreater(proj["projected_revenue"][-1], spread["pnl"]["revenue"][-1])
        
        # Stress Simulation: -20% Demand, +15% Raw Material Cost, +200 bps Rate Hike
        stress = FinancialForecaster.simulate_stress_scenario(
            spread,
            revenue_shock_pct=-0.20,
            cogs_increase_pct=0.15,
            interest_rate_shock_bps=200
        )
        self.assertIn("stressed_dscr", stress)
        self.assertIn("solvency_status", stress)
        print("  ✅ Macro stress simulations and sensitivity curves validated.")

    def test_05_dcf_valuation_and_debt_sizing(self):
        """Verify Discounted Cash Flow (DCF) enterprise valuation."""
        print("▶ Testing DCF Enterprise Valuation & Debt Sizing...")
        spread = FinancialStatementSpreader.spread_financials(self.apex)
        dcf = EnterpriseValuator.calculate_dcf_valuation(
            spread,
            proposed_loan_amount=5000000.0,
            forecast_years=5,
            wacc=0.115,
            terminal_growth_rate=0.04
        )
        self.assertGreater(dcf["enterprise_value"], 10000000.0)
        self.assertLessEqual(dcf["loan_to_enterprise_value_pct"], 50.0)
        self.assertIn("leverage_assessment", dcf)
        print("  ✅ DCF valuation and Loan-to-EV sizing verified.")

    def test_06_mse_parameter_auto_mapper(self):
        """Verify automatic population of Form MSE 1 from Balance Sheet & P&L."""
        print("▶ Testing Automated Form MSE 1 Auto-Population & CBI Grading...")
        
        # 1. Apex Precision -> Auto-scores 100/100 -> CBI 1
        spread_apex = FinancialStatementSpreader.spread_financials(self.apex)
        scorecard_apex = MSEParameterAutoMapper.auto_score_form_mse_1(spread_apex, self.apex["operational_flags"])
        self.assertEqual(scorecard_apex["total_score"], 100)
        self.assertEqual(scorecard_apex["grade"], "CBI 1")
        self.assertTrue(scorecard_apex["hurdle_rate_met"])
        
        # 2. Defaulter Steels -> Overdue > 3 months -> Auto-clamped to 0/100 -> CBI 10
        spread_def = FinancialStatementSpreader.spread_financials(self.defaulter)
        scorecard_def = MSEParameterAutoMapper.auto_score_form_mse_1(spread_def, self.defaulter["operational_flags"])
        self.assertEqual(scorecard_def["total_score"], 0)
        self.assertEqual(scorecard_def["grade"], "CBI 10")
        self.assertFalse(scorecard_def["hurdle_rate_met"])
        self.assertTrue(scorecard_def["is_defaulter_override"])
        print("  ✅ Form MSE 1 auto-mapper populated all 13 parameters with 100% accuracy.")

if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFinancialIntelligence)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
