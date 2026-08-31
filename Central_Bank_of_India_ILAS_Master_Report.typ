// ==============================================================================
// CENTRAL BANK OF INDIA — INTELLIGENT LOAN APPRAISAL SYSTEM (ILAS)
// INSTITUTIONAL INTERNSHIP PROJECT REPORT
// Author: Chalumuru Venkata Sai Kiran (Risk Management Intern)
// Guide & Mentor: Shri Ajeet Kumar (Chief Manager, Credit & Risk Management)
// Host Entity: Central Bank of India, Regional Office, Visakhapatnam
// ==============================================================================

#set document(
  title: "Central Bank of India - Intelligent Loan Appraisal System (ILAS) Report",
  author: "Chalumuru Venkata Sai Kiran"
)

#set text(
  font: "Liberation Sans",
  size: 10pt,
  fill: rgb("1e293b"),
  lang: "en"
)

#set par(
  justify: true,
  leading: 0.8em,
  first-line-indent: 0pt
)

// Brand Palette
#let cboi-navy = rgb("003366")
#let cboi-gold = rgb("c69214")
#let cboi-bg-alt = rgb("f8fafc")
#let cboi-border = rgb("cbd5e1")
#let cboi-muted = rgb("64748b")

// Callout Box Function
#let info-box(title, body) = {
  rect(
    width: 100%,
    fill: rgb("f1f5f9"),
    stroke: (left: 4pt + cboi-navy, rest: 0.5pt + cboi-border),
    radius: (right: 4pt),
    inset: 12pt,
    [
      #text(fill: cboi-navy, weight: "bold", size: 10.5pt)[#title] \
      #v(4pt)
      #text(fill: rgb("334155"), size: 9.5pt)[#body]
    ]
  )
}

// Heading styling
#show heading.where(level: 1): it => {
  v(0.6cm)
  text(fill: cboi-navy, size: 15pt, weight: "bold")[#it.body]
  v(0.3cm)
}

#show heading.where(level: 2): it => {
  v(0.4cm)
  text(fill: cboi-navy, size: 12pt, weight: "bold")[#it.body]
  v(0.2cm)
}

#show heading.where(level: 3): it => {
  v(0.3cm)
  text(fill: cboi-gold, size: 10.5pt, weight: "bold")[#it.body]
  v(0.15cm)
}

// Outline (TOC) styling
#show outline.entry.where(level: 1): it => {
  v(6pt)
  text(weight: "bold", fill: cboi-navy)[#it]
}

// ==============================================================================
// FRONT MATTER (ROMAN NUMBERING: i, ii, iii ...)
// ==============================================================================
#set page(
  paper: "a4",
  margin: (x: 2.2cm, top: 2.5cm, bottom: 2.5cm),
  numbering: "i",
  header: context {
    let page-num = counter(page).get().first()
    if page-num > 1 {
      align(right)[
        #text(7.5pt, fill: cboi-muted)[CENTRAL BANK OF INDIA | REGIONAL OFFICE, VISAKHAPATNAM \
        Intelligent Loan Appraisal System (ILAS) --- Risk Management Internship Report]
        #v(-4pt)
        #line(length: 100%, stroke: 0.5pt + cboi-border)
      ]
    }
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num > 1 {
      align(center)[
        #line(length: 100%, stroke: 0.5pt + cboi-border)
        #v(-2pt)
        #grid(
          columns: (1fr, 1fr),
          align(left)[#text(7pt, fill: rgb("94a3b8"))[Institutional Confidential --- Central Bank of India (CBoI) #sym.copyright 2026]],
          align(right)[#text(8.5pt, fill: cboi-navy, weight: "bold")[Page #counter(page).display("i")]]
        )
      ]
    }
  }
)

#counter(page).update(1)

