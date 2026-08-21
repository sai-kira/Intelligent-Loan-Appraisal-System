"""
Central Bank of India - Intelligent Loan Appraisal System (ILAS)
Financial Document Ingestion & Normalization Parser

Supports:
- CSV / Excel Spreadsheets (.csv, .xlsx, .xls)
- JSON / Tally ERP 9 / Tally Prime exports
- Plain dictionary structures
"""

import json
import io
from typing import Dict, Any, Union
import pandas as pd

class FinancialDocumentParser:
    """Parses and maps diverse corporate financial inputs into standardized financial spreads."""

    @staticmethod
    def parse_json_or_dict(content: Union[str, bytes, dict]) -> Dict[str, Any]:
        """Parses JSON or raw dict into standardized structure."""
        if isinstance(content, (str, bytes)):
            data = json.loads(content)
        else:
            data = content

        # Required fields default mapping
        normalized = {
            "company_name": data.get("company_name", "Uploaded Corporate Borrower"),
            "loan_type": data.get("loan_type", "MSME Loan - Existing Unit"),
            "requested_loan_amount": float(data.get("requested_loan_amount", data.get("loan_amount", 5000000.0))),
            "tenure_months": int(data.get("tenure_months", 60)),
            "credit_score": int(data.get("credit_score", 720)),
            "years": data.get("years", ["FY24", "FY25", "FY26"]),
            "revenue": [float(x) for x in data.get("revenue", [10000000, 12000000, 15000000])],
            "cogs": [float(x) for x in data.get("cogs", [6000000, 7200000, 8700000])],
            "operating_expenses": [float(x) for x in data.get("operating_expenses", [1500000, 1800000, 2200000])],
            "depreciation": [float(x) for x in data.get("depreciation", [500000, 600000, 700000])],
            "interest_expense": [float(x) for x in data.get("interest_expense", [400000, 450000, 500000])],
            "tax_rate": float(data.get("tax_rate", 0.25)),
            "cash_and_bank": [float(x) for x in data.get("cash_and_bank", [500000, 700000, 1200000])],
            "sundry_debtors": [float(x) for x in data.get("sundry_debtors", [1800000, 2200000, 2600000])],
            "inventory": [float(x) for x in data.get("inventory", [1500000, 1900000, 2200000])],
            "other_current_assets": [float(x) for x in data.get("other_current_assets", [400000, 500000, 600000])],
            "net_fixed_assets": [float(x) for x in data.get("net_fixed_assets", [4000000, 4800000, 5600000])],
            "other_non_current_assets": [float(x) for x in data.get("other_non_current_assets", [300000, 400000, 500000])],
            "sundry_creditors": [float(x) for x in data.get("sundry_creditors", [1200000, 1400000, 1600000])],
            "short_term_borrowings": [float(x) for x in data.get("short_term_borrowings", [1000000, 1200000, 1400000])],
            "other_current_liabilities": [float(x) for x in data.get("other_current_liabilities", [300000, 400000, 500000])],
            "long_term_debt": [float(x) for x in data.get("long_term_debt", [2000000, 2200000, 2000000])],
            "paid_up_capital": [float(x) for x in data.get("paid_up_capital", [1500000, 1500000, 1500000])],
            "reserves_and_surplus": [float(x) for x in data.get("reserves_and_surplus", [2500000, 3800000, 5700000])],
            "operational_flags": data.get("operational_flags", {
                "sanction_compliance": "Compliant",
                "stock_statement_status": "Timely",
                "debt_servicing_history": "Within 1 month",
                "inventory_compliance": "Fair compliance",
                "bills_culture": True,
                "bill_payment_record": "Prompt",
                "review_documents_timely": True,
                "lc_bg_status": "Prompt / No Facility",
                "ancillary_relationship": "Substantial"
            })
        }
        return normalized

    @staticmethod
    def parse_csv_file(file_content: Union[str, bytes]) -> Dict[str, Any]:
        """Parses CSV spreadsheet containing Line Item in first column and years in subsequent columns."""
        if isinstance(file_content, str):
            df = pd.read_csv(io.StringIO(file_content))
        else:
            df = pd.read_csv(io.BytesIO(file_content))

        # Expected format: Column 1 = Metric / Line Item, Column 2..N = FY24, FY25, FY26
        years = list(df.columns[1:])
        
        # Map row headers to standardized keys
        lookup = {}
        for _, row in df.iterrows():
            metric_raw = str(row.iloc[0]).lower().strip()
            values = [float(row[y]) for y in years]
            
            if "revenue" in metric_raw or "sales" in metric_raw or "turnover" in metric_raw:
                lookup["revenue"] = values
            elif "cogs" in metric_raw or "material" in metric_raw or "cost of sales" in metric_raw:
                lookup["cogs"] = values
            elif "opex" in metric_raw or "operating expense" in metric_raw or "admin" in metric_raw:
                lookup["operating_expenses"] = values
            elif "depreciation" in metric_raw:
                lookup["depreciation"] = values
            elif "interest" in metric_raw or "finance" in metric_raw:
                lookup["interest_expense"] = values
            elif "cash" in metric_raw or "bank" in metric_raw:
                lookup["cash_and_bank"] = values
            elif "debtor" in metric_raw or "receivable" in metric_raw:
                lookup["sundry_debtors"] = values
            elif "inventory" in metric_raw or "stock" in metric_raw:
                lookup["inventory"] = values
            elif "fixed asset" in metric_raw or "ppe" in metric_raw or "plant" in metric_raw:
                lookup["net_fixed_assets"] = values
            elif "creditor" in metric_raw or "payable" in metric_raw:
                lookup["sundry_creditors"] = values
            elif "short term" in metric_raw or "working capital loan" in metric_raw or "overdraft" in metric_raw:
                lookup["short_term_borrowings"] = values
            elif "long term debt" in metric_raw or "term loan" in metric_raw:
                lookup["long_term_debt"] = values
            elif "capital" in metric_raw or "equity share" in metric_raw:
                lookup["paid_up_capital"] = values
            elif "reserve" in metric_raw or "surplus" in metric_raw:
                lookup["reserves_and_surplus"] = values

        lookup["years"] = years
        return FinancialDocumentParser.parse_json_or_dict(lookup)
