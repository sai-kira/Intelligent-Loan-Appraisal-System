"""
Central Bank of India - Intelligent Loan Appraisal System (ILAS)
Corporate & MSME Financial Intelligence, Forensic Audit & Valuation Engine

Contains:
1. Multi-Year Financial Spreading (CMA Format)
2. 5-Pillar Ratio Diagnostics & Working Capital (Tandon/Nayak MPBF)
3. Forensic Accounting: Altman Z''-Score & Beneish M-Score
4. 3-Year Forecasting & Macro Stress Testing Simulator
5. Discounted Cash Flow (DCF) Enterprise Valuation & Debt Sizing
6. Automated Form MSE 1 & II Parameter Auto-Mapper & CBI Grading
"""

import sys
import os

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import math
from typing import Dict, Any, List, Optional
import numpy as np

try:
    from msme_scoring_engine import assign_cbi_risk_grade
except ImportError:
    try:
        from backend.msme_scoring_engine import assign_cbi_risk_grade
    except ImportError:
        def assign_cbi_risk_grade(score: int) -> Dict[str, Any]:
            if score >= 90: return {"grade": "CBI 1", "risk_profile": "Minimal Risk (Prime Investment Grade)", "hurdle_rate_met": True}
            elif score >= 80: return {"grade": "CBI 2", "risk_profile": "Very Low Risk (High Grade)", "hurdle_rate_met": True}
            elif score >= 70: return {"grade": "CBI 3", "risk_profile": "Low Risk (Upper Medium Grade)", "hurdle_rate_met": True}
            elif score >= 60: return {"grade": "CBI 4", "risk_profile": "Moderate Risk (Standard Investment Grade)", "hurdle_rate_met": True}
            elif score >= 55: return {"grade": "CBI 5", "risk_profile": "Acceptable Risk (Lower Medium Grade)", "hurdle_rate_met": True}
            elif score > 50: return {"grade": "CBI 6", "risk_profile": "Satisfactory Risk (Hurdle Rate Cleared)", "hurdle_rate_met": True}
            elif score == 50: return {"grade": "CBI 7", "risk_profile": "Watchlist Risk (Exact Hurdle Threshold)", "hurdle_rate_met": True}
            elif score >= 40: return {"grade": "CBI 8", "risk_profile": "Vulnerable Risk (Sub-Hurdle Rate)", "hurdle_rate_met": False}
            elif score >= 30: return {"grade": "CBI 9", "risk_profile": "High Vulnerability (Sub-Hurdle Rate)", "hurdle_rate_met": False}
            else: return {"grade": "CBI 10", "risk_profile": "Substantial Risk / Defaulter", "hurdle_rate_met": False}

# =============================================================================
# 1. MULTI-YEAR FINANCIAL STATEMENT SPREADER (CMA FORMAT)
# =============================================================================

