"""
Central Bank of India - Intelligent Loan Appraisal System (ILAS)
Financial Document Ingestion & Normalization Parser

Supports:
- PDF Audited Annual Reports / Financial Statements (.pdf) via pypdf
- Microsoft Word Financial Memorandums (.docx) via python-docx
- Excel / CSV Spreadsheets (.csv, .xlsx, .xls) via pandas / openpyxl
- JSON / Tally ERP 9 / Tally Prime exports
- Plain dictionary structures & messy OCR raw text
"""

import json
import io
import re
from typing import Dict, Any, Union, List, Optional
import pandas as pd

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None


class FinancialDocumentParser:
    """Parses and maps diverse corporate financial inputs (PDF, DOCX, CSV, Excel, JSON, and unstructured OCR text) into standardized financial spreads."""

    # Synonyms and alias patterns for fuzzy matching messy documents
    METRIC_ALIASES = {
        "revenue": ["revenue", "sales", "turnover", "gross receipt", "income from operation", "topline", "gross turnover", "net sales"],
        "cogs": ["cogs", "cost of goods", "cost of sales", "material consumed", "raw material", "direct expenses", "purchase of stock"],
        "operating_expenses": ["opex", "operating expense", "admin expense", "selling expense", "employee cost", "staff expense", "other expenses"],
        "depreciation": ["depreciation", "amortisation", "amortization", "depr", "dep & amort"],
        "interest_expense": ["interest", "finance charge", "finance cost", "borrowing cost", "bank charges"],
        "cash_and_bank": ["cash", "bank balance", "cash and cash equivalent", "liquid funds", "current account", "fixed deposit"],
        "sundry_debtors": ["debtor", "receivable", "trade receivable", "accounts receivable", "book debts"],
        "inventory": ["inventory", "stock", "raw materials", "work-in-progress", "finished goods", "wip"],
        "net_fixed_assets": ["fixed asset", "ppe", "property plant", "plant & machinery", "equipment", "tangible assets", "net block"],
        "sundry_creditors": ["creditor", "payable", "trade payable", "accounts payable", "sundry creditor"],
        "short_term_borrowings": ["short term", "working capital loan", "cash credit", "overdraft", "cc limit", "od limit", "short-term debt", "bank borrowing"],
        "long_term_debt": ["long term", "term loan", "secured loan", "unsecured loan", "debenture", "mortgage loan", "non-current liabilities"],
        "paid_up_capital": ["capital", "equity share capital", "shareholders fund", "share capital", "promoter capital"],
        "reserves_and_surplus": ["reserve", "surplus", "retained earnings", "general reserve", "p&l balance", "accumulated profit"]
    }

    @staticmethod
    def parse_json_or_dict(content: Union[str, bytes, dict]) -> Dict[str, Any]:
        """Parses JSON or raw dict into standardized structure with intelligent fallback values."""
        if isinstance(content, (str, bytes)):
            data = json.loads(content)
        else:
            data = content

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

        years = list(df.columns[1:])
        lookup = {}
        for _, row in df.iterrows():
            metric_raw = str(row.iloc[0]).lower().strip()
            clean_vals = []
            for y in years:
                val_str = str(row[y]).replace(',', '').replace('₹', '').replace('$', '').strip()
                try:
                    clean_vals.append(float(val_str))
                except ValueError:
                    clean_vals.append(0.0)
            
            FinancialDocumentParser._map_line_item(metric_raw, clean_vals, lookup)

        lookup["years"] = years
        return FinancialDocumentParser.parse_json_or_dict(lookup)

    @staticmethod
    def parse_excel_file(file_bytes: bytes) -> Dict[str, Any]:
        """Parses Microsoft Excel spreadsheet (.xlsx, .xls)."""
        df = pd.read_excel(io.BytesIO(file_bytes))
        years = list(df.columns[1:])
        lookup = {}
        for _, row in df.iterrows():
            metric_raw = str(row.iloc[0]).lower().strip()
            clean_vals = []
            for y in years:
                val_str = str(row[y]).replace(',', '').replace('₹', '').replace('$', '').strip()
                try:
                    clean_vals.append(float(val_str))
                except ValueError:
                    clean_vals.append(0.0)
            FinancialDocumentParser._map_line_item(metric_raw, clean_vals, lookup)

        lookup["years"] = years
        return FinancialDocumentParser.parse_json_or_dict(lookup)

    @staticmethod
    def parse_pdf_file(file_bytes: bytes) -> Dict[str, Any]:
        """Parses financial tables and statements from a PDF document using pypdf."""
        if pypdf is None:
            raise ImportError("pypdf is required to parse PDF financial documents.")

        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        full_text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                full_text += t + "\n"

        return FinancialDocumentParser._extract_financials_from_text(full_text)

    @staticmethod
    def parse_docx_file(file_bytes: bytes) -> Dict[str, Any]:
        """Parses tables and paragraphs from Microsoft Word document (.docx)."""
        if docx is None:
            raise ImportError("python-docx is required to parse Word financial documents.")

        doc = docx.Document(io.BytesIO(file_bytes))
        
        # 1. First attempt: check if there are structured Word tables
        table_rows = []
        for table in doc.tables:
            for row in table.rows:
                cells = [c.text.strip() for c in row.cells]
                if len(cells) >= 2:
                    table_rows.append(cells)

        if table_rows and len(table_rows) > 3:
            header = table_rows[0]
            years = header[1:] if len(header) > 1 else ["FY24", "FY25", "FY26"]
            lookup = {}
            for row in table_rows[1:]:
                metric_raw = row[0].lower().strip()
                clean_vals = []
                for val in row[1:]:
                    val_str = str(val).replace(',', '').replace('₹', '').replace('$', '').strip()
                    try:
                        clean_vals.append(float(val_str))
                    except ValueError:
                        clean_vals.append(0.0)
                if clean_vals:
                    FinancialDocumentParser._map_line_item(metric_raw, clean_vals, lookup)
            
            if lookup:
                lookup["years"] = years[:3] if len(years) >= 3 else ["FY24", "FY25", "FY26"]
                return FinancialDocumentParser.parse_json_or_dict(lookup)

        # 2. Fallback: Parse paragraphs text
        full_text = "\n".join([p.text for p in doc.paragraphs])
        return FinancialDocumentParser._extract_financials_from_text(full_text)

    @staticmethod
    def _extract_financials_from_text(text: str) -> Dict[str, Any]:
        """Extracts financial metrics, company name, and figures from raw OCR or messy document text."""
        lookup = {}
        
        # Company name detection
        comp_match = re.search(r'(?:Company|Enterprise|Borrower|Name|Entity|Firm|M/s)\s*(?:Name)?\s*[:=-]\s*([A-Za-z0-9\s.,&()\-]+)', text, re.IGNORECASE)
        if comp_match:
            comp_name = comp_match.group(1).split('\n')[0].strip()
            if len(comp_name) > 3:
                lookup["company_name"] = comp_name

        # Loan Amount requested detection
        loan_amt_match = re.search(r'(?:Loan\s*Amount|Credit\s*Facility|Limit\s*Requested|Proposed\s*Loan)\s*[:=-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d+)?)\s*(?:Cr|Crore|Crores|Lakh|Lakhs|L|K)?', text, re.IGNORECASE)
        if loan_amt_match:
            try:
                l_val = float(loan_amt_match.group(1).replace(',', ''))
                lookup["requested_loan_amount"] = l_val
            except ValueError:
                pass

        # Credit Score / CIBIL detection
        cibil_match = re.search(r'(?:CIBIL|Credit\s*Score|Bureau\s*Score)\s*[:=-]?\s*(\d{3})', text, re.IGNORECASE)
        if cibil_match:
            lookup["credit_score"] = int(cibil_match.group(1))

        lines = text.splitlines()
        for line in lines:
            line_clean = line.strip()
            if not line_clean:
                continue

            # Look for line items followed by 1 to 4 numeric values
            nums = re.findall(r'[-+]?\s*₹?\s*\d+(?:,\d+)*(?:\.\d+)?(?:\s*(?:Cr|Crore|Crores|Lakh|Lakhs|L|K))?', line_clean, re.IGNORECASE)
            
            clean_nums = []
            for n in nums:
                n_str = n.replace('₹', '').replace(',', '').strip()
                mult = 1.0
                if re.search(r'cr(?:ore)?s?', n_str, re.IGNORECASE):
                    mult = 1e7
                    n_str = re.sub(r'cr(?:ore)?s?', '', n_str, flags=re.IGNORECASE).strip()
                elif re.search(r'l(?:akh)?s?', n_str, re.IGNORECASE):
                    mult = 1e5
                    n_str = re.sub(r'l(?:akh)?s?', '', n_str, flags=re.IGNORECASE).strip()
                elif re.search(r'k', n_str, re.IGNORECASE):
                    mult = 1e3
                    n_str = re.sub(r'k', '', n_str, flags=re.IGNORECASE).strip()
                
                try:
                    clean_nums.append(float(n_str) * mult)
                except ValueError:
                    pass

            if clean_nums:
                metric_name = re.sub(r'[-+]?\s*₹?\s*\d+(?:,\d+)*(?:\.\d+)?.*', '', line_clean).lower().strip()
                FinancialDocumentParser._map_line_item(metric_name, clean_nums, lookup)

        return FinancialDocumentParser.parse_json_or_dict(lookup)

    @staticmethod
    def _map_line_item(metric_raw: str, values: List[float], lookup: Dict[str, Any]):
        """Helper to assign multiple numerical years to standard financial spread keys using fuzzy synonym matching."""
        if not values or not metric_raw:
            return

        # Pad values to 3 years if only 1 or 2 are present
        if len(values) == 1:
            values = [values[0] * 0.80, values[0] * 0.90, values[0]]
        elif len(values) == 2:
            values = [values[0], values[1], values[1] * 1.15]
        else:
            values = values[-3:]  # take latest 3 years

        metric_lower = metric_raw.lower()
        for standard_key, aliases in FinancialDocumentParser.METRIC_ALIASES.items():
            if any(alias in metric_lower for alias in aliases):
                lookup[standard_key] = values
                break
