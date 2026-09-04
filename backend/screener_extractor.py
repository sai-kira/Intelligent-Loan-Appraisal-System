import os
import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

sys.stdout.reconfigure(encoding='utf-8')

REPO_OUT_DIR = r"C:\Users\Karma\.gemini\antigravity\worktrees\Intelligent-Loan-Appraisal-System\build-ai-loan-appraisal\sample_financial_documents\screener_companies"
DESKTOP_OUT_DIR = r"C:\Users\Karma\OneDrive\Desktop\ILAS_Sample_Test_Documents\Screener_Companies"

os.makedirs(REPO_OUT_DIR, exist_ok=True)
os.makedirs(DESKTOP_OUT_DIR, exist_ok=True)

COMPANIES_DATA = [
    {
        "ticker": "AVANTEL",
        "company_name": "Avantel Ltd",
        "sector": "Defence & Satellite Communications",
        "cibil_score": 795,
        "requested_loan": 25000000.0,
        "loan_type": "MSME Loan - Existing Unit",
        "years": ["FY24", "FY25", "FY26"],
        "pnl": {
            "Gross Turnover / Revenue": [2240000000.0, 2480000000.0, 2210000000.0],
            "Other Income": [10000000.0, 20000000.0, 20000000.0],
            "Cost of Materials Consumed / COGS": [1080000000.0, 1180000000.0, 1220000000.0],
            "Operating Expenses": [320000000.0, 350000000.0, 460000000.0],
            "Depreciation": [70000000.0, 110000000.0, 180000000.0],
            "Interest Expense": [40000000.0, 30000000.0, 60000000.0],
            "Net Profit (PAT)": [550000000.0, 600000000.0, 220000000.0],
        },
        "balance_sheet": {
            "Paid Up Capital / Equity": [490000000.0, 490000000.0, 530000000.0],
            "Reserves and Surplus": [1230000000.0, 1990000000.0, 3030000000.0],
            "Long Term Debt / Borrowings": [180000000.0, 260000000.0, 340000000.0],
            "Short Term Borrowings": [150000000.0, 190000000.0, 250000000.0],
            "Sundry Creditors": [190000000.0, 220000000.0, 110000000.0],
            "Other Current Liabilities": [340000000.0, 230000000.0, 360000000.0],
            "Net Fixed Assets": [440000000.0, 950000000.0, 1620000000.0],
            "Cash and Bank Balances": [180000000.0, 220000000.0, 280000000.0],
            "Sundry Debtors / Receivables": [640000000.0, 710000000.0, 710000000.0],
            "Inventories": [650000000.0, 1100000000.0, 1660000000.0],
            "Other Current Assets": [320000000.0, 250000000.0, 270000000.0],
        }
    },
    {
        "ticker": "ZENTEC",
        "company_name": "Zen Technologies Ltd",
        "sector": "Defence Simulators & Drone Systems",
        "cibil_score": 820,
        "requested_loan": 50000000.0,
        "loan_type": "MSME Loan - Existing Unit",
        "years": ["FY24", "FY25", "FY26"],
        "pnl": {
            "Gross Turnover / Revenue": [4300000000.0, 9310000000.0, 4240000000.0],
            "Other Income": [10000000.0, 580000000.0, 770000000.0],
            "Cost of Materials Consumed / COGS": [1800000000.0, 4800000000.0, 2100000000.0],
            "Operating Expenses": [730000000.0, 1370000000.0, 780000000.0],
            "Depreciation": [70000000.0, 100000000.0, 140000000.0],
            "Interest Expense": [20000000.0, 90000000.0, 30000000.0],
            "Net Profit (PAT)": [1290000000.0, 2630000000.0, 1460000000.0],
        },
        "balance_sheet": {
            "Paid Up Capital / Equity": [80000000.0, 90000000.0, 90000000.0],
            "Reserves and Surplus": [4450000000.0, 16800000000.0, 18130000000.0],
            "Long Term Debt / Borrowings": [10000000.0, 540000000.0, 20000000.0],
            "Short Term Borrowings": [50000000.0, 120000000.0, 80000000.0],
            "Sundry Creditors": [350000000.0, 820000000.0, 580000000.0],
            "Other Current Liabilities": [2290000000.0, 1200000000.0, 1110000000.0],
            "Net Fixed Assets": [790000000.0, 1050000000.0, 1280000000.0],
            "Cash and Bank Balances": [850000000.0, 2100000000.0, 2450000000.0],
            "Sundry Debtors / Receivables": [1680000000.0, 3770000000.0, 1310000000.0],
            "Inventories": [1740000000.0, 710000000.0, 1520000000.0],
            "Other Current Assets": [2120000000.0, 11120000000.0, 12770000000.0],
        }
    },
    {
        "ticker": "PRECAM",
        "company_name": "Precision Camshafts Ltd",
        "sector": "Precision Engineering & Auto Components (MSME)",
        "cibil_score": 765,
        "requested_loan": 35000000.0,
        "loan_type": "MSME Loan - Existing Unit",
        "years": ["FY24", "FY25", "FY26"],
        "pnl": {
            "Gross Turnover / Revenue": [6750000000.0, 6120000000.0, 5780000000.0],
            "Other Income": [380000000.0, 150000000.0, 140000000.0],
            "Cost of Materials Consumed / COGS": [3600000000.0, 3320000000.0, 3180000000.0],
            "Operating Expenses": [2000000000.0, 1950000000.0, 1980000000.0],
            "Depreciation": [400000000.0, 400000000.0, 330000000.0],
            "Interest Expense": [50000000.0, 50000000.0, 40000000.0],
            "Net Profit (PAT)": [780000000.0, 70000000.0, 60000000.0],
        },
        "balance_sheet": {
            "Paid Up Capital / Equity": [950000000.0, 950000000.0, 950000000.0],
            "Reserves and Surplus": [7950000000.0, 7930000000.0, 7920000000.0],
            "Long Term Debt / Borrowings": [590000000.0, 720000000.0, 420000000.0],
            "Short Term Borrowings": [210000000.0, 180000000.0, 160000000.0],
            "Sundry Creditors": [1400000000.0, 1250000000.0, 1300000000.0],
            "Other Current Liabilities": [500000000.0, 560000000.0, 520000000.0],
            "Net Fixed Assets": [2490000000.0, 2210000000.0, 2640000000.0],
            "Cash and Bank Balances": [620000000.0, 580000000.0, 510000000.0],
            "Sundry Debtors / Receivables": [1370000000.0, 1510000000.0, 1120000000.0],
            "Inventories": [2520000000.0, 2000000000.0, 1680000000.0],
            "Other Current Assets": [3650000000.0, 4460000000.0, 4610000000.0],
        }
    }
]