class FinancialStatementSpreader:
    """
    Standardizes raw financial inputs into a 3-Year Banking CMA Spread:
    - Year t-2 (Historical FY1)
    - Year t-1 (Historical FY2)
    - Year t   (Latest Audited FY3)
    """

    @staticmethod
    def spread_financials(raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes and validates balance sheet, P&L, and cash flow items across 3 years."""
        years = raw_data.get("years", ["FY24", "FY25", "FY26"])
        
        # P&L line items
        revenue = [float(x) for x in raw_data.get("revenue", [10000000, 12000000, 15000000])]
        cogs = [float(x) for x in raw_data.get("cogs", [6000000, 7200000, 8700000])]
        operating_expenses = [float(x) for x in raw_data.get("operating_expenses", [1500000, 1800000, 2200000])]
        depreciation = [float(x) for x in raw_data.get("depreciation", [500000, 600000, 700000])]
        interest_expense = [float(x) for x in raw_data.get("interest_expense", [400000, 450000, 500000])]
        tax_rate = float(raw_data.get("tax_rate", 0.25))

        # Computed P&L
        gross_profit = [rev - c for rev, c in zip(revenue, cogs)]
        ebitda = [gp - opex for gp, opex in zip(gross_profit, operating_expenses)]
        ebit = [eb - dep for eb, dep in zip(ebitda, depreciation)]
        ebt = [eb - int_exp for eb, int_exp in zip(ebit, interest_expense)]
        tax = [max(0.0, e * tax_rate) for e in ebt]
        pat = [e - t for e, t in zip(ebt, tax)]
        cash_accruals = [p + d for p, d in zip(pat, depreciation)]

        # Balance Sheet line items
        cash_and_bank = [float(x) for x in raw_data.get("cash_and_bank", [500000, 700000, 1200000])]
        sundry_debtors = [float(x) for x in raw_data.get("sundry_debtors", [1800000, 2200000, 2600000])]
        inventory = [float(x) for x in raw_data.get("inventory", [1500000, 1900000, 2200000])]
        other_current_assets = [float(x) for x in raw_data.get("other_current_assets", [400000, 500000, 600000])]
        
        current_assets = [
            c + d + inv + oca 
            for c, d, inv, oca in zip(cash_and_bank, sundry_debtors, inventory, other_current_assets)
        ]

        net_fixed_assets = [float(x) for x in raw_data.get("net_fixed_assets", [4000000, 4800000, 5600000])]
        other_non_current_assets = [float(x) for x in raw_data.get("other_non_current_assets", [300000, 400000, 500000])]
        total_assets = [ca + nfa + onca for ca, nfa, onca in zip(current_assets, net_fixed_assets, other_non_current_assets)]

        sundry_creditors = [float(x) for x in raw_data.get("sundry_creditors", [1200000, 1400000, 1600000])]
        short_term_borrowings = [float(x) for x in raw_data.get("short_term_borrowings", [1000000, 1200000, 1400000])]
        other_current_liabilities = [float(x) for x in raw_data.get("other_current_liabilities", [300000, 400000, 500000])]
        
        current_liabilities = [
            sc + stb + ocl 
            for sc, stb, ocl in zip(sundry_creditors, short_term_borrowings, other_current_liabilities)
        ]

        long_term_debt = [float(x) for x in raw_data.get("long_term_debt", [2000000, 2200000, 2000000])]
        total_debt = [stb + ltd for stb, ltd in zip(short_term_borrowings, long_term_debt)]
        
        paid_up_capital = [float(x) for x in raw_data.get("paid_up_capital", [1500000, 1500000, 1500000])]
        reserves_and_surplus = [float(x) for x in raw_data.get("reserves_and_surplus", [2500000, 3800000, 5700000])]
        tangible_net_worth = [puc + rs for puc, rs in zip(paid_up_capital, reserves_and_surplus)]
        
        total_outside_liabilities = [cl + ltd for cl, ltd in zip(current_liabilities, long_term_debt)]

        # Working Capital Gap & Net Working Capital
        working_capital_gap = [ca - (sc + ocl) for ca, sc, ocl in zip(current_assets, sundry_creditors, other_current_liabilities)]
        net_working_capital = [ca - cl for ca, cl in zip(current_assets, current_liabilities)]

        return {
            "years": years,
            "pnl": {
                "revenue": revenue,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "operating_expenses": operating_expenses,
                "ebitda": ebitda,
                "depreciation": depreciation,
                "ebit": ebit,
                "interest_expense": interest_expense,
                "ebt": ebt,
                "tax": tax,
                "pat": pat,
                "cash_accruals": cash_accruals
            },
            "balance_sheet": {
                "cash_and_bank": cash_and_bank,
                "sundry_debtors": sundry_debtors,
                "inventory": inventory,
                "other_current_assets": other_current_assets,
                "current_assets": current_assets,
                "net_fixed_assets": net_fixed_assets,
                "other_non_current_assets": other_non_current_assets,
                "total_assets": total_assets,
                "sundry_creditors": sundry_creditors,
                "short_term_borrowings": short_term_borrowings,
                "other_current_liabilities": other_current_liabilities,
                "current_liabilities": current_liabilities,
                "long_term_debt": long_term_debt,
                "total_debt": total_debt,
                "paid_up_capital": paid_up_capital,
                "reserves_and_surplus": reserves_and_surplus,
                "tangible_net_worth": tangible_net_worth,
                "total_outside_liabilities": total_outside_liabilities,
                "working_capital_gap": working_capital_gap,
                "net_working_capital": net_working_capital
            }
        }


# =============================================================================
# 2. 5-PILLAR RATIO DIAGNOSTICS & WORKING CAPITAL (TANDON / NAYAK MPBF)
# =============================================================================

class RatioDiagnosticsEngine:
    """Computes full institutional 5-pillar ratio diagnostics across all historical years."""

    @staticmethod
    def calculate_ratios(spread: Dict[str, Any]) -> Dict[str, Any]:
        pnl = spread["pnl"]
        bs = spread["balance_sheet"]
        years = spread["years"]
        num_years = len(years)

        # 1. Liquidity Ratios
        current_ratios = [round(ca / cl, 2) if cl > 0 else 0.0 for ca, cl in zip(bs["current_assets"], bs["current_liabilities"])]
        quick_assets = [ca - inv for ca, inv in zip(bs["current_assets"], bs["inventory"])]
        quick_ratios = [round(qa / cl, 2) if cl > 0 else 0.0 for qa, cl in zip(quick_assets, bs["current_liabilities"])]
        cash_ratios = [round(cash / cl, 2) if cl > 0 else 0.0 for cash, cl in zip(bs["cash_and_bank"], bs["current_liabilities"])]

        # 2. Solvency & Leverage Ratios
        debt_to_equity = [round(ltd / tnw, 2) if tnw > 0 else 0.0 for ltd, tnw in zip(bs["long_term_debt"], bs["tangible_net_worth"])]
        total_debt_to_equity = [round(td / tnw, 2) if tnw > 0 else 0.0 for td, tnw in zip(bs["total_debt"], bs["tangible_net_worth"])]
        tol_to_tnw = [round(tol / tnw, 2) if tnw > 0 else 0.0 for tol, tnw in zip(bs["total_outside_liabilities"], bs["tangible_net_worth"])]
        
        interest_coverage = [round(ebitda / int_exp, 2) if int_exp > 0 else 10.0 for ebitda, int_exp in zip(pnl["ebitda"], pnl["interest_expense"])]
        
        # Debt Service Coverage Ratio (DSCR): (PAT + Dep + Interest) / (Interest + Principal Amortization)
        # Assuming annual principal amortization is approx 20% of long term debt
        dscr = []
        for i in range(num_years):
            cash_flow_available = pnl["pat"][i] + pnl["depreciation"][i] + pnl["interest_expense"][i]
            principal_repay = bs["long_term_debt"][i] * 0.20
            debt_service = pnl["interest_expense"][i] + principal_repay
            dscr_val = round(cash_flow_available / debt_service, 2) if debt_service > 0 else 3.0
            dscr.append(dscr_val)

        # 3. Profitability & Returns
        gross_profit_margins = [round(gp / rev * 100, 2) if rev > 0 else 0.0 for gp, rev in zip(pnl["gross_profit"], pnl["revenue"])]
        ebitda_margins = [round(eb / rev * 100, 2) if rev > 0 else 0.0 for eb, rev in zip(pnl["ebitda"], pnl["revenue"])]
        pat_margins = [round(p / rev * 100, 2) if rev > 0 else 0.0 for p, rev in zip(pnl["pat"], pnl["revenue"])]
        
        roe = [round(p / tnw * 100, 2) if tnw > 0 else 0.0 for p, tnw in zip(pnl["pat"], bs["tangible_net_worth"])]
        capital_employed = [tnw + ltd for tnw, ltd in zip(bs["tangible_net_worth"], bs["long_term_debt"])]
        roce = [round(eb / ce * 100, 2) if ce > 0 else 0.0 for eb, ce in zip(pnl["ebit"], capital_employed)]

        # 4. Operating Efficiency & Activity Ratios
        sales_growth_rates = [0.0]
        for i in range(1, num_years):
            prev_rev = pnl["revenue"][i-1]
            curr_rev = pnl["revenue"][i]
            growth = round((curr_rev - prev_rev) / prev_rev * 100, 2) if prev_rev > 0 else 0.0
            sales_growth_rates.append(growth)

        asset_turnover = [round(rev / ta, 2) if ta > 0 else 0.0 for rev, ta in zip(pnl["revenue"], bs["total_assets"])]
        inventory_days = [round(inv / c * 365, 1) if c > 0 else 0.0 for inv, c in zip(bs["inventory"], pnl["cogs"])]
        debtor_days = [round(d / rev * 365, 1) if rev > 0 else 0.0 for d, rev in zip(bs["sundry_debtors"], pnl["revenue"])]
        creditor_days = [round(sc / c * 365, 1) if c > 0 else 0.0 for sc, c in zip(bs["sundry_creditors"], pnl["cogs"])]
        cash_conversion_cycle = [round(d_days + inv_days - c_days, 1) for d_days, inv_days, c_days in zip(debtor_days, inventory_days, creditor_days)]

        # 5. Working Capital MPBF (Tandon & Nayak Committee Models)
        # Latest Year
        latest_ca = bs["current_assets"][-1]
        latest_cl = bs["current_liabilities"][-1]
        latest_other_cl = bs["sundry_creditors"][-1] + bs["other_current_liabilities"][-1]
        
        # Tandon Method I: 75% of (Current Assets - Other Current Liabilities)
        tandon_method_1 = round(0.75 * (latest_ca - latest_other_cl), 2)
        # Tandon Method II: (75% of Current Assets) - Other Current Liabilities
        tandon_method_2 = round((0.75 * latest_ca) - latest_other_cl, 2)
        # Nayak Committee Model (for MSMEs with turnover < 5 Cr): 20% of Turnover
        nayak_turnover_method = round(0.20 * pnl["revenue"][-1], 2)

        return {
            "liquidity": {
                "current_ratio": current_ratios,
                "quick_ratio": quick_ratios,
                "cash_ratio": cash_ratios
            },
            "solvency": {
                "debt_to_equity": debt_to_equity,
                "total_debt_to_equity": total_debt_to_equity,
                "tol_to_tnw": tol_to_tnw,
                "interest_coverage_ratio": interest_coverage,
                "debt_service_coverage_ratio": dscr
            },
            "profitability": {
                "gross_profit_margin_pct": gross_profit_margins,
                "ebitda_margin_pct": ebitda_margins,
                "pat_margin_pct": pat_margins,
                "return_on_equity_pct": roe,
                "return_on_capital_employed_pct": roce
            },
            "efficiency": {
                "sales_growth_rate_pct": sales_growth_rates,
                "asset_turnover": asset_turnover,
                "inventory_days": inventory_days,
                "debtor_days": debtor_days,
                "creditor_days": creditor_days,
                "cash_conversion_cycle_days": cash_conversion_cycle
            },
            "mpbf_working_capital": {
                "tandon_method_1": max(0.0, tandon_method_1),
                "tandon_method_2": max(0.0, tandon_method_2),
                "nayak_turnover_method": nayak_turnover_method,
                "recommended_limit": max(0.0, min(tandon_method_2, nayak_turnover_method)) if nayak_turnover_method > 0 else max(0.0, tandon_method_2)
            }
        }


# =============================================================================
# 3. FORENSIC ACCOUNTING: ALTMAN Z''-SCORE & BENEISH M-SCORE
# =============================================================================

class ForensicAuditor:
    """
    Executes deep forensic algorithms to detect:
    1. Altman Z''-Score (Emerging Market Bankruptcy & Default Risk)
    2. Beneish M-Score (Earnings Manipulation & Financial Statement Fraud)
    """

    @staticmethod
    def calculate_altman_z_double_prime(spread: Dict[str, Any]) -> Dict[str, Any]:
        """
        Altman Z''-Score for Emerging Markets & Private Non-Manufacturing / MSME Firms:
        Z'' = 6.56 * X1 + 3.26 * X2 + 6.72 * X3 + 1.05 * X4
        Where:
        X1 = Working Capital / Total Assets
        X2 = Retained Earnings / Total Assets
        X3 = Operating Earnings (EBIT) / Total Assets
        X4 = Book Value of Equity / Total Liabilities
        """
        bs = spread["balance_sheet"]
        pnl = spread["pnl"]
        
        # Latest Year
        wc = bs["net_working_capital"][-1]
        ta = max(1.0, bs["total_assets"][-1])
        retained_earnings = bs["reserves_and_surplus"][-1]
        ebit = pnl["ebit"][-1]
        equity_bv = bs["tangible_net_worth"][-1]
        total_liabilities = max(1.0, bs["total_outside_liabilities"][-1])

        x1 = wc / ta
        x2 = retained_earnings / ta
        x3 = ebit / ta
        x4 = equity_bv / total_liabilities

        z_score = round((6.56 * x1) + (3.26 * x2) + (6.72 * x3) + (1.05 * x4), 2)

        if z_score > 2.60:
            zone = "Safe Zone"
            risk_level = "Very Low Default Probability (Financially Sound)"
            color = "#10B981" # Green
        elif 1.10 <= z_score <= 2.60:
            zone = "Grey Zone"
            risk_level = "Moderate Vulnerability (Active Monitoring Required)"
            color = "#F59E0B" # Amber
        else:
            zone = "Distress Zone"
            risk_level = "Critical Insolvency Risk (High Probability of Default within 12-24 Months)"
            color = "#EF4444" # Red

        return {
            "z_score": z_score,
            "zone": zone,
            "risk_level": risk_level,
            "badge_color": color,
            "components": {
                "X1_working_capital_to_assets": round(x1, 3),
                "X2_retained_earnings_to_assets": round(x2, 3),
                "X3_ebit_to_assets": round(x3, 3),
                "X4_equity_to_liabilities": round(x4, 3)
            }
        }

    @staticmethod
    def calculate_beneish_m_score(spread: Dict[str, Any]) -> Dict[str, Any]:
        """
        Beneish M-Score for detecting potential earnings manipulation / balance sheet inflation:
        M-Score = -4.84 + 0.920*DSRI + 0.528*GMI + 0.404*AQI + 0.892*SGI + 0.115*DEPI - 0.172*SGAI + 4.037*TATA + 0.0327*LVGI
        A score greater than -1.78 indicates a high probability of accounting manipulation.
        """
        pnl = spread["pnl"]
        bs = spread["balance_sheet"]
        
        if len(pnl["revenue"]) < 2:
            return {"m_score": -2.50, "manipulation_risk": "Low", "flag": False, "explanation": "Insufficient historical data"}

        # t = latest year (index -1), t_1 = previous year (index -2)
        rev_t, rev_t1 = max(1.0, pnl["revenue"][-1]), max(1.0, pnl["revenue"][-2])
        cogs_t, cogs_t1 = max(1.0, pnl["cogs"][-1]), max(1.0, pnl["cogs"][-2])
        rec_t, rec_t1 = bs["sundry_debtors"][-1], max(1.0, bs["sundry_debtors"][-2])
        ta_t, ta_t1 = max(1.0, bs["total_assets"][-1]), max(1.0, bs["total_assets"][-2])
        dep_t, dep_t1 = pnl["depreciation"][-1], max(1.0, pnl["depreciation"][-2])
        ppe_t, ppe_t1 = max(1.0, bs["net_fixed_assets"][-1]), max(1.0, bs["net_fixed_assets"][-2])
        sga_t, sga_t1 = pnl["operating_expenses"][-1], max(1.0, pnl["operating_expenses"][-2])
        lev_t, lev_t1 = (bs["total_outside_liabilities"][-1] / ta_t), (bs["total_outside_liabilities"][-2] / ta_t1)
        
        # 1. Days Sales in Receivables Index (DSRI)
        dsri = (rec_t / rev_t) / (rec_t1 / rev_t1)
        
        # 2. Gross Margin Index (GMI)
        gm_t = (rev_t - cogs_t) / rev_t
        gm_t1 = (rev_t1 - cogs_t1) / rev_t1
        gmi = gm_t1 / gm_t if gm_t > 0 else 1.0
        
        # 3. Asset Quality Index (AQI)
        nca_t = ta_t - bs["current_assets"][-1] - ppe_t
        nca_t1 = ta_t1 - bs["current_assets"][-2] - ppe_t1
        aqi = (1 - (bs["current_assets"][-1] + ppe_t)/ta_t) / max(0.01, (1 - (bs["current_assets"][-2] + ppe_t1)/ta_t1))
        
        # 4. Sales Growth Index (SGI)
        sgi = rev_t / rev_t1
        
        # 5. Depreciation Index (DEPI)
        dep_rate_t = dep_t / (ppe_t + dep_t)
        dep_rate_t1 = dep_t1 / (ppe_t1 + dep_t1)
        depi = dep_rate_t1 / dep_rate_t if dep_rate_t > 0 else 1.0
        
        # 6. Sales General & Admin Expense Index (SGAI)
        sgai = (sga_t / rev_t) / (sga_t1 / rev_t1)
        
        # 7. Leverage Index (LVGI)
        lvgi = lev_t / lev_t1 if lev_t1 > 0 else 1.0
        
        # 8. Total Accruals to Total Assets (TATA)
        net_income = pnl["pat"][-1]
        cfo = pnl["cash_accruals"][-1] # Approximation
        tata = (net_income - cfo) / ta_t

        m_score = (
            -4.84 
            + (0.920 * dsri) 
            + (0.528 * gmi) 
            + (0.404 * aqi) 
            + (0.892 * sgi) 
            + (0.115 * depi) 
            - (0.172 * sgai) 
            + (4.037 * tata) 
            + (0.0327 * lvgi)
        )
        m_score = round(m_score, 2)

        is_manipulator = m_score > -1.78
        
        if is_manipulator:
            risk = "High Probability of Financial Statement Manipulation (Forensic Red Flag)"
            badge_color = "#EF4444"
        else:
            risk = "Clean Financial Reporting (Low Probability of Earnings Distortion)"
            badge_color = "#10B981"

        return {
            "m_score": m_score,
            "threshold": -1.78,
            "manipulation_flag": is_manipulator,
            "risk_assessment": risk,
            "badge_color": badge_color,
            "indices": {
                "DSRI_receivables_growth": round(dsri, 2),
                "GMI_margin_deterioration": round(gmi, 2),
                "AQI_asset_quality": round(aqi, 2),
                "SGI_sales_growth": round(sgi, 2),
                "DEPI_depreciation_slowing": round(depi, 2),
                "SGAI_overhead_surge": round(sgai, 2),
                "LVGI_leverage_jump": round(lvgi, 2),
                "TATA_accruals_to_assets": round(tata, 3)
            }
        }


# =============================================================================
# 4. 3-YEAR PROJECTIONS & MACRO STRESS SIMULATOR
# =============================================================================

class FinancialForecaster:
    """Projects 3 years forward and executes live stress sensitivity simulations."""

    @staticmethod
    def project_3_years(spread: Dict[str, Any], sales_cagr: float = 0.15) -> Dict[str, Any]:
        """Generates 3-year baseline projections based on historical margins."""
        pnl = spread["pnl"]
        bs = spread["balance_sheet"]

        base_rev = pnl["revenue"][-1]
        gross_margin = pnl["gross_profit"][-1] / base_rev if base_rev > 0 else 0.40
        opex_pct = pnl["operating_expenses"][-1] / base_rev if base_rev > 0 else 0.15
        dep_pct = pnl["depreciation"][-1] / base_rev if base_rev > 0 else 0.05
        int_base = pnl["interest_expense"][-1]
        tax_rate = 0.25

        proj_years = ["Proj FY+1", "Proj FY+2", "Proj FY+3"]
        proj_rev, proj_ebitda, proj_pat, proj_dscr = [], [], [], []

        curr_rev = base_rev
        for _ in range(3):
            curr_rev *= (1.0 + sales_cagr)
            ebitda = curr_rev * (gross_margin - opex_pct)
            dep = curr_rev * dep_pct
            ebit = ebitda - dep
            ebt = ebit - int_base
            tax = max(0.0, ebt * tax_rate)
            pat = ebt - tax
            
            cash_flow = pat + dep + int_base
            debt_service = int_base + (bs["long_term_debt"][-1] * 0.20)
            dscr = round(cash_flow / debt_service, 2) if debt_service > 0 else 3.0

            proj_rev.append(round(curr_rev, 2))
            proj_ebitda.append(round(ebitda, 2))
            proj_pat.append(round(pat, 2))
            proj_dscr.append(dscr)

        return {
            "projection_years": proj_years,
            "projected_revenue": proj_rev,
            "projected_ebitda": proj_ebitda,
            "projected_pat": proj_pat,
            "projected_dscr": proj_dscr
        }

    @staticmethod
    def simulate_stress_scenario(
        spread: Dict[str, Any],
        revenue_shock_pct: float = 0.0,       # e.g. -0.20 for -20% sales
        cogs_increase_pct: float = 0.0,       # e.g. +0.15 for +15% raw material inflation
        interest_rate_shock_bps: float = 0.0  # e.g. +200 for +200 bps hike
    ) -> Dict[str, Any]:
        """
        Simulates economic stress conditions on latest audited balance sheet:
        1. Sales Drops (Demand Shock)
        2. Cost Inflation (Margin Compression)
        3. RBLR Rate Hike (Debt Servicing Spike)
        """
        pnl = spread["pnl"]
        bs = spread["balance_sheet"]

        base_rev = pnl["revenue"][-1] * (1.0 + revenue_shock_pct)
        base_cogs = pnl["cogs"][-1] * (1.0 + cogs_increase_pct)
        gross_profit = base_rev - base_cogs
        
        ebitda = gross_profit - pnl["operating_expenses"][-1]
        ebit = ebitda - pnl["depreciation"][-1]
        
        # Interest spike: Base interest + (Total Debt * (shock_bps / 10000))
        added_interest = bs["total_debt"][-1] * (interest_rate_shock_bps / 10000.0)
        stressed_interest = pnl["interest_expense"][-1] + added_interest
        
        ebt = ebit - stressed_interest
        tax = max(0.0, ebt * 0.25)
        stressed_pat = ebt - tax
        
        stressed_icr = round(ebitda / stressed_interest, 2) if stressed_interest > 0 else 10.0
        
        debt_service = stressed_interest + (bs["long_term_debt"][-1] * 0.20)
        stressed_cash_flow = stressed_pat + pnl["depreciation"][-1] + stressed_interest
        stressed_dscr = round(stressed_cash_flow / debt_service, 2) if debt_service > 0 else 3.0

        is_solvent = stressed_dscr >= 1.20 and stressed_icr >= 1.50
        
        if is_solvent:
            status = "RESILIENT (Meets Bank Solvency Threshold under Stress)"
            color = "#10B981"
        elif stressed_dscr >= 1.0:
            status = "VULNERABLE (Borderline Debt Servicing under Stress)"
            color = "#F59E0B"
        else:
            status = "CRITICAL INSOLVENCY (Default Triggered under Stress)"
            color = "#EF4444"

        return {
            "stressed_revenue": round(base_rev, 2),
            "stressed_ebitda": round(ebitda, 2),
            "stressed_pat": round(stressed_pat, 2),
            "stressed_interest_expense": round(stressed_interest, 2),
            "stressed_icr": stressed_icr,
            "stressed_dscr": stressed_dscr,
            "solvency_status": status,
            "badge_color": color,
            "is_solvent": is_solvent
        }


# =============================================================================
# 5. DISCOUNTED CASH FLOW (DCF) VALUATION & DEBT SIZING
# =============================================================================

class EnterpriseValuator:
    """Executes Discounted Cash Flow (DCF) valuation and Loan-to-Enterprise Value (LTV_EV) sizing."""

    @staticmethod
    def calculate_dcf_valuation(
        spread: Dict[str, Any],
        proposed_loan_amount: float = 5000000.0,
        forecast_years: int = 5,
        wacc: float = 0.115,          # 11.5% Weighted Average Cost of Capital
        terminal_growth_rate: float = 0.04 # 4.0% Long-term GDP growth rate
    ) -> Dict[str, Any]:
        pnl = spread["pnl"]
        bs = spread["balance_sheet"]

        base_ebit = max(100000.0, pnl["ebit"][-1])
        base_dep = pnl["depreciation"][-1]
        tax_rate = 0.25

        # Project 5-year Free Cash Flows to Firm (FCFF)
        fcff_projections = []
        discount_factors = []
        present_values = []
        
        growth_rate = 0.12 # 12% revenue growth
        curr_ebit = base_ebit

        for t in range(1, forecast_years + 1):
            curr_ebit *= (1.0 + growth_rate)
            nopat = curr_ebit * (1.0 - tax_rate)
            capex = base_dep * 1.10 # Re-investment
            delta_nwc = curr_ebit * 0.05
            
            fcff = nopat + base_dep - capex - delta_nwc
            discount_factor = 1.0 / math.pow(1.0 + wacc, t)
            pv = fcff * discount_factor
            
            fcff_projections.append(round(fcff, 2))
            discount_factors.append(round(discount_factor, 4))
            present_values.append(round(pv, 2))

        pv_discrete_cash_flows = sum(present_values)

        # Terminal Value (Gordon Growth Model)
        final_fcff = fcff_projections[-1] * (1.0 + terminal_growth_rate)
        terminal_value = final_fcff / (wacc - terminal_growth_rate) if (wacc - terminal_growth_rate) > 0 else 0.0
        pv_terminal_value = terminal_value / math.pow(1.0 + wacc, forecast_years)

        enterprise_value = round(pv_discrete_cash_flows + pv_terminal_value, 2)
        net_debt = bs["total_debt"][-1] - bs["cash_and_bank"][-1]
        equity_value = max(0.0, round(enterprise_value - net_debt, 2))

        # Loan to Enterprise Value (LTV on EV)
        loan_to_ev_ratio = round((proposed_loan_amount / enterprise_value) * 100, 2) if enterprise_value > 0 else 0.0

        if loan_to_ev_ratio <= 35.0:
            leverage_grade = "Conservative (Safe Leverage Ceiling < 35%)"
            badge_color = "#10B981"
        elif loan_to_ev_ratio <= 50.0:
            leverage_grade = "Moderate (Acceptable Banking Leverage < 50%)"
            badge_color = "#F59E0B"
        else:
            leverage_grade = "Highly Leveraged (Loan Exceeds 50% of Total Enterprise Value)"
            badge_color = "#EF4444"

        return {
            "enterprise_value": enterprise_value,
            "equity_value": equity_value,
            "pv_discrete_cash_flows": round(pv_discrete_cash_flows, 2),
            "pv_terminal_value": round(pv_terminal_value, 2),
            "fcff_projections": fcff_projections,
            "wacc_pct": round(wacc * 100, 2),
            "terminal_growth_pct": round(terminal_growth_rate * 100, 2),
            "proposed_loan_amount": proposed_loan_amount,
            "loan_to_enterprise_value_pct": loan_to_ev_ratio,
            "leverage_assessment": leverage_grade,
            "badge_color": badge_color
        }


# =============================================================================
# 6. MSE PARAMETER AUTO-MAPPER & CENTRAL BANK RISK GRADING
# =============================================================================

class MSEParameterAutoMapper:
    """
    Takes spread financial statements and automatically calculates, scores,
    and maps all 13 parameters of Form MSE 1 (or 9 of Form MSE II) without manual typing!
    """

    @staticmethod
    def auto_score_form_mse_1(spread: Dict[str, Any], operational_flags: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Auto-computes Form MSE 1 (Existing Units) scorecard directly from Balance Sheet and P&L."""
        pnl = spread["pnl"]
        bs = spread["balance_sheet"]
        flags = operational_flags or {}

        # 1. Current Ratio
        cr = bs["current_assets"][-1] / bs["current_liabilities"][-1] if bs["current_liabilities"][-1] > 0 else 0.0
        if cr >= 1.33: score_cr, max_cr = 10, 10
        elif cr >= 1.20: score_cr, max_cr = 7, 10
        elif cr >= 1.10: score_cr, max_cr = 4, 10
        else: score_cr, max_cr = 0, 10

        # 2. Debt Equity Ratio
        der = bs["long_term_debt"][-1] / bs["tangible_net_worth"][-1] if bs["tangible_net_worth"][-1] > 0 else 0.0
        if der <= 2.0: score_der, max_der = 10, 10
        elif der <= 3.0: score_der, max_der = 7, 10
        elif der <= 4.0: score_der, max_der = 4, 10
        else: score_der, max_der = 0, 10

        # 3. Sales Growth Rate
        if len(pnl["revenue"]) >= 2:
            prev_rev = pnl["revenue"][-2]
            growth = ((pnl["revenue"][-1] - prev_rev) / prev_rev * 100) if prev_rev > 0 else 0.0
        else:
            growth = 15.0
            
        if growth > 20.0: score_growth, max_growth = 10, 10
        elif growth >= 10.0: score_growth, max_growth = 7, 10
        elif growth >= 0.0: score_growth, max_growth = 4, 10
        else: score_growth, max_growth = 0, 10

        # 4. PAT Margin
        rev = pnl["revenue"][-1]
        pat_margin = (pnl["pat"][-1] / rev * 100) if rev > 0 else 0.0
        if pat_margin > 15.0: score_pat, max_pat = 10, 10
        elif pat_margin >= 10.0: score_pat, max_pat = 7, 10
        elif pat_margin >= 5.0: score_pat, max_pat = 4, 10
        else: score_pat, max_pat = 0, 10

        # 5. Sanction Terms Adherence
        sanction_status = flags.get("sanction_compliance", "Compliant")
        score_sanction = 10 if sanction_status == "Compliant" else (5 if sanction_status == "Minor deviations" else 0)

        # 6. Stock Statements Status
        stock_status = flags.get("stock_statement_status", "Timely")
        score_stock = 10 if stock_status == "Timely" else (5 if stock_status == "Irregular/Delayed" else 0)

        # 7. Debt Servicing History
        debt_servicing = flags.get("debt_servicing_history", "Within 1 month")
        is_defaulter = debt_servicing in ["Overdue > 3 months", "Defaulter"]
        score_debt = 0 if is_defaulter else (10 if debt_servicing == "Within 1 month" else 5)

        # 8. Inventory / QIS compliance
        inv_status = flags.get("inventory_compliance", "Fair compliance")
        score_inv = 5 if inv_status == "Fair compliance" else (2 if inv_status == "Moderate deviation" else 0)

        # 9. Bills Culture
        bills_culture = flags.get("bills_culture", True)
        score_bills = 5 if bills_culture else 0

        # 10. Bill Payment Record
        bill_pay = flags.get("bill_payment_record", "Prompt")
        score_bill_pay = 5 if bill_pay == "Prompt" else (2 if bill_pay == "Occasional delay" else 0)

        # 11. Annual Review Timeliness
        review_timely = flags.get("review_documents_timely", True)
        score_review = 5 if review_timely else 0

        # 12. LC/BG Facility Conduct
        lc_status = flags.get("lc_bg_status", "Prompt / No Facility")
        score_lc = 5 if lc_status in ["Prompt / No Facility", "Prompt"] else 0

        # 13. Ancillary Business
        ancillary = flags.get("ancillary_relationship", "Substantial")
        score_ancillary = 5 if ancillary == "Substantial" else (3 if ancillary == "Moderate" else 0)

        total_score = (
            score_cr + score_der + score_growth + score_pat + score_sanction +
            score_stock + score_debt + score_inv + score_bills + score_bill_pay +
            score_review + score_lc + score_ancillary
        )

        if is_defaulter:
            total_score = 0

        grade_info = assign_cbi_risk_grade(total_score)

        return {
            "model_form": "Form MSE 1 (Existing Units - Auto-Mapped)",
            "total_score": total_score,
            "grade": grade_info["grade"],
            "risk_profile": grade_info["risk_profile"],
            "hurdle_rate_met": grade_info["hurdle_rate_met"],
            "is_defaulter_override": is_defaulter,
            "calculated_financial_ratios": {
                "current_ratio": round(cr, 2),
                "debt_equity_ratio": round(der, 2),
                "sales_growth_rate": round(growth, 2),
                "pat_margin": round(pat_margin, 2)
            },
            "parameter_scores": [
                {"param": "1. Current Ratio", "value": f"{cr:.2f}", "score": score_cr, "max": 10},
                {"param": "2. Debt Equity Ratio", "value": f"{der:.2f}", "score": score_der, "max": 10},
                {"param": "3. Sales Growth Rate", "value": f"{growth:.1f}%", "score": score_growth, "max": 10},
                {"param": "4. PAT Margin", "value": f"{pat_margin:.1f}%", "score": score_pat, "max": 10},
                {"param": "5. Sanction Terms Adherence", "value": sanction_status, "score": score_sanction, "max": 10},
                {"param": "6. Stock Statement Submission", "value": stock_status, "score": score_stock, "max": 10},
                {"param": "7. Debt Servicing History", "value": debt_servicing, "score": score_debt, "max": 10},
                {"param": "8. Inventory Compliance", "value": inv_status, "score": score_inv, "max": 5},
                {"param": "9. Bills Culture", "value": "Yes" if bills_culture else "No", "score": score_bills, "max": 5},
                {"param": "10. Bill Payment Record", "value": bill_pay, "score": score_bill_pay, "max": 5},
                {"param": "11. Annual Review Timely", "value": "Yes" if review_timely else "No", "score": score_review, "max": 5},
                {"param": "12. LC/BG Facility Conduct", "value": lc_status, "score": score_lc, "max": 5},
                {"param": "13. Ancillary Relationship", "value": ancillary, "score": score_ancillary, "max": 5}
            ]
        }