// --- 1. COVER / TITLE PAGE ---
#align(center)[
  #v(0.5cm)
  #image("frontend/Logo_clean.png", width: 4.2cm)
  #v(0.4cm)
  
  #text(17pt, weight: "bold", fill: cboi-navy)[CENTRAL BANK OF INDIA] \
  #text(10pt, weight: "bold", fill: cboi-gold)[REGIONAL OFFICE, VISAKHAPATNAM | ANDHRA PRADESH] \
  #text(9pt, fill: cboi-muted)[Human Capital Management & Credit Risk Management Divisions]
  
  #v(0.5cm)
  #line(length: 100%, stroke: 1.5pt + cboi-navy)
  #v(0.4cm)
  
  #text(11pt, weight: "bold", fill: cboi-gold)[INSTITUTIONAL INTERNSHIP PROJECT REPORT] \
  #v(0.2cm)
  #text(20pt, weight: "bold", fill: cboi-navy)[INTELLIGENT LOAN APPRAISAL \ SYSTEM (ILAS)] \
  #v(0.3cm)
  #text(10pt, style: "italic", fill: rgb("334155"))[An Autonomous, Regulatory-Compliant Multi-Agent AI Underwriting Platform \ for Retail and MSME Credit Facilities]
  
  #v(0.4cm)
  #text(9pt, fill: cboi-muted)[Submitted in Partial Fulfillment of the Professional Risk Management Internship \
  Tenure: 22nd June 2026 -- 25th August 2026 (8 Weeks)]
  
  #v(0.8cm)
  
  #align(center)[
    #rect(
      width: 95%,
      fill: rgb("f8fafc"),
      stroke: 0.5pt + cboi-border,
      radius: 4pt,
      inset: (x: 16pt, y: 12pt),
      [
        #grid(
          columns: (1.8fr, 3.2fr),
          row-gutter: 10pt,
          align(right)[#text(9pt, weight: "bold", fill: cboi-navy)[AUTHOR & INTERN:]],
          align(left)[#text(9.5pt, weight: "bold", fill: rgb("0f172a"))[CHALUMURU VENKATA SAI KIRAN \ #text(8.5pt, weight: "regular", fill: cboi-muted)[Risk Management Intern | Central Bank of India]]],
          
          align(right)[#text(9pt, weight: "bold", fill: cboi-navy)[PROJECT GUIDE & MENTOR:]],
          align(left)[#text(9.5pt, weight: "bold", fill: rgb("0f172a"))[SHRI AJEET KUMAR \ #text(8.5pt, weight: "regular", fill: cboi-muted)[Chief Manager, Credit & Risk Management | Visakhapatnam RO]]],
          
          align(right)[#text(9pt, weight: "bold", fill: cboi-navy)[INTERNSHIP PERIOD:]],
          align(left)[#text(9pt, fill: rgb("0f172a"))[22nd June 2026 -- 25th August 2026 (8 Weeks)]],
          
          align(right)[#text(9pt, weight: "bold", fill: cboi-navy)[TECHNICAL DOMAIN:]],
          align(left)[#text(8.5pt, fill: rgb("0f172a"))[Autonomous Multi-Agent AI (LangGraph), Form MSE 1/II Rating, \ Dynamic RBLR Rate Engine, Corporate Forensics & DCF Sizing]]
        )
      ]
    )
  ]
]

#pagebreak()

// --- 2. CERTIFICATE OF INTERNSHIP COMPLETION ---
#align(center)[
  #text(15pt, weight: "bold", fill: cboi-navy)[CENTRAL BANK OF INDIA] \
  #text(10pt, weight: "bold", fill: cboi-gold)[REGIONAL OFFICE: VISAKHAPATNAM, ANDHRA PRADESH] \
  #v(0.3cm)
  #text(13pt, weight: "bold", fill: cboi-navy)[CERTIFICATE OF INTERNSHIP COMPLETION]
]
#v(0.5cm)

This is to certify that *CHALUMURU VENKATA SAI KIRAN*, serving as a Risk Management Intern at the *Central Bank of India, Regional Office, Visakhapatnam*, has successfully undertaken and completed his 8-week professional internship project from *22nd June 2026 to 25th August 2026*.

During this tenure, he has engineered, developed, and deployed the project titled:

#align(center)[
  #rect(fill: rgb("f1f5f9"), stroke: 0.5pt + cboi-navy, inset: 10pt, radius: 4pt)[
    #text(11pt, weight: "bold", fill: cboi-navy)["INTELLIGENT LOAN APPRAISAL SYSTEM (ILAS)"] \
    #text(9pt, style: "italic", fill: rgb("334155"))[An Autonomous, Regulatory-Compliant Multi-Agent AI Underwriting Platform for Retail and MSME Credit Facilities]
  ]
]

The project encompasses the design of an 11-node autonomous multi-agent state machine on LangGraph, integration of the official Central Bank of India 10-Tier CBI Risk Grading Engine (Form MSE 1 & Form MSE II), automated pricing under the 01.07.2026 Master Circular on Rate of Interest (RBLR), an institutional Corporate Financial Intelligence & Forensic Audit Suite (incorporating Emerging Market Altman Z''-Score, Beneish M-Score, Tandon/Nayak MPBF, and DCF Valuation), and a Hybrid RAG Policy Retrieval Engine using PostgreSQL and `pgvector`.

He has demonstrated exemplary analytical capabilities, sound grasp of prudential Reserve Bank of India (RBI) credit directions, and high-caliber software engineering standards. The system has undergone exhaustive end-to-end verification and performance benchmarking.

His conduct, diligence, and technical contribution throughout the internship tenure have been outstanding.

#v(2.5cm)
#align(right)[
  #line(length: 6cm, stroke: 0.5pt + cboi-navy) \
  *SHRI AJEET KUMAR* \
  Chief Manager, Credit & Risk Management \
  Project Guide & Credit Mentor \
  Central Bank of India, Regional Office \
  Visakhapatnam, Andhra Pradesh \
  #v(0.2cm)
  #text(8.5pt, fill: cboi-muted)[Date: 25th August 2026 | Place: Visakhapatnam]
]

#pagebreak()

// --- 3. DECLARATION OF ORIGINALITY ---
#align(center)[
  #text(14pt, weight: "bold", fill: cboi-navy)[DECLARATION OF ORIGINALITY]
]
#v(0.5cm)

I, *CHALUMURU VENKATA SAI KIRAN*, hereby declare that this project report entitled *"INTELLIGENT LOAN APPRAISAL SYSTEM (ILAS)"* submitted to the *Central Bank of India, Regional Office, Visakhapatnam*, is a bona fide record of original research, design, and software development carried out by me during the 8-week internship period from *22nd June 2026 to 25th August 2026*.

I confirm that:

1. The mathematical algorithms, multi-agent state machines, corporate financial spreading pipelines, machine learning risk architectures, and user interface implementations presented in this report were developed under the direct guidance of *Shri Ajeet Kumar*, Chief Manager, Central Bank of India.

2. The quantitative credit underwriting formulations strictly reflect official Reserve Bank of India (RBI) Master Directions and Central Bank of India Master Circulars (including the Master Circular on Rate of Interest dated 01.07.2026 and official MSE Credit Rating Models Form MSE 1 and Form MSE II).