def generate_excel_balance_sheet(comp, out_path):
    rows = []
    years = comp["years"]
    for k, vals in comp["balance_sheet"].items():
        rows.append([k] + vals)
    df = pd.DataFrame(rows, columns=["Particulars / Line Item"] + years)
    df.to_excel(out_path, index=False, engine='openpyxl')

def generate_csv_pnl(comp, out_path):
    rows = []
    years = comp["years"]
    for k, vals in comp["pnl"].items():
        rows.append([k] + vals)
    df = pd.DataFrame(rows, columns=["Particulars / Line Item"] + years)
    df.to_csv(out_path, index=False)

def generate_pdf_report(comp, out_path):
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#003366'),
        spaceAfter=8
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#CC0000'),
        spaceBefore=10,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=9,
        leading=13
    )

    story = []
    story.append(Paragraph(f"<b>AUDITED ANNUAL FINANCIAL STATEMENTS & CREDIT DOSSIER</b>", title_style))
    story.append(Paragraph(f"<b>Borrower Entity:</b> {comp['company_name']}<br/><b>Exchange Ticker:</b> {comp['ticker']} (Screener.in) | <b>Industry:</b> {comp['sector']}<br/><b>CIBIL Bureau Score:</b> {comp['cibil_score']} | <b>Requested Credit Facility:</b> INR {comp['requested_loan']:,.0f}", body_style))
    story.append(Spacer(1, 10))

    # P&L Table
    story.append(Paragraph("<b>1. Profit & Loss Account (Figures in INR)</b>", h2_style))
    pnl_data = [["Particulars / Financial Indicator"] + comp["years"]]
    for k, vals in comp["pnl"].items():
        pnl_data.append([k] + [f"{v:,.0f}" for v in vals])
    
    t_pnl = Table(pnl_data, colWidths=[240, 95, 95, 95])
    t_pnl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_pnl)
    story.append(Spacer(1, 12))

    # Balance Sheet Table
    story.append(Paragraph("<b>2. Balance Sheet (Figures in INR)</b>", h2_style))
    bs_data = [["Balance Sheet Particulars"] + comp["years"]]
    for k, vals in comp["balance_sheet"].items():
        bs_data.append([k] + [f"{v:,.0f}" for v in vals])
    
    t_bs = Table(bs_data, colWidths=[240, 95, 95, 95])
    t_bs.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#CC0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_bs)
    story.append(Spacer(1, 12))

    doc.build(story)

def main():
    for comp in COMPANIES_DATA:
        t = comp["ticker"]
        safe_name = comp["company_name"].replace(" ", "_")

        f_bs_xlsx = f"{safe_name}_Audited_Balance_Sheet.xlsx"
        f_pnl_csv = f"{safe_name}_Profit_and_Loss.csv"
        f_pdf = f"{safe_name}_Annual_Report_Dossier.pdf"

        for base_dir in [REPO_OUT_DIR, DESKTOP_OUT_DIR]:
            p_bs = os.path.join(base_dir, f_bs_xlsx)
            p_pnl = os.path.join(base_dir, f_pnl_csv)
            p_pdf = os.path.join(base_dir, f_pdf)

            generate_excel_balance_sheet(comp, p_bs)
            generate_csv_pnl(comp, p_pnl)
            generate_pdf_report(comp, p_pdf)

        print(f"Generated multi-file suite for {comp['company_name']} ({t}):")
        print(f"   - {f_bs_xlsx}")
        print(f"   - {f_pnl_csv}")
        print(f"   - {f_pdf}")

    print(f"\nAll files successfully generated and saved to:")
    print(f"1. {REPO_OUT_DIR}")
    print(f"2. {DESKTOP_OUT_DIR}")

if __name__ == "__main__":
    main()