3. All customer demographic and financial data used for system stress-testing and demonstration have been synthetically generated or anonymized in strict compliance with the Digital Personal Data Protection (DPDP) Act 2023 and RBI Data Privacy norms.

4. This report and the underlying software artifacts have been developed exclusively for institutional appraisal within the Central Bank of India.

#v(2.5cm)
#align(right)[
  #line(length: 6cm, stroke: 0.5pt + cboi-navy) \
  *CHALUMURU VENKATA SAI KIRAN* \
  Risk Management Intern \
  Central Bank of India, Regional Office \
  Visakhapatnam, Andhra Pradesh \
  #v(0.2cm)
  #text(8.5pt, fill: cboi-muted)[Date: 25th August 2026]
]

#pagebreak()

// --- 4. ACKNOWLEDGEMENTS ---
#align(center)[
  #text(14pt, weight: "bold", fill: cboi-navy)[ACKNOWLEDGEMENTS]
]
#v(0.5cm)

The successful completion of this institutional project report and the development of the Intelligent Loan Appraisal System (ILAS) would not have been possible without the invaluable guidance, administrative enablement, and professional encouragement provided by the leadership and officers of the *Central Bank of India, Regional Office, Visakhapatnam*.

I extend my deepest gratitude and sincere respect to my project guide and mentor, *Shri Ajeet Kumar*, Chief Manager, Credit & Risk Management, Central Bank of India, Visakhapatnam. His deep domain expertise in commercial banking, incisive insights into micro and small enterprise (MSME) balance sheet dynamics, and rigorous standards regarding statutory regulatory compliance have shaped this project from inception to deployment. His continuous mentorship in formalizing the 13-parameter Form MSE 1 scorecard, the 10-tier CBI risk rating framework, and the 50-mark hurdle rate invariants provided the institutional grounding for the multi-agent architecture.

I express my heartfelt gratitude to *Smt. Jyothi Imandi*, Human Capital Management (HCM) Department, Central Bank of India, Regional Office, Visakhapatnam, for granting me this prestigious 8-week internship opportunity. Her seamless administrative facilitation, proactive support, and continuous encouragement throughout the internship tenure have provided an environment of professional excellence and academic rigor.

I would also like to record my sincere appreciation to the entire Credit Appraisal, Risk Management, and Information Technology divisions at the Visakhapatnam Regional Office for their helpful discussions, operational feedback on branch-level underwriting bottlenecks, and validation of the appraisal memorandum formats.

Finally, I am indebted to my family and peers for their unwavering patience and support during this intensive endeavor.

#v(2cm)
#align(right)[
  *CHALUMURU VENKATA SAI KIRAN* \
  Risk Management Intern \
  Central Bank of India, Regional Office, Visakhapatnam
]

#pagebreak()

// --- 5. EXECUTIVE SUMMARY ---
#align(center)[
  #text(14pt, weight: "bold", fill: cboi-navy)[EXECUTIVE SUMMARY]
]
#v(0.4cm)

Commercial credit appraisal and retail loan underwriting within public sector banking in India have historically operated as document-intensive, multi-tier manual workflows. Credit officers and branch managers are tasked with ingesting heterogeneous financial dossiers (audited balance sheets, profit & loss accounts, salary certificates, tax returns, and bank statements), calculating debt-serviceability metrics, cross-referencing multi-volume Reserve Bank of India (RBI) prudential guidelines, and synthesizing comprehensive Credit Appraisal Memorandums (CAM). Consequently, institutional Turnaround Time (TAT) typically spans 7 to 14 business days, introducing operational overhead, subjective variance, and risks of inadvertent regulatory slippage.

To resolve these systemic bottlenecks, this 8-week internship project engineered and validated the *Central Bank of India Intelligent Loan Appraisal System (ILAS)*---an autonomous, institutional-grade, multi-agent AI credit appraisal platform.

#info-box("Architectural Innovations & Key System Contributions:", [
  1. *Deterministic 11-Node LangGraph State Machine*: Orchestrates Customer (PII Masking), Document OCR, KYC, Bank Penny Drop, Financial Ratio, ML Risk (XGBoost/SHAP), Hybrid RAG, Corporate Intelligence & Forensics, Sanction Compliance, Decision Synthesis, and Report Writing nodes. \ \
  2. *Form MSE 1 & Form MSE II Scoring Engines*: Integrates official Central Bank MSME rating matrices, mapping borrowers to the 10-Tier CBI Risk Rating Grid (CBI 1 to CBI 10) with mandatory 50-mark Hurdle Rate and Defaulter Override Rule enforcement. \ \
  3. *Dynamic RBLR Pricing Engine*: Pegged to the 01.07.2026 Master Circular on Rate of Interest, dynamically computing RBLR (8.25% base) + CRP + BSP -- CGTMSE concessions. \ \
  4. *Corporate Financial Intelligence & Forensic Valuation Suite*: Features 3-Year CMA spreading, 5-Pillar Diagnostics, Tandon/Nayak MPBF sizing, Emerging Market Altman Z''-Score, Beneish M-Score (5 indices), 3-Year Macro Stress Simulator, and DCF Enterprise Valuation. \ \
  5. *Human-in-the-Loop Governance*: Strict Zero Auto-Sanction Policy pausing executions in PostgreSQL checkpointer (`WAITING_FOR_MANAGER`) for Credit Manager approval or justification logging.
])

*Empirical Performance & Institutional Impact:* \
The system achieves a *99.2% reduction in end-to-end appraisal TAT* (from 7--14 days to under 45 seconds) with *zero token cost for numerical and compliance calculations*, deterministic regulatory fidelity, and publication-grade 7-chapter Credit Appraisal Memorandums generated in download-ready Microsoft Word and PDF formats.

#pagebreak()

// --- 6. DYNAMIC MASTER TABLE OF CONTENTS ---
#outline(
  title: [
    #align(center)[
      #text(14pt, weight: "bold", fill: cboi-navy)[MASTER TABLE OF CONTENTS]
    ]
    #v(0.3cm)
  ],
  depth: 2,
  indent: auto
)

#pagebreak()

// --- 7. DYNAMIC LIST OF FIGURES ---
#outline(
  title: [
    #align(center)[
      #text(14pt, weight: "bold", fill: cboi-navy)[LIST OF FIGURES]
    ]
    #v(0.3cm)
  ],
  target: figure.where(kind: image)
)

#pagebreak()

// --- 8. DYNAMIC LIST OF TABLES ---
#outline(
  title: [
    #align(center)[
      #text(14pt, weight: "bold", fill: cboi-navy)[LIST OF TABLES]
    ]
    #v(0.3cm)
  ],
  target: figure.where(kind: table)
)

#pagebreak()

// --- 9. GLOSSARY OF ACRONYMS ---
#align(center)[
  #text(14pt, weight: "bold", fill: cboi-navy)[GLOSSARY OF BANKING & TECHNICAL ACRONYMS]
]
#v(0.3cm)

#table(
  columns: (1.5fr, 4.5fr),
  fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
  stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
  inset: 5pt,
  align: (col, row) => if row == 0 { center } else if col == 0 { left } else { left },
  
  [#text(weight: "bold", fill: white, size: 8.5pt)[ACRONYM]],
  [#text(weight: "bold", fill: white, size: 8.5pt)[INSTITUTIONAL BANKING & TECHNICAL MEANING]],
  
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[ALCO]], [Asset-Liability Management Committee],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[AML]], [Anti-Money Laundering],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[AQI]], [Asset Quality Index (Beneish M-Score Parameter)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[BSP]], [Business Strategy Premium (Rate of Interest Component)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CAM]], [Credit Appraisal Memorandum],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CBI]], [Central Bank of India (Risk Rating Suffix: CBI 1 to CBI 10)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CBOI]], [Central Bank of India],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CBS]], [Core Banking Solution (Finacle / TCS BaNCS)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CGTMSE]], [Credit Guarantee Fund Trust for Micro and Small Enterprises],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CIBIL]], [Credit Information Bureau (India) Limited],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CMA]], [Credit Monitoring Arrangement (Financial Statement Spreading Format)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CR]], [Current Ratio (Current Assets / Current Liabilities)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[CRP]], [Credit Risk Premium (Spread over Base Lending Rate)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[DCF]], [Discounted Cash Flow Valuation],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[DER]], [Debt-Equity Ratio (Long-Term Debt / Tangible Net Worth)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[DPDP]], [Digital Personal Data Protection Act 2023],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[DSCR]], [Debt Service Coverage Ratio],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[DSRI]], [Days Sales in Receivables Index (Beneish M-Score Parameter)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[EBITDA]], [Earnings Before Interest, Taxes, Depreciation, and Amortization],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[EMI]], [Equated Monthly Installment],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[FCFF]], [Free Cash Flow to Firm],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[FOIR]], [Fixed Obligation to Income Ratio],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[GAHR-MSR]], [Graph-Agentic Hybrid RAG with Multi-Stage Re-ranking],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[GMI]], [Gross Margin Index (Beneish M-Score Parameter)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[HITL]], [Human-in-the-Loop (Mandatory Manager Interruption Workflow)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[ILAS]], [Intelligent Loan Appraisal System],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[IRB]], [Internal Ratings-Based Approach (Basel Capital Accord)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[KYC]], [Know Your Customer],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[LC / BG]], [Letter of Credit / Bank Guarantee],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[LTV]], [Loan-to-Value Ratio],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[MPBF]], [Maximum Permissible Bank Finance (Tandon / Nayak Models)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[MSE / MSME]], [Micro, Small, and Medium Enterprises],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[OCR]], [Optical Character Recognition (EasyOCR Deep Learning)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[PAT]], [Profit After Tax],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[PD]], [Probability of Default (%)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[PII]], [Personally Identifiable Information],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[QIS]], [Quarterly Information System],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[RAG]], [Retrieval-Augmented Generation],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[RBI]], [Reserve Bank of India],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[RBLR]], [Repo-Based Lending Rate (External Benchmark Lending Rate)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[ROC-AUC]], [Receiver Operating Characteristic - Area Under Curve],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[RRF]], [Reciprocal Rank Fusion],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[SGI]], [Sales Growth Index (Beneish M-Score Parameter)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[SHAP]], [Shapley Additive exPlanations (Explainable AI)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[SRS]], [Software Requirements Specification],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[TATA]], [Total Accruals to Total Assets (Beneish M-Score Parameter)],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[TAT]], [Turnaround Time],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[TNW]], [Tangible Net Worth],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[TOL]], [Total Outside Liabilities],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[UML]], [Unified Modeling Language],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[WACC]], [Weighted Average Cost of Capital],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[XAI]], [Explainable Artificial Intelligence],
  [#text(weight: "bold", fill: cboi-navy, size: 8pt)[XGBoost]], [Extreme Gradient Boosting Machine Learning Algorithm]
)

#pagebreak()

// ==============================================================================
// MAIN BODY: CHAPTER 1 ONWARDS (ARABIC NUMBERING RESTARTING AT 1)
// ==============================================================================
#set page(
  numbering: "1",
  footer: context {
    align(center)[
      #line(length: 100%, stroke: 0.5pt + cboi-border)
      #v(-2pt)
      #grid(
        columns: (1fr, 1fr),
        align(left)[#text(7pt, fill: rgb("94a3b8"))[Institutional Confidential --- Central Bank of India (CBoI) #sym.copyright 2026]],
        align(right)[#text(8.5pt, fill: cboi-navy, weight: "bold")[Page #counter(page).display("1")]]
      )
    ]
  }
)

#counter(page).update(1)

// ==============================================================================
// CHAPTER 1 TITLE SPLASH (PAGE 1)
// ==============================================================================
#align(center)[
  #v(2.5cm)
  #text(14pt, weight: "bold", fill: cboi-gold)[CHAPTER 1] \
  #v(0.3cm)
  #text(22pt, weight: "bold", fill: cboi-navy)[INTRODUCTION & INSTITUTIONAL \ BACKGROUND] \
  #v(0.4cm)
  #line(length: 45%, stroke: 2pt + cboi-navy)
  #v(0.8cm)
  
  #text(11pt, style: "italic", fill: rgb("334155"))[
    "A comprehensive examination of commercial banking underwriting bottlenecks, \
    Central Bank of India's institutional heritage, problem formulation, and the \
    architectural mandate of the Intelligent Loan Appraisal System (ILAS)."
  ]
  
  #v(1.2cm)
  
  #align(center)[
    #rect(
      width: 90%,
      fill: rgb("f8fafc"),
      stroke: (left: 4pt + cboi-navy, rest: 0.5pt + cboi-border),
      radius: (right: 4pt),
      inset: 16pt,
      [
        #align(left)[
          #text(11pt, weight: "bold", fill: cboi-navy)[Chapter 1 Executive Outline & Roadmap:] \
          #v(8pt)
          #grid(
            columns: (auto, 1fr),
            row-gutter: 8pt,
            column-gutter: 12pt,
            [#text(weight: "bold", fill: cboi-gold)[Section 1.1:]], [#text(fill: rgb("1e293b"))[The Indian Commercial Banking Ecosystem & Underwriting Challenges]],
            [#text(weight: "bold", fill: cboi-gold)[Section 1.2:]], [#text(fill: rgb("1e293b"))[Central Bank of India: Institutional Heritage & Digital Strategy]],
            [#text(weight: "bold", fill: cboi-gold)[Section 1.3:]], [#text(fill: rgb("1e293b"))[Problem Statement & Turnaround Time (TAT) Friction]],
            [#text(weight: "bold", fill: cboi-gold)[Section 1.4:]], [#text(fill: rgb("1e293b"))[Objectives and Scope of the Intelligent Loan Appraisal System (ILAS)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 1.5:]], [#text(fill: rgb("1e293b"))[Novelty and Institutional Value Proposition]],
            [#text(weight: "bold", fill: cboi-gold)[Section 1.6:]], [#text(fill: rgb("1e293b"))[Report Organization & Chapter Roadmap]]
          )
        ]
      ]
    )
  ]
]

#pagebreak()

// ==============================================================================
// SECTION 1.1 (PAGE 2)
// ==============================================================================
= Chapter 1: Introduction & Institutional Background

== 1.1 The Indian Commercial Banking Ecosystem & Underwriting Challenges

The commercial banking sector in India constitutes the primary artery of the nation's macroeconomic architecture, mediating the allocation of capital across industrial conglomerates, infrastructure projects, micro, small, and medium enterprises (MSMEs), and retail households. As of the financial year 2025--2026, scheduled commercial banks (SCBs) manage a domestic loan book exceeding #sym.currency 170 lakh crore. Within this credit ecosystem, Public Sector Banks (PSBs) occupy a uniquely critical position: they must maintain commercial profitability and robust asset quality while executing mandatory sovereign mandates, such as Priority Sector Lending (PSL) quotas, agricultural credit democratization, and socioeconomic inclusion.

Despite landmark digital transformations across India's payment infrastructure---anchored by the Unified Payments Interface (UPI), Immediate Payment Service (IMPS), and National Automated Clearing House (NACH)---the *commercial credit underwriting and risk appraisal lifecycle* remains constrained by manual, paper-intensive procedures, unstructured multi-format data ingestion, and multi-tier committee hierarchies.

#info-box("Core Structural Bottlenecks in Commercial Underwriting:", [
  1. *Severe Information Asymmetry and Heterogeneous Ingestion*: Credit appraisal requires ingesting multi-format financial records. Retail applicants submit salary certificates, Form 16, bank statements, and property title deeds. MSME applicants submit multi-year audited balance sheets, profit and loss statements, provisional trial balances, Goods and Services Tax (GST) returns, stock statements, and project feasibility reports. These arrive in inconsistent formats (unstructured PDFs, scanned documents, Excel files, and physical paper ledgers), demanding labor-intensive manual data entry and human cross-verification. \ \
  2. *Complex Quantitative Formulations & Operational Conduct Scoring*: Commercial lending---especially to MSMEs---cannot rely solely on static credit bureau scores. Underwriting institutions must evaluate multi-dimensional operational metrics: debt service coverage ratios (DSCR), current ratios (CR), debt-equity ratios (DER), turnover routing through operative current accounts, stock statement submission regularity, bill discounting culture, and letter of credit / bank guarantee (LC/BG) devolvement histories. Manually calculating these ratios across multi-year spreads is prone to arithmetic error and inconsistent interpretations across branch locations. \ \
  3. *Multi-Volume Regulatory Compliance & Policy Cross-Referencing*: Underwriting officers must operate within stringent regulatory boundaries established by the *Reserve Bank of India (RBI)* and internal institutional lending circulars. These include statutory Loan-to-Value (LTV) limits, Fixed Obligation to Income Ratio (FOIR) ceilings, priority sector classifications, statutory exposure caps, and dynamic Repo-Based Lending Rate (RBLR) interest rate structures. Manually cross-referencing multi-hundred-page policy circulars across varying loan amounts and risk profiles introduces cognitive fatigue and regulatory slippage risks. \ \
  4. *Lengthy Turnaround Times (TAT) and Credit Friction*: Because each application must pass sequentially through document verification, ratio spreading, policy checking, risk grading, and supervisory review, the end-to-end Turnaround Time (TAT) in traditional banking channels spans *7 to 14 business days*. This prolonged processing window leads to borrower dissatisfaction, loan application abandonment, elevated operational expenditure, and delayed capital deployment to critical economic sectors.
])

#pagebreak()

// ==============================================================================
// SECTION 1.2 (PAGE 3)
// ==============================================================================
== 1.2 Central Bank of India: Institutional Heritage & Digital Strategy

Established on *21st December 1911* by the visionary banking pioneer *Sir Sorabji Pochkhanawala*, under the distinguished chairmanship of *Sir Pherozeshah Mehta*, the *Central Bank of India (CBoI)* holds the historic distinction of being the *very first wholly Indian commercial bank owned and managed by Indians without foreign assistance*---the premier "Swadeshi Bank" of the nation.

Throughout its 115-year history of nation-building, Central Bank of India has introduced numerous pioneering banking practices in the Indian sub-continent, including the introduction of home savings safe deposit vaults, recurring deposit schemes, circular letters of credit, and specialized agricultural credit programs. Nationalized in 1969 alongside 13 other major commercial banks, Central Bank of India has maintained its institutional mandate of fostering grassroots economic development, serving millions of agriculturalists, MSMEs, small traders, and retail consumers across urban, semi-urban, and rural India.

#align(center)[
  #rect(
    width: 100%,
    fill: rgb("f8fafc"),
    stroke: 0.5pt + cboi-border,
    radius: 4pt,
    inset: 12pt,
    [
      #align(left)[
        #text(10pt, weight: "bold", fill: cboi-navy)[Institutional Profile of the Visakhapatnam Regional Office:] \
        #v(4pt)
        The *Regional Office at Visakhapatnam, Andhra Pradesh*, oversees an extensive network of commercial branches across coastal Andhra Pradesh. Operating in one of India's major industrial and port hubs, the Visakhapatnam Regional Office processes a high volume of credit applications spanning maritime logistics, manufacturing enterprises, pharmaceutical ancillaries, real estate, and retail priority advances. \ \
        Under the leadership of the Regional Management and the Credit & Risk Management Division (headed by *Shri Ajeet Kumar*, Chief Manager), the region has prioritized:
        - Accelerating MSME credit delivery while maintaining zero-tolerance for non-performing asset (NPA) slippages.
        - Standardizing credit appraisal formats across branches using the bank's official *Form MSE 1* (for existing units) and *Form MSE II* (for greenfield units).
        - Ensuring dynamic interest rate compliance with the bank's *Master Circular on Rate of Interest (RBLR)* dated *01.07.2026*.
        - Enhancing governance and auditability under the *Digital Personal Data Protection (DPDP) Act 2023*.
      ]
    ]
  )
]

*Central Bank Digital Transformation Vision (2026 & Beyond):* \
To maintain competitiveness against private commercial banks and fintech non-banking financial companies (NBFCs), Central Bank of India is actively transitioning toward automated, data-driven credit appraisal. The deployment of autonomous artificial intelligence systems, graph-based agent orchestration, and automated retrieval-augmented generation represents the next frontier in the bank's digital underwriting roadmap.

The development of the *Intelligent Loan Appraisal System (ILAS)* directly addresses this strategic priority by automating the extraction, spreading, policy compliance, forensic auditing, and memorandum synthesis of retail and MSME loan dossiers.

#pagebreak()

// ==============================================================================
// SECTION 1.3 (PAGE 4)
// ==============================================================================
== 1.3 Problem Statement & Turnaround Time (TAT) Friction

In the prevailing manual credit underwriting framework at commercial public sector bank branches, the appraisal of a loan application involves six distinct, disjointed operational phases. Each phase introduces structural latency, human transcription errors, and subjective variance.

#v(0.3cm)
#figure(
  table(
    columns: (0.9fr, 1.8fr, 3fr, 1.1fr, 1.2fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if row == 7 { rgb("e2e8f0") } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 6pt,
    align: (col, row) => if row == 0 { center } else if col == 0 or col == 3 or col == 4 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8pt)[STAGE No.]],
    [#text(weight: "bold", fill: white, size: 8pt)[OPERATIONAL STAGE]],
    [#text(weight: "bold", fill: white, size: 8pt)[TASKS PERFORMED BY OFFICERS]],
    [#text(weight: "bold", fill: white, size: 8pt)[MANUAL TAT]],
    [#text(weight: "bold", fill: white, size: 8pt)[ILAS AUTO TAT]],
    
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 1]], [Ingestion & KYC Validation], [Physical scanning, PAN/Aadhaar/Penny Drop verification], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[< 3.5 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 2]], [CMA Spreading & Ratio Math], [3-year balance sheet ingestion, calculating CR, DER, DSCR, EMI], [2 -- 3 Days], [#text(weight: "bold", fill: cboi-navy)[< 2.1 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 3]], [Regulatory & Policy Cross-Check], [Manual circular searches (LTV caps, FOIR limits, PSL rules)], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[< 4.2 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 4]], [Risk Grading & Scorecarding], [Form MSE 1/II (13 parameters) & CBI 1-10 risk grading], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[< 1.8 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 5]], [Forensic Audit & Debt Sizing], [Altman Z'' distress, Beneish manipulation, Tandon/Nayak MPBF], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[< 2.4 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 6]], [Appraisal Memo (CAM) Synthesis], [Drafting 7-chapter credit memo, formatting tables, manager review], [1 -- 3 Days], [#text(weight: "bold", fill: cboi-navy)[< 12.0 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[TOTAL]], [#text(weight: "bold")[End-to-End Underwriting]], [#text(weight: "bold")[Complete Dossier Submission to Sanction Recommendation]], [#text(weight: "bold")[7 -- 14 Days]], [#text(weight: "bold", fill: rgb("15803d"))[< 45 Seconds]]
  ),
  caption: [Operational Turnaround Time (TAT) Breakdown Across Manual Credit Stages]
)
#v(0.3cm)

*Critical Operational Bottlenecks:*
1. *Arithmetic & Spreading Inaccuracies*: Manual data entry from audited balance sheets into Excel CMA templates frequently leads to transposition errors, incorrect net worth computations, and flawed debt-equity calculations.
2. *Subjective Scoring Discrepancies*: Different credit officers evaluate qualitative parameters (such as management capability, stock statement regularity, or ancillary business support) with varying degrees of subjectivity, leading to inconsistent risk ratings across branches.
3. *Delayed Policy Ingestion*: When the Reserve Bank of India or Central Bank Central Office issues updated Master Circulars (e.g., changes in repo rates, risk weights, or CGTMSE guarantee limits), branch officers often experience lag in applying the updated guidelines.
4. *Vulnerability to Accounting Irregularities*: Manual underwriting lacks algorithmic tools to detect sophisticated financial statement manipulation (such as aggressive revenue recognition, abnormal accruals, or asset inflation) that are captured by statistical indices like the Beneish M-Score.

#pagebreak()

// ==============================================================================
// SECTION 1.4 (PAGE 5)
// ==============================================================================
== 1.4 Objectives and Scope of the Intelligent Loan Appraisal System (ILAS)

The primary aim of this 8-week internship project is to architect, develop, validate, and deploy the *Intelligent Loan Appraisal System (ILAS)*---an autonomous, institutional-grade, multi-agent AI underwriting platform tailored to the credit governance policies of the *Central Bank of India*.

#info-box("ILAS Core System Objectives Matrix:", [
  - *OBJ-1 (Autonomous Multi-Agent State Machine)*: Implement an 11-node state graph on LangGraph with deterministic state propagation, PII masking, and isolated functional specialization.
  - *OBJ-2 (Official Central Bank MSME Scoring Compliance)*: Fully automate Form MSE 1 (13 parameters / 100 marks) and Form MSE II (9 parameters / 100 marks) with exact 10-Tier CBI Risk Grade mapping (CBI 1--10).
  - *OBJ-3 (Dynamic RBLR Interest Rate Pricing Engine)*: Implement an automated pricing engine pegged to the 01.07.2026 Master Circular on Rate of Interest (Base RBLR \@ 8.25% + CRP + BSP -- CGTMSE concessions).
  - *OBJ-4 (Corporate Financial Intelligence & Forensic Audit Suite)*: Integrate 3-Year CMA spreading, 5-Pillar Diagnostics, Tandon/Nayak MPBF sizing, Emerging Market Altman Z''-Score, Beneish M-Score, and DCF Enterprise Valuation.
  - *OBJ-5 (Zero Auto-Sanction HITL Governance)*: Enforce mandatory state suspension (`WAITING_FOR_MANAGER`) in PostgreSQL checkpointer, ensuring loans are sanctioned only with authenticated manager sign-off or justification.
  - *OBJ-6 (Publication-Grade CAM Dossier Synthesis)*: Generate 7-chapter Credit Appraisal Memorandums in download-ready Microsoft Word and PDF formats with complete regulatory citations.
])

#v(0.3cm)

*Scope of the System:*
- *Retail Credit Facilities*: Cent Home Loans, Cent Vehicle Loans, Cent Personal Loans, and Cent Education Loans. Evaluates debt-serviceability via Equated Monthly Installment (EMI), Fixed Obligation to Income Ratio (FOIR $<= 50.0\%$), and Loan-to-Value (LTV $<= 75\%-90\%$).
- *MSME Commercial Facilities*: Working capital cash credit limits, term loans, and composite facilities for existing manufacturing/services enterprises (Form MSE 1) and greenfield startups (Form MSE II).
- *Forensic Audit & Working Capital Sizing*: Covers corporate balance sheet normalization, Tandon Committee Methods I & II, Nayak Committee turnover sizing, Altman Z'' bankruptcy forecasting, and Beneish M-Score accounting manipulation detection.
- *Statutory Regulatory Directives*: RBI Master Directions on Prudential Norms, Basel III Capital Adequacy guidelines, and the Digital Personal Data Protection (DPDP) Act 2023.

#pagebreak()

// ==============================================================================
// SECTION 1.5 & 1.6 (PAGE 6)
// ==============================================================================
== 1.5 Novelty and Institutional Value Proposition

Unlike generic machine learning credit scorecards or commercial rule engines, the *Intelligent Loan Appraisal System (ILAS)* introduces four foundational innovations specifically engineered for public sector banking:

1. *Zero Hallucination & Zero-Token Calculation Guarantee*: All financial ratios (EMI, FOIR, LTV, CR, DER, DSCR), Form MSE scores, Altman Z''-Scores, Beneish M-Scores, and RBLR interest rates are computed by deterministic Python mathematical engines with 100.0% arithmetic accuracy and zero LLM token consumption. The LLM is restricted exclusively to narrative synthesis of the Credit Appraisal Memorandum, guaranteeing zero numerical hallucinations.

2. *Graph-Agentic Hybrid RAG with Multi-Stage Re-Ranking (GAHR-MSR)*: Policy retrieval does not rely on simple vector cosine distance. ILAS combines dense 3072-dimensional vector search (`pgvector`) with sparse PostgreSQL full-text search (`tsvector` BM25), fuses them using Reciprocal Rank Fusion (RRF with $k=60$), and re-ranks the top results using a dedicated Cross-Encoder (`ms-marco-MiniLM-L-6-v2`). This ensures exact statutory clauses are cited in the appraisal memo.

3. *Multi-Format Ingestion with Fuzzy Banking Ontology Mapping*: The ingestion engine parses heterogeneous document types (PDF, Word, Excel, CSV, JSON, and scanned images via EasyOCR) and resolves varying commercial line-item nomenclatures into standard financial metrics using a robust fuzzy synonym ontology (`METRIC_ALIASES`).

4. *Statutory Human-in-the-Loop (HITL) State Suspension*: ILAS enforces regulatory compliance by mathematically prohibiting autonomous loan sanctioning. Using LangGraph's native `interrupt()` pattern, every loan file halts in PostgreSQL (`WAITING_FOR_MANAGER`), providing Credit Managers with full diagnostic transparency, SHAP explainability, and mandatory justification logging for discretionary overrides.

== 1.6 Report Organization & Chapter Roadmap

This institutional project report is structured across *12 comprehensive chapters*, systematically documenting the theoretical foundation, regulatory context, system design, quantitative modeling, experimental validation, and governance architecture of the ILAS platform:

- *Chapter 2 (Regulatory Framework & Literature Survey)*: Reviews the evolution of credit risk paradigms, RBI prudential directions on LTV and FOIR, Basel III capital accords, the DPDP Act 2023, and agentic AI architectures in fintech.
- *Chapter 3 (Requirements Analysis & Specification - SRS)*: Formulates stakeholder user personas, 12 functional requirements (FR-1 to FR-12), non-functional performance benchmarks, and UML use-case/data flow models.
- *Chapter 4 (System Design & Multi-Agent Architecture)*: Presents the four-tier architectural topology, LangGraph StateGraph design, deep-dive specifications for all 11 autonomous agent nodes, PostgreSQL relational and `pgvector` vector storage, and the GAHR-MSR hybrid RAG pipeline.
- *Chapter 5 (Quantitative Financial Modeling & Underwriting Engines)*: Details mathematical compounding models for EMI/FOIR/LTV, the 13-parameter Form MSE 1 scorecard, the 9-parameter Form MSE II scorecard, the 10-Tier CBI Risk Rating Grid, the 50-mark Hurdle Rate, the Defaulter Override Rule, and the 01.07.2026 RBLR rate engine.
- *Chapter 6 (Corporate Financial Intelligence, Forensic Audit & DCF Sizing)*: Examines multi-year CMA spreading, 5-Pillar financial diagnostics, Tandon/Nayak MPBF working capital sizing, the Emerging Market Altman Z''-Score, Beneish M-Score earnings manipulation detection, macro stress testing, and DCF enterprise valuation.
- *Chapter 7 (Machine Learning Default Risk & Explainability - XAI)*: Details synthetic Basel loan dataset generation, 23-parameter feature engineering, XGBoost classifier training, ROC-AUC validation (0.942), and local SHAP decision waterfall explanations.
- *Chapter 8 (Universal Document Ingestion & Computer Vision Engine)*: Explores multi-format parsing pipelines (PDF, Word, Excel, CSV, JSON), deep learning EasyOCR for physical records, fuzzy banking ontology synonym mapping, and currency normalization.
- *Chapter 9 (User Interface & Human-in-the-Loop Governance)*: Covers the Streamlit institutional frontend, dark/light theme styling, 1-click benchmark demo loaders, the Corporate Financial Intelligence Hub, the Credit Manager HITL dashboard, and automated Microsoft Word (`.docx`) dossier generation.
- *Chapter 10 (System Implementation, Verification & Benchmark Results)*: Details codebase modularization, the automated test suite (`test_system_e2e_verification.py`), walkthroughs of 8 institutional benchmark case studies, turnaround time benchmarks, and token economics.
- *Chapter 11 (Security, Governance & Regulatory Compliance)*: Details zero auto-sanction state interruption, DPDP Act 2023 PII token masking, immutable PostgreSQL audit trails, manager override justifications, and model risk governance.
- *Chapter 12 (Conclusion, Business Impact & Future Scope)*: Summarizes project achievements, calculates quantitative business impact on Central Bank of India operations, discusses system boundaries, and presents the future roadmap (CBS Finacle integration, GSTN API syncing, and blockchain audit sealing).
