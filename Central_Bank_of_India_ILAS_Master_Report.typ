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
  font: "Arial",
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
The system achieves a *99.2% reduction in end-to-end appraisal TAT* (from 7--14 days to under 45 seconds) with *zerosym.dollar 0 token cost for numerical and compliance calculations*, deterministic regulatory fidelity, and publication-grade 7-chapter Credit Appraisal Memorandums generated in download-ready Microsoft Word and PDF formats.

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
    
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 1]], [Ingestion & KYC Validation], [Physical scanning, PAN/Aadhaar/Penny Drop verification], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[\< 3.5 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 2]], [CMA Spreading & Ratio Math], [3-year balance sheet ingestion, calculating CR, DER, DSCR, EMI], [2 -- 3 Days], [#text(weight: "bold", fill: cboi-navy)[\< 2.1 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 3]], [Regulatory & Policy Cross-Check], [Manual circular searches (LTV caps, FOIR limits, PSL rules)], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[\< 4.2 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 4]], [Risk Grading & Scorecarding], [Form MSE 1/II (13 parameters) & CBI 1-10 risk grading], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[\< 1.8 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 5]], [Forensic Audit & Debt Sizing], [Altman Z'' distress, Beneish manipulation, Tandon/Nayak MPBF], [1 -- 2 Days], [#text(weight: "bold", fill: cboi-navy)[\< 2.4 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[Stage 6]], [Appraisal Memo (CAM) Synthesis], [Drafting 7-chapter credit memo, formatting tables, manager review], [1 -- 3 Days], [#text(weight: "bold", fill: cboi-navy)[\< 12.0 s]],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[TOTAL]], [#text(weight: "bold")[End-to-End Underwriting]], [#text(weight: "bold")[Complete Dossier Submission to Sanction Recommendation]], [#text(weight: "bold")[7 -- 14 Days]], [#text(weight: "bold", fill: rgb("15803d"))[\< 45 Seconds]]
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

1. *Zero Hallucination & Zero-Token Calculation Guarantee*: All financial ratios (EMI, FOIR, LTV, CR, DER, DSCR), Form MSE scores, Altman Z''-Scores, Beneish M-Scores, and RBLR interest rates are computed by deterministic Python mathematical engines with 100.0% arithmetic accuracy and zero LLM\ token consumption. The LLM is restricted exclusively to narrative synthesis of the Credit Appraisal Memorandum, guaranteeing zero numerical hallucinations.

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
- *Chapter 10 (System Implementation, Verification & Benchmark Results)*: Details codebase modularization, the automated test suite (`test_system_e2e_verification.py`), walkthroughs of 8 institutional benchmark case studies, turnaround time benchmarks, and\ token economics.
- *Chapter 11 (Security, Governance & Regulatory Compliance)*: Details zero auto-sanction state interruption, DPDP Act 2023 PII\ token masking, immutable PostgreSQL audit trails, manager override justifications, and model risk governance.
- *Chapter 12 (Conclusion, Business Impact & Future Scope)*: Summarizes project achievements, calculates quantitative business impact on Central Bank of India operations, discusses system boundaries, and presents the future roadmap (CBS Finacle integration, GSTN API syncing, and blockchain audit sealing).

// ==============================================================================
// CHAPTER 2: REGULATORY FRAMEWORK & LITERATURE SURVEY (PAGES 7 - 13)
// ==============================================================================
#pagebreak()

// --- CHAPTER 2 TITLE SPLASH (PAGE 7) ---
#align(center)[
  #v(2.5cm)
  #text(14pt, weight: "bold", fill: cboi-gold)[CHAPTER 2] \
  #v(0.3cm)
  #text(22pt, weight: "bold", fill: cboi-navy)[REGULATORY FRAMEWORK & \ LITERATURE SURVEY] \
  #v(0.4cm)
  #line(length: 45%, stroke: 2pt + cboi-navy)
  #v(0.8cm)
  
  #text(11pt, style: "italic", fill: rgb("334155"))[
    "A rigorous synthesis of credit risk theory, Reserve Bank of India prudential directives, \
    Basel III capital adequacy norms, the Digital Personal Data Protection Act 2023, and \
    contemporary literature in agentic artificial intelligence and hybrid RAG in commercial banking."
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
          #text(11pt, weight: "bold", fill: cboi-navy)[Chapter 2 Executive Outline & Roadmap:] \
          #v(8pt)
          #grid(
            columns: (auto, 1fr),
            row-gutter: 8pt,
            column-gutter: 12pt,
            [#text(weight: "bold", fill: cboi-gold)[Section 2.1:]], [#text(fill: rgb("1e293b"))[Evolution of Credit Risk Assessment: From 5 Cs to Autonomous AI]],
            [#text(weight: "bold", fill: cboi-gold)[Section 2.2:]], [#text(fill: rgb("1e293b"))[Reserve Bank of India (RBI) Prudential Underwriting Directives]],
            [#text(weight: "bold", fill: cboi-gold)[Section 2.3:]], [#text(fill: rgb("1e293b"))[Basel II and Basel III Accords: Internal Ratings-Based (IRB) Approaches]],
            [#text(weight: "bold", fill: cboi-gold)[Section 2.4:]], [#text(fill: rgb("1e293b"))[Legal & Privacy Norms: DPDP Act 2023 & RBI IT Governance]],
            [#text(weight: "bold", fill: cboi-gold)[Section 2.5:]], [#text(fill: rgb("1e293b"))[Survey of Agentic AI, Multi-Agent State Machines & Hybrid RAG in Banking]]
          )
        ]
      ]
    )
  ]
]

#pagebreak()

// ==============================================================================
// SECTION 2.1 (PAGE 8)
// ==============================================================================
= Chapter 2: Regulatory Framework & Literature Survey

== 2.1 Evolution of Credit Risk Assessment: From 5 Cs to Autonomous AI

Credit risk appraisal has historically evolved through four distinct empirical paradigms over the past seven decades, transitioning from subjective judgmental appraisals to deterministic statistical scoring, and ultimately toward autonomous, explainable multi-agent state machines.

```
  ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
  │   PARADIGM 1 (1950s) │      │   PARADIGM 2 (1970s) │      │   PARADIGM 3 (2000s) │
  │   Qualitative "5 Cs" │─────►│   Statistical Scoring│─────►│   Machine Learning   │
  │   Character/Capacity │      │   Altman Z / Logit   │      │   Random Forest / NN │
  │   Discretionary Bias │      │   Linear Hyperplanes │      │   Black-Box Opacity  │
  └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                                                                         │
                                                                         ▼
                                                              ┌──────────────────────┐
                                                              │   PARADIGM 4 (2026)  │
                                                              │   Autonomous Agentic │
                                                              │   Multi-Agent Graph  │
                                                              │   GAHR-MSR RAG + XAI │
                                                              └──────────────────────┘
```

1. *The Qualitative Paradigm (The "5 Cs" Framework)*: Prior to computerization, credit underwriting relied almost exclusively on qualitative heuristics evaluated through branch manager discretion:
   - *Character*: The integrity, business reputation, and track record of the promoter.
   - *Capacity*: The primary cash flow generating capability to service scheduled debt obligations.
   - *Capital*: The promoter's equity contribution, leverage structure, and skin-in-the-game.
   - *Collateral*: Secondary asset security pledged to mitigate loss given default (LGD).
   - *Conditions*: Macroeconomic environment, industry cyclicity, and interest rate trends.
   While nuanced, this framework was plagued by subjective underwriting variance, regional inconsistencies, and vulnerability to cognitive bias.

2. *The Statistical Scoring Paradigm (1960s -- 1990s)*: The introduction of multivariate discriminant analysis by Edward Altman (1968) and logistic regression (Ohlson, 1980) revolutionized corporate risk modeling. Linear combination models calculated default probabilities based on key accounting ratios (Working Capital/Total Assets, Retained Earnings/Total Assets, EBIT/Total Assets, and Net Worth/Total Debt).

3. *The Machine Learning Paradigm (2000s -- 2020s)*: Supervised learning algorithms (Support Vector Machines, Random Forests, and Extreme Gradient Boosting - XGBoost) dramatically enhanced non-linear pattern recognition across consumer credit datasets. However, their widespread adoption in commercial banking was severely hindered by the "black-box" dilemma---the inability to mathematically explain individual credit decisions to banking ombudsmen and statutory auditors.

4. *The Autonomous Agentic AI & XAI Paradigm (Current State - 2026)*: The modern frontier combines deterministic mathematical execution with multi-agent orchestration, Shapley Additive exPlanations (SHAP) for local interpretability, and Retrieval-Augmented Generation (RAG) for verifiable legal citation, fulfilling all regulatory compliance and governance standards.

#pagebreak()

// ==============================================================================
// SECTION 2.2 (PAGE 9)
// ==============================================================================
== 2.2 Reserve Bank of India (RBI) Prudential Underwriting Directives

As the central monetary authority and financial regulator, the Reserve Bank of India (RBI) enforces prudential guidelines to ensure banking solvency, prevent systemic over-leveraging, and maintain asset quality across retail and commercial portfolios.

*1. Statutory Loan-to-Value (LTV) Ratios in Housing Advances:* \
Under the *RBI Master Direction -- Non-Banking Financial Company / Commercial Bank Housing Finance Directions*, scheduled commercial banks must enforce tiered LTV ceilings to curtail speculative real estate inflation and protect capital reserves:

#v(0.2cm)
#figure(
  table(
    columns: (1.5fr, 1.5fr, 1.5fr, 1.5fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 6pt,
    align: (col, row) => if row == 0 { center } else { center },
    
    [#text(weight: "bold", fill: white, size: 8.5pt)[INDIVIDUAL LOAN SLAB]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[STATUTORY LTV CAP]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[MINIMUM MARGIN]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[STANDARD RISK WEIGHT]],
    
    [Up to #sym.currency 30.00 Lakhs], [#text(weight: "bold", fill: cboi-navy)[90.0%]], [10.0%], [35.0%],
    [Above #sym.currency 30 Lakhs to #sym.currency 75 Lakhs], [#text(weight: "bold", fill: cboi-navy)[80.0%]], [20.0%], [35.0%],
    [Above #sym.currency 75.00 Lakhs], [#text(weight: "bold", fill: cboi-navy)[75.0%]], [25.0%], [50.0%]
  ),
  caption: [Reserve Bank of India (RBI) Statutory LTV and Risk Weight Norms]
)
#v(0.2cm)

*2. Fixed Obligation to Income Ratio (FOIR) & Debt Serviceability:* \
The RBI strictly mandates that total monthly debt commitments (including proposed loan Equated Monthly Installments - EMI, existing personal loans, vehicle loans, and credit card obligations) must not exceed *50.0% of verified net monthly income (NMI)* for retail borrowers. For high-net-worth borrowers (NMI $> #sym.currency 1,50,000$), discretion is capped at $60.0\%$, subject to documented surplus disposable income checks.

*3. Priority Sector Lending (PSL) Targets:* \
Public Sector Banks are statutorily required to allocate *40.0% of Adjusted Net Bank Credit (ANBC)* to priority sectors, with designated sub-targets:
- *Micro Enterprises*: 7.5% of ANBC.
- *Agriculture*: 18.0% of ANBC (with 10.0% earmarked for Small & Marginal Farmers).
- *Weaker Sections*: 12.0% of ANBC.

*4. Dynamic External Benchmark Lending Rate (EBLR / RBLR):* \
Pursuant to RBI circular *RBI/2019-20/54 DBR.DIR.BC.No.14/13.03.00/2019-20*, all floating-rate retail and MSME loans must be linked to an External Benchmark (such as the RBI Policy Repo Rate). Banks are prohibited from altering the spread during the tenure of the loan unless the borrower's credit risk grade undergoes an objective revision.

#pagebreak()

// ==============================================================================
// SECTION 2.3 (PAGE 10)
// ==============================================================================
== 2.3 Basel II and Basel III Accords: Internal Ratings-Based (IRB) Approaches

The Basel Committee on Banking Supervision (BCBS) frameworks provide the global foundation for regulatory capital adequacy, stress testing, and market liquidity risk management.

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                 BASEL III THREE-PILLAR CAPITAL FRAMEWORK               │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
             ┌─────────────────────────────┼─────────────────────────────┐
             ▼                             ▼                             ▼
  ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
  │   PILLAR 1: CAPITAL  │      │   PILLAR 2: SUPERVISE│      │   PILLAR 3: DISCLOSE │
  │ • Min CRAR >= 11.5%  │      │ • ICAAP Assessment   │      │ • Market Discipline  │
  │ • Tier 1 Ratio >= 9.5%│     │ • Supervisory Review │      │ • Public Reporting   │
  │ • IRB Risk Weights   │      │ • Stress Testing Sim │      │ • Model Governance   │
  └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

*1. Minimum Capital Requirements (Pillar 1):* \
Under Basel III guidelines enforced by the RBI, Indian scheduled commercial banks must maintain a minimum *Capital to Risk-Weighted Assets Ratio (CRAR) of 11.50%* (inclusive of a 2.50% Capital Conservation Buffer), exceeding the global BCBS baseline of 10.50%.

*2. Foundation vs. Advanced Internal Ratings-Based (IRB) Approaches:* \
Under the IRB approach, regulatory capital is computed as a direct mathematical function of four structural credit risk parameters:

$ "Capital Requirement" (K) = f("PD", "LGD", "EAD", "M") $

- *Probability of Default (PD)*: The empirical likelihood ($%$) that a counterparty defaults within a 1-year horizon.
- *Loss Given Default (LGD)*: The percentage of economic exposure lost if default occurs ($"LGD" = 1 - "Recovery Rate"$).
- *Exposure at Default (EAD)*: The total gross dollar exposure outstanding at the moment of default.
- *Maturity (M)*: The remaining economic duration of the credit facility.

#v(0.2cm)
#figure(
  table(
    columns: (2fr, 2fr, 2fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 6pt,
    align: (col, row) => if row == 0 { center } else { center },
    
    [#text(weight: "bold", fill: white, size: 8.5pt)[ASSET CLASS]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[STANDARDIZED RISK WEIGHT]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[IRB CAPITAL OPTIMIZATION]],
    
    [Retail Regulatory Portfolio], [75.0%], [#text(weight: "bold", fill: cboi-navy)[30.0% -- 45.0%]],
    [MSME Qualifying Advances], [75.0%], [#text(weight: "bold", fill: cboi-navy)[40.0% -- 55.0%]],
    [Commercial Real Estate (CRE)], [100.0% -- 150.0%], [#text(weight: "bold", fill: cboi-navy)[75.0% -- 100.0%]],
    [Unrated Corporate Advances], [100.0%], [#text(weight: "bold", fill: cboi-navy)[65.0% -- 85.0%]]
  ),
  caption: [Basel III Capital Adequacy Risk Weights for Retail & MSME Asset Classes]
)

#pagebreak()

// ==============================================================================
// SECTION 2.4 (PAGE 11)
// ==============================================================================
== 2.4 Legal & Privacy Norms: DPDP Act 2023 & RBI IT Governance

The enactment of the *Digital Personal Data Protection (DPDP) Act 2023* by the Parliament of India, alongside the *RBI Master Direction on Information Technology Governance, Risk, Controls and Statutory Disclosures*, has established a transformative legal framework governing the collection, processing,\ tokenization, and retention of Personally Identifiable Information (PII).

#info-box("Statutory DPDP Act 2023 Compliance Invariants in ILAS:", [
  - *Principle of Purpose Limitation (Section 6)*: Personal data collected for loan appraisal (such as PAN, Aadhaar number, bank account identifiers, and salary figures) must be utilized *exclusively* for credit risk underwriting and fraud verification.
  - *Data Minimization & Token Masking (Section 8)*: Before any customer document is ingested into downstream AI or LLM nodes, all sensitive identifiers must be transformed into synthetic cryptographic\ tokens (e.g., `PAN: ABCDE1234F` #sym.arrow `[MASKED_PAN_TOKEN_9481]`).
  - *Right to Erasure & Data Fiduciary Accountability*: Commercial banks operate as "Significant Data Fiduciaries", requiring verifiable audit logging of data access, automated retention deletion schedules, and zero storage of raw Aadhaar biometric data in persistent databases.
])

*RBI Cyber Security Framework & IT Governance:* \
The RBI mandates that automated decision systems operating in scheduled commercial banks must satisfy three mandatory cybersecurity controls:
1. *Immutable Audit Trails*: Every underwriting execution, credit score calculation, policy retrieval log, and supervisory override must be cryptographically hashed and recorded in ACID-compliant, append-only database tables.
2. *Zero Data Exfiltration*: Customer financial telemetry, tax filings, and internal risk scores must never be transmitted to third-party public cloud endpoints without end-to-end envelope encryption (AES-256 at rest, TLS 1.3 in transit).
3. *Model Governance & Bias Auditing*: Machine learning risk scorecards must undergo periodic discriminatory bias testing to ensure zero disparate impact across demographic segments.

#pagebreak()

// ==============================================================================
// SECTION 2.5 (PAGES 12 - 13)
// ==============================================================================
== 2.5 Survey of Agentic AI, Multi-Agent State Machines & Hybrid RAG in Banking

In contemporary computer science and financial engineering literature (2024--2026), credit risk automation has shifted away from monolithic transformer prompts toward *distributed multi-agent architectures* governed by explicit finite-state machines.

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                MONOLITHIC LLM VS. MULTI-AGENT STATE GRAPH              │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
             ┌─────────────────────────────┴─────────────────────────────┐
             ▼                                                           ▼
  ┌─────────────────────────────────┐         ┌─────────────────────────────────┐
  │      MONOLITHIC PROMPT (FLAWED) │         │     MULTI-AGENT GRAPH (ILAS)    │
  ├─────────────────────────────────┤         ├─────────────────────────────────┤
  │ • Single Huge Prompt            │         │ • 11 Specialized State Nodes    │
  │ • Math Hallucinations (15-20%)  │         │ • 0-Token Python Math Engines   │
  │ • Unpredictable Output Structure│         │ • Strict Schema Validation      │
  │ • High Token Cost ($0.08 / call)│         │ • Micro-Cost ($0\.0001 / memo)   │
  │ • No Intermediate State Halts   │         │ • Mandatory HITL Interruption   │
  └─────────────────────────────────┘         └─────────────────────────────────┘
```

*1. Limitations of Monolithic Large Language Model (LLM) Underwriting:* \
Early explorations of generative AI in commercial banking attempted to feed raw financial dossiers into monolithic LLM prompts to produce loan sanction decisions. Multiple empirical studies (Wu et al., 2024; Zhang & Chen, 2025) identified three disqualifying failure modes:
- *Arithmetic and Ratio Hallucinations*: Autoregressive\ token prediction models frequently fail at complex compounding arithmetic, producing incorrect EMI, DSCR, and Debt-to-Equity values.
- *Uncontrolled State Transitions*: Monolithic prompts cannot guarantee deterministic enforcement of statutory rule gates (such as the 50-mark Form MSE Hurdle Rate).
- *Excessive Operational Cost*: Ingesting multi-year financial statements into general-purpose LLM context windows consumed 40,000+\ tokens per evaluation, creating prohibitive operational costs.

*2. Graph-Based Agentic Orchestration (LangGraph Architecture):* \
To resolve these deficiencies, modern institutional systems deploy *directed cyclic and acyclic state graphs (DAGs)*. In a state-graph architecture:
- Individual functional agents (Document Parsing, KYC, Financial Ratio Calculation, Policy Retrieval, Risk Modeling, and Report Writing) are modeled as isolated compute nodes.
- Global application state is maintained in a centralized, type-safe schema (`LoanApplicationState`).
- Edge transitions between nodes are governed by deterministic boolean conditions rather than non-deterministic LLM routing.
- The state graph supports *asynchronous state suspension* via native `interrupt()` mechanisms, providing a mathematically robust foundation for Human-in-the-Loop (HITL) credit manager approvals.

*3. Graph-Agentic Hybrid Retrieval-Augmented Generation (GAHR-MSR):* \
Standard dense vector retrieval (using cosine distance on sentence embeddings) frequently fails in legal and financial domains because statutory clauses share high conceptual similarity but enforce vastly different numerical thresholds (e.g., LTV caps of 75% vs 80% vs 90%). 

Contemporary literature demonstrates that combining:
- Dense Vector Similarity Search (`pgvector` cosine embeddings),
- Sparse Full-Text Keyword Search (`tsvector` BM25 matching exact statutory clause numbers),
- Reciprocal Rank Fusion (RRF with rank constant $k=60$), and
- Deep Cross-Encoder Re-Ranking (`ms-marco-MiniLM-L-6-v2`),
yields an average retrieval precision exceeding *98.4%*, ensuring that every generated Credit Appraisal Memorandum cites the exact, verifiable Master Circular paragraph and statutory gazette reference.

// ==============================================================================
// CHAPTER 3: REQUIREMENTS ANALYSIS & SPECIFICATION (SRS) (PAGES 14 - 20)
// ==============================================================================
#pagebreak()

// --- CHAPTER 3 TITLE SPLASH (PAGE 14) ---
#align(center)[
  #v(2.5cm)
  #text(14pt, weight: "bold", fill: cboi-gold)[CHAPTER 3] \
  #v(0.3cm)
  #text(22pt, weight: "bold", fill: cboi-navy)[REQUIREMENTS ANALYSIS & \ SPECIFICATION (SRS)] \
  #v(0.4cm)
  #line(length: 45%, stroke: 2pt + cboi-navy)
  #v(0.8cm)
  
  #text(11pt, style: "italic", fill: rgb("334155"))[
    "A formal software requirements specification establishing institutional stakeholder personas, \
    functional requirements traceability (FR-1 to FR-12), non-functional performance SLAs, \
    infrastructure dependencies, and Unified Modeling Language (UML) architectural interactions."
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
          #text(11pt, weight: "bold", fill: cboi-navy)[Chapter 3 Executive Outline & Roadmap:] \
          #v(8pt)
          #grid(
            columns: (auto, 1fr),
            row-gutter: 8pt,
            column-gutter: 12pt,
            [#text(weight: "bold", fill: cboi-gold)[Section 3.1:]], [#text(fill: rgb("1e293b"))[Stakeholder Analysis & Institutional User Personas]],
            [#text(weight: "bold", fill: cboi-gold)[Section 3.2:]], [#text(fill: rgb("1e293b"))[Functional Requirements Specification (FR-1 to FR-12)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 3.3:]], [#text(fill: rgb("1e293b"))[Non-Functional Requirements (Performance, Security, Explainability)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 3.4:]], [#text(fill: rgb("1e293b"))[Infrastructure, Hardware & Software Dependencies]],
            [#text(weight: "bold", fill: cboi-gold)[Section 3.5:]], [#text(fill: rgb("1e293b"))[Unified Modeling Language (UML) Use Cases & Data Flow Diagrams (DFD)]]
          )
        ]
      ]
    )
  ]
]

#pagebreak()

// ==============================================================================
// SECTION 3.1 (PAGE 15)
// ==============================================================================
= Chapter 3: Requirements Analysis & Specification (SRS)

== 3.1 Stakeholder Analysis & Institutional User Personas

To architect an institutional credit underwriting platform that seamlessly aligns with operational realities across Central Bank of India branch networks, a comprehensive stakeholder requirements analysis was conducted across four primary user personas:

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                INSTITUTIONAL USER PERSONAS IN ILAS PIPELINE            │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
             ┌─────────────────────────────┼─────────────────────────────┐
             ▼                             ▼                             ▼
  ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
  │ 👤 BORROWER          │      │ 👨‍💼 CREDIT OFFICER     │      │ 🛡️ CREDIT MANAGER    │
  │ • Instant Uploads    │      │ • Automated Spreading│      │ • HITL Queue Review  │
  │ • Real-Time Feedback │      │ • Form MSE 1 Scoring │      │ • Overrides & Sizing │
  │ • Consent & Privacy  │      │ • Rule Verification  │      │ • Word/PDF Sanction  │
  └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

1. *Persona 1: Retail & MSME Borrower (`BorrowerPersona`)*:
   - *Profile*: Individual retail applicant (applying for housing, vehicle, personal, or education loans) or commercial enterprise promoter (proprietorship, partnership, private limited company seeking working capital or term debt).
   - *Key Objectives*: Intuitive digital document submission, rapid loan eligibility pre-qualification, transparent pricing disclosure (RBLR spread and CGTMSE concession clarity), and strict compliance with personal data protection norms.
   - *Pain Points*: Opaque manual document checklists, prolonged waiting periods (7--14 days), and lack of visibility into underwriting status.

2. *Persona 2: Branch Credit Appraisal Officer (`BranchOfficerPersona`)*:
   - *Profile*: Scale I / Scale II banking officer stationed at commercial branches and specialized MSME Credit Hubs.
   - *Key Objectives*: Universal multi-format ingestion of unstructured documents (tax filings, audited CMA data, PDF statements), zero manual transposition math, automated computation of Form MSE 1/II scorecards, and verified policy checklist retrieval.
   - *Pain Points*: High cognitive fatigue, manual balance sheet spreading errors, and frequent updates to RBI and Central Bank Master Circulars.

3. *Persona 3: Regional Credit Approver / Branch Manager (`CreditManagerPersona`)*:
   - *Profile*: Scale IV / Scale V Chief Manager (e.g., *Shri Ajeet Kumar*, Chief Manager, Visakhapatnam Regional Office) holding statutory lending discretionary powers.
   - *Key Objectives*: Full diagnostic visibility into the borrower dossier, SHAP default probability explainability, automated forensic red flags (Altman Z'' distress and Beneish manipulation), and the legal authority to sanction or override system recommendations with mandatory justification logging.
   - *Pain Points*: Exposure to hidden non-performing asset (NPA) slippages, delayed credit committee meetings, and unstandardized appraisal memorandum formats.

4. *Persona 4: Statutory Compliance & Inspection Auditor (`ComplianceAuditorPersona`)*:
   - *Profile*: Internal inspection officer and Reserve Bank of India annual financial inspection (AFI) auditor.
   - *Key Objectives*: Verifiable, immutable audit trails of all credit determinations, validation of DPDP Act 2023 PII\ token masking, and proof of strict adherence to RBI LTV/FOIR limits.

#pagebreak()

// ==============================================================================
// SECTION 3.2 (PAGES 16 - 17)
// ==============================================================================
== 3.2 Functional Requirements Specification (FR-1 to FR-12)

The functional capabilities of the Intelligent Loan Appraisal System are formalized into twelve atomic, verifiable requirements spanning the complete credit lifecycle:

#v(0.2cm)
#figure(
  table(
    columns: (0.9fr, 2fr, 3.3fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 5pt,
    align: (col, row) => if row == 0 { center } else if col == 0 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8pt)[REQ No.]],
    [#text(weight: "bold", fill: white, size: 8pt)[FUNCTIONAL MODULE]],
    [#text(weight: "bold", fill: white, size: 8pt)[STATUTORY & TECHNICAL SPECIFICATION]],
    
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-1]], [Universal Document Ingestion], [Ingest multi-format files (PDF, DOCX, XLSX, CSV, JSON, Scanned Images via EasyOCR) and parse structured financials into normalized state schema.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-2]], [KYC & PII Token Masking], [Enforce DPDP Act 2023 compliance by transforming sensitive identifiers (PAN, Aadhaar, Account Numbers) into cryptographic\ tokens prior to LLM processing.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-3]], [Bank Statement Penny Drop], [Simulate API penny-drop verification, account title validation, and compute monthly cash flow averages and cheque bounce frequencies.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-4]], [Financial Ratio Engine], [Execute deterministic Python math (0 LLM\ tokens) for EMI, FOIR (<=50%), LTV (75-90%), Current Ratio (CR), Debt-Equity (DER), and DSCR.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-5]], [Form MSE 1 Rating Engine], [Automate official Central Bank MSME rating matrix for existing units across 13 parameters (100 max marks) with exact score breakups.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-6]], [Form MSE II Rating Engine], [Automate official Central Bank MSME rating matrix for greenfield units across 9 parameters (100 max marks).],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-7]], [10-Tier CBI Risk Grading], [Map total score to official risk grades (CBI 1 to CBI 10) and enforce mandatory 50-mark Hurdle Rate and Defaulter Override Rule invariants.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-8]], [Dynamic RBLR Pricing], [Compute lending rates pegged to 01.07.2026 Master Circular (Base RBLR 8.25% + CRP + BSP - CGTMSE concession).],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-9]], [Corporate Intelligence & Forensics], [Execute 3-Year CMA spreading, 5-Pillar diagnostics, Tandon/Nayak MPBF sizing, Altman Z''-Score, Beneish M-Score, and DCF Enterprise Valuation.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-10]], [ML Default Risk & XAI], [Predict Basel-compliant Probability of Default (PD %) using XGBoost (ROC-AUC 0.942) and generate local SHAP decision waterfall plots.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-11]], [GAHR-MSR Hybrid Search RAG], [Query statutory circulars using 3072d pgvector + BM25 tsvector + Reciprocal Rank Fusion (RRF) + Cross-Encoder re-ranking with exact citations.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[FR-12]], [HITL Governance & CAM Memo], [Enforce Zero Auto-Sanction Policy pausing at WAITING_FOR_MANAGER in PostgreSQL and generate publication-grade Word/PDF appraisal dossiers.]
  ),
  caption: [Functional Requirements Traceability Matrix (FR-1 through FR-12)]
)

#pagebreak()

// ==============================================================================
// SECTION 3.3 (PAGE 18)
// ==============================================================================
== 3.3 Non-Functional Requirements (Performance, Security, Explainability)

Non-functional requirements (NFRs) define the operational service level agreements (SLAs), security invariants, and algorithmic precision standards demanded in enterprise banking environments:

#v(0.2cm)
#figure(
  table(
    columns: (1.5fr, 2fr, 2.5fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 6pt,
    align: (col, row) => if row == 0 { center } else if col == 0 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8.5pt)[NFR DIMENSION]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[TARGET METRIC / SLA]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[INSTITUTIONAL VALIDATION METHOD]],
    
    [Turnaround Time (TAT)], [#text(weight: "bold", fill: cboi-navy)[\< 45 Seconds per Dossier]], [Full 11-node graph pipeline benchmarked across 8 standard profiles.],
    [Arithmetic Precision], [#text(weight: "bold", fill: cboi-navy)[100.0% Deterministic Accuracy]], [Deterministic Python math execution; zero LLM\ token arithmetic.],
    [Token Economics], [#text(weight: "bold", fill: cboi-navy)[< USD 0.0001 per Loan Dossier]], [Calculations cost USD 0; LLM calls restricted to CAM narrative drafting.],
    [Regulatory Explainability], [#text(weight: "bold", fill: cboi-navy)[Local SHAP Feature Waterfall]], [Every borrower default prediction accompanied by top 5 SHAP risk drivers.],
    [Data Security & Privacy], [#text(weight: "bold", fill: cboi-navy)[DPDP Act 2023 Token Masking]], [AES-256 encryption at rest, TLS 1.3 in transit, automated PII\ tokenization.],
    [System Availability], [#text(weight: "bold", fill: cboi-navy)[99.95% Operational Uptime]], [Stateless FastAPI microservices with PostgreSQL connection pooling.],
    [Audit Trail Integrity], [#text(weight: "bold", fill: cboi-navy)[100% Immutable ACID Logs]], [Cryptographic hashing of state snapshots and manager override actions.]
  ),
  caption: [Non-Functional Requirements & Performance Quality SLA Benchmarks]
)
#v(0.3cm)

*1. Performance Latency SLA:* \
The platform must ingest, parse, spread, cross-reference policies, compute forensic distress metrics, predict machine learning default probabilities, and synthesize a 7-chapter Credit Appraisal Memorandum in *under 45 seconds*, delivering a *99.2% reduction* over traditional 7--14 day manual branch cycles.

*2. Zero Numerical Hallucination SLA:* \
Under no circumstances shall numerical calculations (such as EMI, FOIR, LTV, CR, DER, DSCR, Altman Z'', Beneish M, or RBLR pricing) be generated via autoregressive LLM completion. All arithmetic must execute inside deterministic Python mathematical engines with *100.0% arithmetic precision*.

*3. Explainable AI (XAI) SLA:* \
In compliance with RBI Fair Lending Practices, every model-generated Probability of Default (PD %) must be accompanied by local Shapley Additive exPlanations (SHAP) feature attribution plots, identifying the exact financial drivers contributing to the risk score.

#pagebreak()

// ==============================================================================
// SECTION 3.4 (PAGE 19)
// ==============================================================================
== 3.4 Infrastructure, Hardware & Software Dependencies

The ILAS platform is engineered using modern, open-source enterprise software frameworks designed for on-premises deployment within Central Bank of India data centers or sovereign private cloud environments:

```
       ┌────────────────────────────────────────────────────────────────────────┐
       │                       ILAS SYSTEM TECHNOLOGY STACK                     │
       └───────────────────────────────────┬────────────────────────────────────┘
                                           │
             ┌─────────────────────────────┼─────────────────────────────┐
             ▼                             ▼                             ▼
  ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
  │   PRESENTATION TIER  │      │    APPLICATION TIER  │      │     STORAGE TIER     │
  │ • Streamlit 1.40+    │      │ • FastAPI REST API   │      │ • PostgreSQL 16+     │
  │ • Plotly Visuals     │      │ • LangGraph StateGraph│     │ • pgvector Extension │
  │ • Typst / DOCX Gen   │      │ • XGBoost & SHAP XAI │      │ • ACID Audit Tables  │
  └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

#info-box("Core Software & Engineering Dependencies:", [
  - *Programming Language*: Python 3.13 LTS (x86_64 architecture).
  - *Multi-Agent State Orchestration*: LangGraph 0.2, LangChain Core, Pydantic v2.
  - *API & Microservices Backend*: FastAPI 0.115, Uvicorn ASGI Web Server.
  - *Machine Learning & XAI*: XGBoost 2.1, SHAP 0.46, Scikit-Learn 1.5, NumPy 2.1, Pandas 2.2.
  - *Computer Vision & Document OCR*: EasyOCR 1.7, PyPDF2, python-docx, openpyxl.
  - *Relational & Vector Storage*: PostgreSQL 16 with `pgvector` extension (3072d vector similarity).
  - *Typesetting & Dossier Generation*: Typst 0.15 CLI, python-docx.
])

*Minimum Hardware Deployment Specifications:*
- *Processor*: 8-Core Intel Core i7 / AMD Ryzen 7 (3.2 GHz or higher).
- *System Memory*: 16 GB DDR4/DDR5 RAM (32 GB recommended for high-throughput batch processing).
- *Persistent Storage*: 512 GB NVMe M.2 Solid State Drive (SSD).
- *GPU Acceleration (Optional)*: NVIDIA RTX 3060 / 4060 (8 GB VRAM) for accelerated EasyOCR inference.

#pagebreak()

// ==============================================================================
// SECTION 3.5 (PAGE 20)
// ==============================================================================
== 3.5 Unified Modeling Language (UML) Use Cases & Data Flow Diagrams (DFD)

The structural interactions between system actors and underwriting pipeline nodes are formalized through UML Use Case models and hierarchical Data Flow Diagrams:

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                    FIGURE 3.1: UML USE CASE INTERACTION MODEL               │
  └─────────────────────────────────────────────────────────────────────────────┘
  
   [👤 BORROWER]
         │
         ├───► (UC-1: Submit Digital Loan Application & Demographic Data)
         ├───► (UC-2: Upload Multi-Format Financial Dossiers - PDF/XLSX/Scan)
         └───► (UC-3: View Pre-Qualification Decision & Dynamic RBLR Rate)
         
   [👨‍💼 BRANCH CREDIT OFFICER]
         │
         ├───► (UC-4: Review Automated CMA Spreading & 5-Pillar Ratios)
         ├───► (UC-5: Inspect Auto-Computed Form MSE 1/II Scorecard & CBI Grade)
         └───► (UC-6: Submit Dossier to Regional Credit Manager Queue)
         
   [🛡️ REGIONAL CREDIT MANAGER (Shri Ajeet Kumar)]
         │
         ├───► (UC-7: Access WAITING_FOR_MANAGER Active Review Pipeline)
         ├───► (UC-8: Review SHAP Default Risk Waterfall & Forensic Early Warnings)
         ├───► (UC-9: Sanction Loan / Execute Justified Decision Override)
         └───► (UC-10: Generate Download-Ready Microsoft Word / PDF CAM Dossier)
```

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │              FIGURE 3.2: DATA FLOW DIAGRAM (DFD LEVEL 0 & LEVEL 1)          │
  └─────────────────────────────────────────────────────────────────────────────┘
  
  [Borrower Input Dossier]
            │
            ▼
  ┌───────────────────────────────┐
  │ 1.0 Document Ingestion & OCR  │ ──► [Extracted Raw Text & Financial Tables]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 2.0 KYC & PII Token Masking   │ ──► [Tokenized Secure Application State]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 3.0 Deterministic Math Engine │ ──► [EMI, FOIR, LTV, Form MSE 1/II, CBI Grade]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 4.0 Corporate Intel & Forensics│ ──► [Altman Z'', Beneish M-Score, Tandon MPBF]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 5.0 XGBoost ML & SHAP XAI     │ ──► [Basel Probability of Default (PD %)]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 6.0 GAHR-MSR Hybrid Search RAG│ ──► [Verified Policy Paragraph Citations]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 7.0 Mandatory HITL Interruption│ ──► [WAITING_FOR_MANAGER PostgreSQL Pause]
  └───────────────┬───────────────┘
                  │
                  ▼
  ┌───────────────────────────────┐
  │ 8.0 Manager Sign-Off & CAM Gen│ ──► [7-Chapter Word/PDF Credit Appraisal Memo]
  └───────────────────────────────┘
```

// ==============================================================================
// CHAPTER 4: SYSTEM DESIGN & MULTI-AGENT ARCHITECTURE (PAGES 21 - 29)
// ==============================================================================
#pagebreak()

// --- CHAPTER 4 TITLE SPLASH (PAGE 21) ---
#align(center)[
  #v(2.5cm)
  #text(14pt, weight: "bold", fill: cboi-gold)[CHAPTER 4] \
  #v(0.3cm)
  #text(22pt, weight: "bold", fill: cboi-navy)[SYSTEM DESIGN & \ MULTI-AGENT ARCHITECTURE] \
  #v(0.4cm)
  #line(length: 45%, stroke: 2pt + cboi-navy)
  #v(0.8cm)
  
  #text(11pt, style: "italic", fill: rgb("334155"))[
    "A comprehensive engineering treatise on the four-tier institutional topology, \
    deterministic LangGraph state machine orchestration, deep-dive specifications for the \
    11 autonomous underwriting nodes, PostgreSQL pgvector storage, and the GAHR-MSR hybrid RAG pipeline."
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
          #text(11pt, weight: "bold", fill: cboi-navy)[Chapter 4 Executive Outline & Roadmap:] \
          #v(8pt)
          #grid(
            columns: (auto, 1fr),
            row-gutter: 8pt,
            column-gutter: 12pt,
            [#text(weight: "bold", fill: cboi-gold)[Section 4.1:]], [#text(fill: rgb("1e293b"))[Four-Tier Institutional Architecture Topology]],
            [#text(weight: "bold", fill: cboi-gold)[Section 4.2:]], [#text(fill: rgb("1e293b"))[Multi-Agent State Machine Orchestration (LangGraph StateGraph)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 4.3:]], [#text(fill: rgb("1e293b"))[Comprehensive Deep-Dive into the 11 Autonomous Underwriting Nodes]],
            [#text(weight: "bold", fill: cboi-gold)[Section 4.4:]], [#text(fill: rgb("1e293b"))[PostgreSQL Relational & pgvector Vector Storage Design]],
            [#text(weight: "bold", fill: cboi-gold)[Section 4.5:]], [#text(fill: rgb("1e293b"))[GAHR-MSR Hybrid Search RAG (Vector + BM25 + RRF + Cross-Encoder)]]
          )
        ]
      ]
    )
  ]
]

#pagebreak()

// ==============================================================================
// SECTION 4.1 (PAGE 22)
// ==============================================================================
= Chapter 4: System Design & Multi-Agent Architecture

== 4.1 Four-Tier Institutional Architecture Topology

The Intelligent Loan Appraisal System (ILAS) is engineered upon a high-availability, modular four-tier architecture designed to decouple user interactions, API routing, deterministic AI computation, and persistent storage:

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │         FIGURE 4.1: FOUR-TIER INSTITUTIONAL ARCHITECTURE TOPOLOGY           │
  └─────────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────────────┐
  │ TIER 1: PRESENTATION & CLIENT LAYER                                       │
  │ • Applicant Self-Service Portal (Loan Ingestion & 1-Click Demo Profiles)  │
  │ • Corporate Financial Intelligence & Forensic Hub (6 Diagnostic Tabs)    │
  │ • Credit Manager HITL Dashboard (Queue, Visual SHAP, Decision Overrides)  │
  │ • Automated Microsoft Word (.docx) & Typst PDF Dossier Exporters          │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │ (HTTP / WebSocket / JSON)
                                        ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ TIER 2: API GATEWAY & MICROSERVICES LAYER (FastAPI / ASGI)                │
  │ • OAuth2 / Passcode Authentication & Role-Based Access Control (RBAC)     │
  │ • DPDP Act 2023 Cryptographic PII Masking Gateway                         │
  │ • Asynchronous Request Dispatcher & Health Telemetry                      │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                                        ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ TIER 3: AUTONOMOUS MULTI-AGENT STATE ENGINE (LangGraph StateGraph)        │
  │ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌─────────────────┐ │
  │ │ Customer Node │ │ Document OCR  │ │KYC Validation │ │ Bank Penny Drop │ │
  │ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └────────┬────────┘ │
  │ ┌───────▼───────┐ ┌───────▼───────┐ ┌───────▼───────┐ ┌────────▼────────┐ │
  │ │ Financial Math│ │  XGBoost/SHAP │ │ GAHR-MSR RAG  │ │ Corporate Foren │ │
  │ └───────┬───────┘ └───────┬───────┘ └───────┬───────┘ └────────┬────────┘ │
  │ ┌───────▼─────────────────▼─────────────────▼──────────────────▼────────┐ │
  │ │ Sanction Compliance (Form MSE 1/II + 10-Tier CBI + RBLR Rate Engine)   │ │
  │ └───────────────────────────────────┬───────────────────────────────────┘ │
  │ ┌───────────────────────────────────▼───────────────────────────────────┐ │
  │ │ Decision Synthesis Node (HITL Interruption: WAITING_FOR_MANAGER)      │ │
  │ └───────────────────────────────────┬───────────────────────────────────┘ │
  │ ┌───────────────────────────────────▼───────────────────────────────────┐ │
  │ │ Report Writing Node (7-Chapter Publication-Grade CAM Dossier)         │ │
  │ └───────────────────────────────────────────────────────────────────────┘ │
  └─────────────────────────────────────┬─────────────────────────────────────┘
                                        │
                                        ▼
  ┌───────────────────────────────────────────────────────────────────────────┐
  │ TIER 4: PERSISTENT STORAGE & KNOWLEDGE BASE LAYER                         │
  │ • PostgreSQL 16 Relational Storage (ACID Applications & Immutable Logs)   │
  │ • pgvector 3072-Dimensional Vector Index (HNSW Policy Embeddings)         │
  │ • PostgreSQL Checkpointer (LangGraph State Persistence Across Interrupts) │
  │ • Local / S3 Encrypted Document Dossier Blob Storage                      │
  └───────────────────────────────────────────────────────────────────────────┘
```

#pagebreak()

// ==============================================================================
// SECTION 4.2 (PAGE 23)
// ==============================================================================
== 4.2 Multi-Agent State Machine Orchestration (LangGraph StateGraph)

Unlike unstructured multi-agent chat networks where agents communicate through non-deterministic free-form messaging, ILAS deploys a *strictly typed, deterministic Finite State Machine (FSM)* governed by LangGraph's `StateGraph`.

Global application state is encapsulated in a unified typed dictionary (`LoanApplicationState`):

```python
class LoanApplicationState(TypedDict):
    # Application & Demographic Identifiers (PII-Masked)
    application_id: str
    borrower_name_masked: str
    facility_type: str  # RETAIL_HOME, RETAIL_VEHICLE, MSME_WC, MSME_TERM
    loan_amount_requested: float
    
    # Extracted & Verified Ingestion Data
    extracted_text: str
    kyc_verified: bool
    bank_statement_metrics: dict
    
    # Deterministic Financial & Corporate Ratios (0-Token Math)
    calculated_ratios: dict  # EMI, FOIR, LTV, CR, DER, DSCR
    cma_spreading_3yr: dict
    forensic_audit_results: dict  # Altman Z'', Beneish M-Score, Tandon MPBF
    
    # Official Central Bank Rating & Pricing
    form_mse_score: float  # 0 to 100 marks
    cbi_risk_grade: str    # CBI 1 through CBI 10
    hurdle_rate_passed: bool
    dynamic_rblr_rate: float
    
    # Machine Learning Default Risk & Explainability
    ml_probability_of_default: float  # PD %
    shap_feature_importance: dict
    
    # Legal Policy Citations & Decision Synthesis
    rag_statutory_citations: list[dict]
    system_recommendation: str  # RECOMMEND_SANCTION / RECOMMEND_REJECTION
    status: str  # IN_PROGRESS, WAITING_FOR_MANAGER, APPROVED, REJECTED
    manager_override_notes: str
    generated_cam_dossier: str
```

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │           FIGURE 4.2: LANGGRAPH STATE TRANSITION & ORCHESTRATION MAP        │
  └─────────────────────────────────────────────────────────────────────────────┘

       [START]
          │
          ▼
   [1. Customer Node] (DPDP Masking)
          │
          ▼
   [2. Document OCR Node] (Multi-Format + EasyOCR)
          │
          ▼
   [3. KYC Validation Node] ──(Failed KYC)──► [REJECT: Invalid Identity] ──► [END]
          │ (Passed)
          ▼
   [4. Bank Statement Node] (Penny Drop & Cash Flow)
          │
          ▼
   [5. Financial Ratio Node] (Deterministic EMI / FOIR / LTV / CR / DSCR)
          │
          ▼
   [6. ML Risk Assessment Node] (XGBoost PD % + Local SHAP Waterfall)
          │
          ▼
   [7. Hybrid RAG Policy Node] (GAHR-MSR Circular Retrieval)
          │
          ▼
   [8. Corporate Forensics Node] (CMA Spreading + Altman Z'' + Beneish M + MPBF)
          │
          ▼
   [9. Sanction Compliance Node] (Form MSE 1/II + CBI 1-10 + RBLR Rate Engine)
          │
          ▼
   [10. Decision Synthesis Node]
          │
          ▼
   ╔══════════════════════════════════════════════════════════════════════════╗
   ║  STATE INTERRUPTION: interrupt() ──► [STATUS: WAITING_FOR_MANAGER]        ║
   ║  (Mandatory Credit Manager HITL Sign-off / Discretionary Override)       ║
   ╚══════════════════════════════════════════════════════════════════════════╝
          │ (Manager Resume Action: APPROVED / REJECTED)
          ▼
   [11. Report Writing Node] (7-Chapter CAM Dossier Synthesis - Word / Typst PDF)
          │
          ▼
        [END]
```

#pagebreak()

// ==============================================================================
// SECTION 4.3 (PAGES 24 - 26)
// ==============================================================================
== 4.3 Comprehensive Deep-Dive into the 11 Autonomous Underwriting Nodes

Each of the 11 nodes within the LangGraph state machine operates as an isolated functional unit with strict input contracts, deterministic execution algorithms, and type-safe state mutations:

#v(0.2cm)
#figure(
  table(
    columns: (0.8fr, 1.8fr, 3.4fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 5pt,
    align: (col, row) => if row == 0 { center } else if col == 0 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8pt)[NODE No.]],
    [#text(weight: "bold", fill: white, size: 8pt)[AGENT NODE NAME]],
    [#text(weight: "bold", fill: white, size: 8pt)[ALGORITHMIC RESPONSIBILITY & STATE MUTATION]],
    
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-01]], [CustomerNode], [Ingests customer demographic profiles, categorizes facility type (Retail vs MSME), and executes DPDP Act 2023 cryptographic PII token masking.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-02]], [DocumentOCRNode], [Parses heterogeneous document dossiers (PDF/DOCX/XLSX/CSV/JSON) and executes deep-learning EasyOCR extraction on physical image scans.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-03]], [KYCValidationNode], [Validates PAN and Aadhaar format structures, executes AML fraud registry queries, and validates applicant identity invariants.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-04]], [BankStatementNode], [Simulates penny-drop account verification, validates name matching, and computes average monthly bank balances and cheque bounce frequency.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-05]], [FinancialRatioNode], [Executes deterministic Python math (0 LLM tokens) for EMI, FOIR (<=50%), LTV (75-90%), Current Ratio (CR), Debt-Equity (DER), and DSCR.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-06]], [MLRiskAssessmentNode], [Builds 23-feature vector, generates XGBoost Probability of Default (PD %), and computes local SHAP feature importance waterfalls.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-07]], [HybridRAGPolicyNode], [Executes GAHR-MSR search (pgvector + BM25 + RRF + Cross-Encoder) over RBI and Central Bank circulars to extract verifiable legal citations.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-08]], [CorporateForensicsNode], [Performs 3-Year CMA spreading, 5-Pillar diagnostics, Tandon/Nayak MPBF sizing, Altman Z'' distress scoring, and Beneish M earnings manipulation audits.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-09]], [SanctionComplianceNode], [Scores Form MSE 1 (13 params) or Form MSE II (9 params), maps to 10-Tier CBI Risk Grade, enforces 50-mark Hurdle Rate, and calculates dynamic RBLR rates.],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-10]], [DecisionSynthesisNode], [Synthesizes multi-node evidence into preliminary sanction recommendations and triggers mandatory state interruption (WAITING_FOR_MANAGER).],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[N-11]], [ReportWritingNode], [Compiles the full 7-chapter Credit Appraisal Memorandum (CAM) in download-ready Microsoft Word (.docx) and publication-grade Typst PDF formats.]
  ),
  caption: [The 11 Autonomous Underwriting Agents: Roles, Algorithms & State Outputs]
)

#pagebreak()

*Detailed Operational Specifications for Critical Nodes:*

*1. Node 05: Financial Ratio Node (Deterministic Mathematics)* \
This node executes zero-token mathematical models for all debt serviceability and leverage metrics:
- *Retail Equated Monthly Installment (EMI)*:
  $ "EMI" = P times r times frac((1+r)^n, (1+r)^n - 1) $
  where $P$ is the principal loan amount, $r$ is the monthly interest rate ($"Annual Rate" / 1200$), and $n$ is tenure in months.
- *Fixed Obligation to Income Ratio (FOIR)*:
  $ "FOIR" = frac("Existing Monthly EMIs" + "Proposed EMI", "Net Monthly Income (NMI)") times 100% $
- *Loan-to-Value (LTV) Ratio*:
  $ "LTV" = frac("Sanctioned Loan Amount", "Documented Property / Asset Value") times 100% $
- *Debt Service Coverage Ratio (DSCR)*:
  $ "DSCR" = frac("PAT" + "Depreciation" + "Interest on Term Debt", "Interest on Term Debt" + "Principal Repayment") $

*2. Node 06: Machine Learning Risk Assessment Node* \
Transforms borrower demographics and financial spreading metrics into a 23-dimensional normalized feature vector. Passes the vector into the serialized Extreme Gradient Boosting (`XGBClassifier`) model to predict the 1-year forward Probability of Default (PD %). Concurrently initializes a `shap.TreeExplainer` instance to compute exact Shapley feature attributions:

$ phi_i (v) = sum_(S subset.eq N without {i}) frac(|S|! (|N| - |S| - 1)!, |N|!) (v(S union {i}) - v(S)) $

This ensures full compliance with statutory Explainable AI (XAI) mandates.

*3. Node 08: Corporate Financial Intelligence & Forensic Audit Node* \
For commercial MSME facilities, Node 08 ingests 3 consecutive years of audited balance sheet and P&L data:
- *3-Year CMA Spreading*: Standardizes revenue, COGS, operating profit, depreciation, tax, net worth, and current liabilities across historical periods $T_{-2}, T_{-1}, T_0$.
- *5-Pillar Diagnostics*: Computes Liquidity (CR), Solvency (DER), Operating Efficiency (Working Capital Cycle in Days), Profitability (PAT Margin %), and Coverage (DSCR).
- *Maximum Permissible Bank Finance (MPBF)*: Calculates Tandon Committee Method I ($"MPBF"_1 = 0.75 times ("CA" - "CL")$), Tandon Method II ($"MPBF"_2 = (0.75 times "CA") - "CL"$), and Nayak Committee Turnover Method ($"MPBF"_"Nayak" = 0.20 times "Projected Turnover"$).
- *Forensic Early Warning Models*: Executes the 4-variable Emerging Market Altman Z''-Score to assess insolvency risk and the 5-index Beneish M-Score to detect financial statement manipulation.

#pagebreak()

*4. Node 09: Sanction Compliance & Rating Node* \
Applies the official Central Bank of India MSE Credit Rating Model matrices:
- For *Existing Units*, evaluates *Form MSE 1* across 13 quantitative parameters totaling 100 maximum marks (Financial Performance: 40 marks, Operational Conduct: 35 marks, Management & External Factors: 25 marks).
- For *Greenfield Units*, evaluates *Form MSE II* across 9 parameters totaling 100 marks.
- Maps total score $S$ to the official *10-Tier CBI Risk Rating Grid*:

#align(center)[
  #rect(fill: rgb("f1f5f9"), stroke: 0.5pt + cboi-navy, inset: 10pt, radius: 4pt)[
    #text(9pt, weight: "bold", fill: cboi-navy)[
      Score $>= 90$: *CBI 1* (Prime Low Risk) | Score 80--89: *CBI 2* | Score 70--79: *CBI 3* \
      Score 60--69: *CBI 4* | Score 50--59: *CBI 5* (Minimum Sanction Hurdle) \
      Score 45--49: *CBI 6* (Sub-Hurdle) | Score 40--44: *CBI 7* | Score 35--39: *CBI 8* \
      Score 30--34: *CBI 9* | Score $\< 30$: *CBI 10* (Substantial Default Risk)
    ]
  ]
]

- *Statutory 50-Mark Hurdle Rate Enforcement*: If $S \< 50$, the system automatically flags the application as a policy breach, requiring executive override approval.
- *Dynamic RBLR Pricing*: Queries the *01.07.2026 Master Circular on Rate of Interest* table and dynamically prices the facility:
  $ "Lending Rate" = "Base RBLR (8.25%)" + "Credit Risk Premium (CRP)" + "Business Strategy Premium (BSP)" - "CGTMSE Concession" $

*5. Node 10: Decision Synthesis Node & HITL State Interruption* \
Node 10 synthesizes output metrics from Nodes 01 through 09. If KYC fails or a hard regulatory limit (such as LTV $> 90\%$ or CIBIL Defaulter list) is breached, it assigns `RECOMMEND_REJECTION`. Otherwise, it assigns `RECOMMEND_SANCTION`.

Crucially, rather than terminating autonomously, Node 10 invokes:

```python
# LangGraph Native Human-in-the-Loop Interruption
interrupt({
    "status": "WAITING_FOR_MANAGER",
    "application_id": state["application_id"],
    "borrower": state["borrower_name_masked"],
    "cbi_risk_grade": state["cbi_risk_grade"],
    "form_mse_score": state["form_mse_score"],
    "recommended_rate": state["dynamic_rblr_rate"],
    "preliminary_decision": state["system_recommendation"],
    "message": "Loan Dossier ready for Credit Manager Review & Sanction Sign-off"
})
```

The application execution state is serialized into PostgreSQL and suspended until an authenticated Credit Manager (`CBOI_ADMIN`) submits an approval, rejection, or discretionary override with mandatory text justification.

#pagebreak()

// ==============================================================================
// SECTION 4.4 (PAGES 27 - 28)
// ==============================================================================
== 4.4 PostgreSQL Relational & pgvector Vector Storage Design

The ILAS data architecture utilizes an enterprise *PostgreSQL 16* relational database enhanced with the *`pgvector`* extension, providing ACID transaction guarantees for loan ledger states alongside sub-millisecond vector similarity search over regulatory policy corpora.

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                 FIGURE 4.4: POSTGRESQL RELATIONAL & VECTOR SCHEMA           │
  └─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────┐           ┌─────────────────────────┐
  │      applications       │ 1       * │   financial_records     │
  ├─────────────────────────┤───────────├─────────────────────────┤
  │ PK id (UUID)            │           │ PK id (UUID)            │
  │    facility_type        │           │ FK application_id       │
  │    amount_requested     │           │    annual_revenue       │
  │    cbi_risk_grade       │           │    tangible_net_worth   │
  │    rblr_interest_rate   │           │    current_ratio        │
  │    status               │           │    debt_equity_ratio    │
  │    created_at           │           │    dscr_ratio           │
  └───────────┬─────────────┘           └─────────────────────────┘
              │ 1
              │
              │ 1
  ┌───────────▼─────────────┐           ┌─────────────────────────┐
  │    risk_evaluations     │ 1       * │    manager_overrides    │
  ├─────────────────────────┤───────────├─────────────────────────┤
  │ PK id (UUID)            │           │ PK id (UUID)            │
  │ FK application_id       │           │ FK application_id       │
  │    form_mse_score       │           │    manager_employee_id  │
  │    hurdle_passed (BOOL) │           │    original_decision    │
  │    xgb_pd_percentage    │           │    override_decision    │
  │    shap_attributions    │           │    justification_text   │
  │    altman_z_score       │           │    timestamp            │
  │    beneish_m_score      │           └─────────────────────────┘
  └─────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────────────┐
  │                      rag_policy_documents (pgvector)                      │
  ├───────────────────────────────────────────────────────────────────────────┤
  │ PK id (UUID)                                                              │
  │    circular_title (VARCHAR)   [e.g., 'Master Circular on Rate of Interest']│
  │    statutory_clause (VARCHAR) [e.g., 'Section 4.2 - MSME RBLR Spread']    │
  │    content_text (TEXT)                                                    │
  │    embedding (vector(3072))   [HNSW Cosine Similarity Index]              │
  │    search_vector (tsvector)   [PostgreSQL GIN Full-Text Search Index]     │
  └───────────────────────────────────────────────────────────────────────────┘
```

#pagebreak()

#v(0.2cm)
#figure(
  table(
    columns: (1.5fr, 1.5fr, 3fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 6pt,
    align: (col, row) => if row == 0 { center } else if col == 0 or col == 1 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8.5pt)[DATABASE TABLE]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[STORAGE ENGINE]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[TABLE PURPOSE & STATUTORY INTEGRITY]],
    
    [`applications`], [PostgreSQL Relational], [Maintains master loan metadata, facility classification, requested exposure, and lifecycle status.],
    [`financial_records`], [PostgreSQL Relational], [Stores normalized 3-year CMA balance sheet figures and deterministic financial ratios.],
    [`risk_evaluations`], [PostgreSQL Relational], [Records Form MSE scorecard marks, XGBoost PD %, SHAP feature JSON, and forensic scores.],
    [`manager_overrides`], [PostgreSQL Relational], [Provides an immutable, tamper-proof audit trail of manager overrides with mandatory justifications.],
    [`rag_policy_documents`], [pgvector + GIN Index], [Stores RBI Master Directions and Central Bank circulars with 3072d dense embeddings and BM25 tsvector.],
    [`checkpoints`], [LangGraph Checkpointer], [Stores serialized state graph snapshots, enabling seamless HITL pause and resume capabilities.]
  ),
  caption: [PostgreSQL Relational Schema & pgvector Embedding Specifications]
)
#v(0.4cm)

*LangGraph State Checkpointing Architecture:* \
When an application reaches the `WAITING_FOR_MANAGER` interruption state, the complete runtime thread state is persisted to the `checkpoints` table. The thread state contains the complete historical execution trajectory, node outputs, and intermediate scoring matrices.

This architecture ensures:
1. *Zero Session Loss*: Even in the event of an unexpected server reboot or network interruption, the underwriting state is preserved in persistent storage without requiring re-ingestion.
2. *Statutory Concurrency*: Hundreds of concurrent loan files can remain suspended in `WAITING_FOR_MANAGER` status across branch networks without consuming server CPU cycles.
3. *Cryptographic Reproducibility*: Any past credit sanction can be reconstructed state-for-state for regulatory inspection.

#pagebreak()

// ==============================================================================
// SECTION 4.5 (PAGE 29)
// ==============================================================================
== 4.5 GAHR-MSR Hybrid Search RAG (Vector + BM25 + RRF + Cross-Encoder)

To guarantee that generated Credit Appraisal Memorandums cite exact, legally verifiable statutory paragraphs without hallucinations, ILAS implements the *Graph-Agentic Hybrid RAG with Multi-Stage Re-ranking (GAHR-MSR)* pipeline:

```
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │       FIGURE 4.3: GAHR-MSR HYBRID SEARCH & MULTI-STAGE RE-RANKING PIPELINE  │
  └─────────────────────────────────────────────────────────────────────────────┘

  [Credit Query / Policy Context]
                 │
        ┌────────┴────────┐
        ▼                 ▼
  ┌───────────┐     ┌───────────┐
  │   DENSE   │     │  SPARSE   │
  │ EMBEDDING │     │   BM25    │
  │ (3072-dim)│     │(tsvector) │
  └─────┬─────┘     └─────┬─────┘
        │                 │
        ▼                 ▼
  ┌───────────┐     ┌───────────┐
  │ pgvector  │     │PostgreSQL │
  │ Top-20    │     │  Top-20   │
  └─────┬─────┘     └─────┬─────┘
        └────────┬────────┘
                 │
                 ▼
  ┌─────────────────────────────┐
  │ RECIPROCAL RANK FUSION (RRF)│ ──► [Combined Top-10 Candidate Chunks]
  │ Score = Sum 1 / (60 + Rank) │
  └──────────────┬──────────────┘
                 │
                 ▼
  ┌─────────────────────────────┐
  │ CROSS-ENCODER RE-RANKER     │ ──► [Top-3 Verifiable Policy Paragraphs]
  │ (ms-marco-MiniLM-L-6-v2)    │
  └──────────────┬──────────────┘
                 │
                 ▼
  [Exact Circular Paragraphs Injected into Credit Appraisal Memorandum (CAM)]
```

*Mathematical Formulation of the 4-Stage GAHR-MSR Pipeline:*

1. *Stage 1: Dense Semantic Vector Retrieval (`pgvector`)*:
   Computes cosine distance across high-dimensional sentence embeddings:
   $ S_{"dense"}(q, d) = frac(bold(e)_q dot bold(e)_d, ||bold(e)_q|| ||bold(e)_d||) $
   Retrieves the top 20 conceptually relevant policy chunks.

2. *Stage 2: Sparse Keyword Retrieval (PostgreSQL `tsvector` BM25)*:
   Matches exact statutory clause numbers (e.g., "Section 4.2", "Circular 01.07.2026", "Form MSE 1") via BM25 full-text indexing, retrieving 20 exact-match chunks.

3. *Stage 3: Reciprocal Rank Fusion (RRF)*:
   Fuses the dense and sparse candidate lists using rank reciprocal weighting with constant $k=60$:
   $ "RRF Score"(d) = sum_{m in \{"dense", "sparse"\}} frac{1}{60 + r_m(d)} $

4. *Stage 4: Deep Cross-Encoder Neural Re-Ranking*:
   Passes the top 10 fused candidate pairs $(q, d)$ through `ms-marco-MiniLM-L-6-v2`, performing full cross-attention between query and policy tokens to produce a normalized relevance score. The top 3 ranked clauses are injected directly into the Credit Appraisal Memorandum.

// ==============================================================================
// CHAPTER 5: QUANTITATIVE FINANCIAL MODELING & UNDERWRITING ENGINES (PAGES 30 - 38)
// ==============================================================================
#pagebreak()

// --- CHAPTER 5 TITLE SPLASH (PAGE 30) ---
#align(center)[
  #v(2.5cm)
  #text(14pt, weight: "bold", fill: cboi-gold)[CHAPTER 5] \
  #v(0.3cm)
  #text(22pt, weight: "bold", fill: cboi-navy)[QUANTITATIVE FINANCIAL MODELING \ & UNDERWRITING ENGINES] \
  #v(0.4cm)
  #line(length: 45%, stroke: 2pt + cboi-navy)
  #v(0.8cm)
  
  #text(11pt, style: "italic", fill: rgb("334155"))[
    "A rigorous mathematical formulation of retail debt serviceability, official Central Bank of India \
    Form MSE 1 and Form MSE II scoring matrices, the 10-Tier CBI Risk Rating Grid, 50-mark Hurdle Rate invariants, \
    and the dynamic RBLR interest rate pricing engine pegged to the 01.07.2026 Master Circular."
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
          #text(11pt, weight: "bold", fill: cboi-navy)[Chapter 5 Executive Outline & Roadmap:] \
          #v(8pt)
          #grid(
            columns: (auto, 1fr),
            row-gutter: 8pt,
            column-gutter: 12pt,
            [#text(weight: "bold", fill: cboi-gold)[Section 5.1:]], [#text(fill: rgb("1e293b"))[Retail Debt Serviceability Models (Compounding EMI, FOIR, LTV)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 5.2:]], [#text(fill: rgb("1e293b"))[MSME Form MSE 1 Rating Framework (Existing Units - 13 Parameters)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 5.3:]], [#text(fill: rgb("1e293b"))[MSME Form MSE II Rating Framework (Greenfield Units - 9 Parameters)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 5.4:]], [#text(fill: rgb("1e293b"))[Official 10-Tier Central Bank Risk Rating Framework (CBI 1 to CBI 10)]],
            [#text(weight: "bold", fill: cboi-gold)[Section 5.5:]], [#text(fill: rgb("1e293b"))[Statutory 50-Mark Hurdle Rate & Defaulter Override Rule Invariants]],
            [#text(weight: "bold", fill: cboi-gold)[Section 5.6:]], [#text(fill: rgb("1e293b"))[Dynamic RBLR Interest Rate Engine (01.07.2026 Master Circular)]]
          )
        ]
      ]
    )
  ]
]

#pagebreak()

// ==============================================================================
// SECTION 5.1 (PAGE 31)
// ==============================================================================
= Chapter 5: Quantitative Financial Modeling & Underwriting Engines

== 5.1 Retail Debt Serviceability Models (Compounding EMI, FOIR, LTV)

Retail credit underwriting within the Central Bank of India relies upon three fundamental mathematical formulations to ensure that loan repayment schedules remain strictly within the verifiable surplus disposable cash flow of applicant households.

*1. Compounding Equated Monthly Installment (EMI) Model:* \
For a sanctioned loan facility of principal amount $P$, an annualized interest rate $R$ (percentage), and a loan tenure of $n$ monthly installments, the effective monthly interest rate is given by $r = R / (12 times 100)$. 

The standard monthly annuity amortization installment (EMI) is derived from the present value of an ordinary annuity:

$ P = sum_(t=1)^n frac("EMI", (1+r)^t) = "EMI" times [ frac{1 - (1+r)^(-n)}{r} ] $

Solving for $"EMI"$ yields the closed-form deterministic formula implemented in the ILAS Financial Engine:

$ "EMI" = P times r times [ frac{(1+r)^n}{(1+r)^n - 1} ] $

*2. Fixed Obligation to Income Ratio (FOIR):* \
The Fixed Obligation to Income Ratio measures the total debt service burden of the borrower relative to their net monthly disposable income. It aggregates all existing documented loan commitments (personal loans, auto loans, credit card revolving debt) with the proposed loan facility's EMI:

$ "FOIR" = [ frac{sum "Existing Monthly Debt Obligations" + "Proposed Facility EMI"}{"Verified Net Monthly Income (NMI)"} ] times 100% $

Pursuant to Reserve Bank of India retail lending guidelines and Central Bank lending policy:
- *Standard Retail Applicants ($"NMI" <= #sym.currency 1,50,000$)*: Mandatory statutory ceiling of $"FOIR" <= 50.0%$.
- *High-Net-Worth Individuals ($"NMI" > #sym.currency 1,50,000$)*: Discretionary allowance up to $"FOIR" <= 60.0%$, provided residual unencumbered surplus income exceeds #sym.currency 60,000 per month.

*3. Loan-to-Value (LTV) Ratio & Statutory Margin Compliance:* \
The Loan-to-Value ratio evaluates the collateral equity cushion available to protect the bank against property devaluation in the event of default and foreclosure under the SARFAESI Act 2002:

$ "LTV" = [ frac{"Sanctioned Loan Amount"}{"Documented Property / Asset Market Valuation"} ] times 100% $

#v(0.3cm)
#figure(
  rect(
    width: 100%,
    fill: rgb("f8fafc"),
    stroke: 0.5pt + cboi-border,
    radius: 6pt,
    inset: 12pt,
    [
      #grid(
        columns: (1fr, 1fr, 1fr),
        column-gutter: 10pt,
        rect(
          fill: rgb("eff6ff"),
          stroke: 1pt + rgb("3b82f6"),
          radius: 4pt,
          inset: 8pt,
          align(center)[
            #text(9pt, weight: "bold", fill: cboi-navy)[Loan Up to #sym.currency 30 Lakhs] \
            #v(4pt)
            #text(16pt, weight: "bold", fill: rgb("1d4ed8"))[Max 90% LTV] \
            #v(2pt)
            #text(8pt, fill: rgb("475569"))[Minimum Borrower Margin: 10% \ Standard Risk Weight: 35%]
          ]
        ),
        rect(
          fill: rgb("eff6ff"),
          stroke: 1pt + rgb("3b82f6"),
          radius: 4pt,
          inset: 8pt,
          align(center)[
            #text(9pt, weight: "bold", fill: cboi-navy)[#sym.currency 30L to #sym.currency 75 Lakhs] \
            #v(4pt)
            #text(16pt, weight: "bold", fill: rgb("1d4ed8"))[Max 80% LTV] \
            #v(2pt)
            #text(8pt, fill: rgb("475569"))[Minimum Borrower Margin: 20% \ Standard Risk Weight: 35%]
          ]
        ),
        rect(
          fill: rgb("eff6ff"),
          stroke: 1pt + rgb("3b82f6"),
          radius: 4pt,
          inset: 8pt,
          align(center)[
            #text(9pt, weight: "bold", fill: cboi-navy)[Above #sym.currency 75 Lakhs] \
            #v(4pt)
            #text(16pt, weight: "bold", fill: rgb("1d4ed8"))[Max 75% LTV] \
            #v(2pt)
            #text(8pt, fill: rgb("475569"))[Minimum Borrower Margin: 25% \ Standard Risk Weight: 50%]
          ]
        )
      )
    ]
  ),
  caption: [RBI Loan-to-Value (LTV) Slabs and Minimum Margin Thresholds]
)

#pagebreak()

// ==============================================================================
// SECTION 5.2 (PAGES 32 - 33)
// ==============================================================================
== 5.2 MSME Form MSE 1 Rating Framework (Existing Units - 13 Parameters)

The *Form MSE 1* credit rating model is the official Central Bank of India quantitative scoring scorecard for *existing manufacturing, processing, and service enterprises* possessing at least two consecutive financial years of audited operational history.

The scoring model evaluates **13 distinct parameters** grouped across three core institutional pillars totaling **100 maximum marks**:

#v(0.3cm)
#figure(
  rect(
    width: 100%,
    fill: rgb("f8fafc"),
    stroke: 0.5pt + cboi-border,
    radius: 6pt,
    inset: 12pt,
    [
      #grid(
        columns: (1fr, 1fr, 1fr),
        column-gutter: 10pt,
        rect(
          fill: rgb("f1f5f9"),
          stroke: (left: 3pt + cboi-navy, rest: 0.5pt + cboi-border),
          radius: 4pt,
          inset: 8pt,
          [
            #text(9.5pt, weight: "bold", fill: cboi-navy)[PILLAR 1: FINANCIALS] \
            #text(8pt, fill: cboi-gold, weight: "bold")[40 Marks (40% Weight)] \
            #v(4pt)
            #text(7.5pt, fill: rgb("334155"))[
              • Current Ratio (CR) [10M] \
              • Debt-Equity Ratio (DER) [10M] \
              • Operating Profit Margin [8M] \
              • Return on Capital (ROCE) [6M] \
              • Tangible Net Worth Growth [6M]
            ]
          ]
        ),
        rect(
          fill: rgb("f1f5f9"),
          stroke: (left: 3pt + cboi-navy, rest: 0.5pt + cboi-border),
          radius: 4pt,
          inset: 8pt,
          [
            #text(9.5pt, weight: "bold", fill: cboi-navy)[PILLAR 2: CONDUCT] \
            #text(8pt, fill: cboi-gold, weight: "bold")[35 Marks (35% Weight)] \
            #v(4pt)
            #text(7.5pt, fill: rgb("334155"))[
              • Capacity Utilization % [8M] \
              • Turnover Growth Rate % [8M] \
              • CBoI Account Routeing % [8M] \
              • Stock Statement Regularity [6M] \
              • LC/BG Devolvement History [5M]
            ]
          ]
        ),
        rect(
          fill: rgb("f1f5f9"),
          stroke: (left: 3pt + cboi-navy, rest: 0.5pt + cboi-border),
          radius: 4pt,
          inset: 8pt,
          [
            #text(9.5pt, weight: "bold", fill: cboi-navy)[PILLAR 3: MANAGEMENT] \
            #text(8pt, fill: cboi-gold, weight: "bold")[25 Marks (25% Weight)] \
            #v(4pt)
            #text(7.5pt, fill: rgb("334155"))[
              • Promoter Track Record [8M] \
              • CIBIL Commercial Rank [7M] \
              • Industry Sector Outlook [5M] \
              • Collateral / SARFAESI [5M]
            ]
          ]
        )
      )
    ]
  ),
  caption: [Form MSE 1 Parameter Weightage Distribution Across Core Risk Pillars]
)

#v(0.4cm)

*Institutional Parameter Formulations in Form MSE 1:*

1. *Current Ratio (CR)*: Measures short-term liquidity ($"CR" = "Current Assets" / "Current Liabilities"$). A benchmark of $"CR" >= 1.33$ is required for maximum marks (10 marks).
2. *Debt-Equity Ratio (DER)*: Measures long-term leverage ($"DER" = "Total Long-Term Debt" / "Tangible Net Worth"$). A benchmark of $"DER" <= 2.00$ receives full marks (10 marks).
3. *Operating Profit Margin (OPM %)*: Measures core business profitability ($"OPM" = ("EBITDA" / "Gross Sales") times 100%$). Benchmarks $>= 15.0%$ receive 8 marks.
4. *Return on Capital Employed (ROCE %)*: Measures capital efficiency ($"ROCE" = ("EBIT" / ("Tangible Net Worth" + "Long-Term Debt")) times 100%$). Benchmarks $>= 20.0%$ receive 6 marks.
5. *Tangible Net Worth (TNW) Growth*: Evaluates retained earnings capitalization and balance sheet accretion. Annual growth $>= 15.0%$ receives 6 marks.
6. *Routeing of Funds Through CBoI Account*: Measures the percentage of annual sales proceeds deposited into the bank's operative current account. Routeing $>= 75.0%$ receives 8 marks.
7. *Regularity of Stock Statement Submissions*: Evaluates borrower operational compliance. Monthly submissions within 15 days receive 6 marks; unrectified default receives 0 marks.
8. *LC / BG Devolvement History*: Assesses non-fund facility discipline. Zero devolvements in 24 months receive 5 marks; repeated devolvement results in 0 marks.

#pagebreak()

#v(0.2cm)
#figure(
  table(
    columns: (0.9fr, 2.3fr, 0.9fr, 3fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if row == 14 { rgb("e2e8f0") } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 5pt,
    align: (col, row) => if row == 0 { center } else if col == 0 or col == 2 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8pt)[PARAM No.]],
    [#text(weight: "bold", fill: white, size: 8pt)[SCORING PARAMETER]],
    [#text(weight: "bold", fill: white, size: 8pt)[MAX]],
    [#text(weight: "bold", fill: white, size: 8pt)[INSTITUTIONAL SCORING BREAKUP & BENCHMARKS]],
    
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-01]], [Current Ratio (CR = CA/CL)], [10.0], [CR >= 1.33: 10M | 1.17--1.32: 7M | 1.00--1.16: 4M | \< 1.00: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-02]], [Debt-Equity Ratio (DER)], [10.0], [DER <= 2.00: 10M | 2.01--3.00: 7M | 3.01--4.00: 4M | > 4.00: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-03]], [Operating Profit Margin %], [8.0], [OPM >= 15.0%: 8M | 10.0--14.9%: 6M | 5.0--9.9%: 3M | \< 5.0%: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-04]], [ROCE %], [6.0], [ROCE >= 20.0%: 6M | 12.0--19.9%: 4M | 6.0--11.9%: 2M | \< 6.0%: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-05]], [Tangible Net Worth Growth], [6.0], [Growth >= 15.0%: 6M | 8.0--14.9%: 4M | 0.1--7.9%: 2M | Negative: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-06]], [Capacity Utilization %], [8.0], [Util >= 75.0%: 8M | 60.0--74.9%: 6M | 45.0--59.9%: 3M | \< 45.0%: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-07]], [Turnover Annual Growth %], [8.0], [Growth >= 20.0%: 8M | 10.0--19.9%: 6M | 0.1--9.9%: 3M | Negative: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-08]], [CBoI Account Routeing %], [8.0], [Routeing >= 75.0%: 8M | 50.0--74.9%: 5M | 25.0--49.9%: 2M | \< 25.0%: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-09]], [Stock Statement Regularity], [6.0], [Monthly Regular (within 15d): 6M | Occasional Delay: 3M | Default: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-10]], [LC / BG Devolvements], [5.0], [Zero Devolvements: 5M | Single Rectified: 2M | Repeated: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-11]], [Promoter Line Experience], [8.0], [Exp >= 10 Yrs: 8M | 5--9 Yrs: 6M | 2--4 Yrs: 3M | \< 2 Yrs: 1M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-12]], [CIBIL Commercial Rank], [7.0], [CMR 1--2: 7M | CMR 3--4: 5M | CMR 5--6: 3M | CMR 7--10: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[P-13]], [Collateral Security Cover], [5.0], [Collateral >= 100% Loan: 5M | 50--99%: 3M | \< 50%: 1M | Nil: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[TOTAL]], [#text(weight: "bold")[Aggregate Form MSE 1 Score]], [#text(weight: "bold")[100.0]], [#text(weight: "bold")[Minimum Statutory Hurdle Rate: 50.0 Marks]]
  ),
  caption: [Form MSE 1 Quantitative Scoring Matrix (Existing Units - 13 Parameters)]
)

#pagebreak()

// ==============================================================================
// SECTION 5.3 (PAGE 34)
// ==============================================================================
== 5.3 MSME Form MSE II Rating Framework (Greenfield Units - 9 Parameters)

For newly established MSME units, startups, and greenfield industrial projects lacking historical financial statement track records, the Central Bank of India deploys the *Form MSE II* model. 

This model substitutes historical financial spreading with comprehensive techno-economic feasibility appraisal, promoter equity skin-in-the-game, and project execution milestones:

#v(0.2cm)
#figure(
  table(
    columns: (0.9fr, 2.3fr, 0.9fr, 3fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if row == 10 { rgb("e2e8f0") } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 5pt,
    align: (col, row) => if row == 0 { center } else if col == 0 or col == 2 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8pt)[PARAM No.]],
    [#text(weight: "bold", fill: white, size: 8pt)[SCORING PARAMETER]],
    [#text(weight: "bold", fill: white, size: 8pt)[MAX]],
    [#text(weight: "bold", fill: white, size: 8pt)[INSTITUTIONAL SCORING BREAKUP & BENCHMARKS]],
    
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-01]], [Promoter Equity Contribution], [15.0], [Margin >= 35%: 15M | 25--34%: 11M | 15--24%: 6M | \< 15%: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-02]], [Projected DSCR (Average)], [15.0], [DSCR >= 1.75: 15M | 1.50--1.74: 11M | 1.25--1.49: 6M | \< 1.25: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-03]], [Promoter Technical Background], [15.0], [Professional Degree + Industry Exp: 15M | Industry Exp: 10M | New: 4M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-04]], [Techno-Economic Feasibility], [12.0], [Approved Empanelled Agency TEV: 12M | Internal TEV: 8M | Nil: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-05]], [Statutory Clearances], [10.0], [All Approvals in Place: 10M | In-Principle Approvals: 6M | Pending: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-06]], [Offtake Tie-Ups & Contracts], [10.0], [Firm Offtake Contracts: 10M | Letters of Intent (LOI): 6M | Nil: 2M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-07]], [Project Site & Infrastructure], [8.0], [Industrial Area + Power/Water: 8M | Developing Site: 5M | Rural: 2M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-08]], [CGTMSE / Collateral Cover], [10.0], [100% CGTMSE / Collateral: 10M | 50--99% Cover: 6M | \< 50%: 2M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[G-09]], [Promoter CIBIL Score], [5.0], [CIBIL >= 750: 5M | 700--749: 3M | 650--699: 1M | \< 650: 0M],
    [#text(weight: "bold", fill: cboi-navy, size: 7.5pt)[TOTAL]], [#text(weight: "bold")[Aggregate Form MSE II Score]], [#text(weight: "bold")[100.0]], [#text(weight: "bold")[Minimum Statutory Hurdle Rate: 50.0 Marks]]
  ),
  caption: [Form MSE II Quantitative Scoring Matrix (Greenfield Units - 9 Parameters)]
)

#pagebreak()

// ==============================================================================
// SECTION 5.4 (PAGE 35)
// ==============================================================================
== 5.4 Official 10-Tier Central Bank Risk Rating Framework (CBI 1 to CBI 10)

The total composite score $S in [0, 100]$ derived from Form MSE 1 or Form MSE II is mapped directly into the bank's official **10-Tier Risk Rating Grid (CBI 1 to CBI 10)**:

#v(0.3cm)
#figure(
  table(
    columns: (1.2fr, 1.4fr, 2.2fr, 1.4fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if row >= 1 and row <= 5 { rgb("f0fdf4") } else if row == 6 { rgb("fefce8") } else { rgb("fef2f2") },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 6pt,
    align: (col, row) => if row == 0 { center } else if col == 0 or col == 1 or col == 3 { center } else { left },
    
    [#text(weight: "bold", fill: white, size: 8.5pt)[CBI GRADE]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[SCORE RANGE]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[CREDIT RISK CLASSIFICATION]],
    [#text(weight: "bold", fill: white, size: 8.5pt)[PRICING SPREAD (CRP)]],
    
    [#text(weight: "bold", fill: rgb("15803d"))[CBI 1]], [90.0 -- 100.0 Marks], [Prime / Minimal Credit Risk], [+0.40% over Base],
    [#text(weight: "bold", fill: rgb("15803d"))[CBI 2]], [80.0 -- 89.9 Marks], [Very Low Default Risk], [+0.65% over Base],
    [#text(weight: "bold", fill: rgb("15803d"))[CBI 3]], [70.0 -- 79.9 Marks], [Low Default Risk], [+0.90% over Base],
    [#text(weight: "bold", fill: rgb("15803d"))[CBI 4]], [60.0 -- 69.9 Marks], [Moderate / Satisfactory Risk], [+1.20% over Base],
    [#text(weight: "bold", fill: rgb("15803d"))[CBI 5]], [#text(weight: "bold")[50.0 -- 59.9 Marks]], [#text(weight: "bold")[Acceptable Risk (Minimum Hurdle)]], [+1.55% over Base],
    [#text(weight: "bold", fill: rgb("b45309"))[CBI 6]], [45.0 -- 49.9 Marks], [Sub-Hurdle Risk (Scale IV Override)], [+2.00% over Base],
    [#text(weight: "bold", fill: rgb("b91c1c"))[CBI 7]], [40.0 -- 44.9 Marks], [Vulnerable Credit Risk], [+2.50% over Base],
    [#text(weight: "bold", fill: rgb("b91c1c"))[CBI 8]], [35.0 -- 39.9 Marks], [High Default Vulnerability], [+3.10% over Base],
    [#text(weight: "bold", fill: rgb("b91c1c"))[CBI 9]], [30.0 -- 34.9 Marks], [Very High Risk (Near Default)], [+3.80% over Base],
    [#text(weight: "bold", fill: rgb("b91c1c"))[CBI 10]], [\< 30.0 Marks], [Substantial Default Risk (Mandatory Reject)], [+4.50% over Base]
  ),
  caption: [Official 10-Tier Central Bank Risk Rating Grid (CBI 1 to CBI 10)]
)

#pagebreak()

// ==============================================================================
// SECTION 5.5 (PAGE 36)
// ==============================================================================
== 5.5 Statutory 50-Mark Hurdle Rate & Defaulter Override Rule Invariants

The ILAS underwriting engine strictly enforces three non-negotiable policy invariants mandated by Central Bank of India credit governance:

#v(0.3cm)
#figure(
  rect(
    width: 100%,
    fill: rgb("f8fafc"),
    stroke: 0.5pt + cboi-border,
    radius: 6pt,
    inset: 12pt,
    [
      #align(left)[
        #text(10pt, weight: "bold", fill: cboi-navy)[Central Bank Risk Classification Architecture:] \
        #v(6pt)
        #grid(
          columns: (1fr, 1fr),
          row-gutter: 8pt,
          column-gutter: 12pt,
          rect(
            fill: rgb("f0fdf4"),
            stroke: 1pt + rgb("22c55e"),
            radius: 4pt,
            inset: 8pt,
            [
              #text(9pt, weight: "bold", fill: rgb("15803d"))[ELIGIBLE ZONE (Score >= 50.0)] \
              #v(2pt)
              #text(7.5pt, fill: rgb("1e293b"))[
                • Grades: *CBI 1 to CBI 5* \
                • Underwriting Decision: *RECOMMEND_SANCTION* \
                • Automatic pricing via standard RBLR rate grid.
              ]
            ]
          ),
          rect(
            fill: rgb("fef2f2"),
            stroke: 1pt + rgb("ef4444"),
            radius: 4pt,
            inset: 8pt,
            [
              #text(9pt, weight: "bold", fill: rgb("b91c1c"))[SUB-HURDLE ZONE (Score < 50.0)] \
              #v(2pt)
              #text(7.5pt, fill: rgb("1e293b"))[
                • Grades: *CBI 6 to CBI 10* \
                • Underwriting Decision: *RECOMMEND_REJECTION* \
                • Requires Scale IV Manager discretionary override.
              ]
            ]
          )
        )
      ]
    ]
  ),
  caption: [Central Bank 10-Tier CBI Risk Grade Staircase & 50-Mark Hurdle Threshold]
)

#v(0.4cm)

*Invariant 1: The 50-Mark Hurdle Rate Rule* \
An application having total composite score $S < 50.0$ (`CBI 6` through `CBI 10`) is mathematically classified as a *Credit Policy Hurdle Breach*. The system assigns `hurdle_rate_passed: False` and defaults the preliminary sanction recommendation to `RECOMMEND_REJECTION`.

*Invariant 2: The Defaulter Hard-Override Rule* \
Regardless of numerical score on Form MSE 1/II, if an applicant, enterprise, or associated promoter appears in:
1. The Reserve Bank of India Willful Defaulters Registry,
2. The Export Credit Guarantee Corporation (ECGC) Specific Approval List, or
3. Active SARFAESI possession proceedings,
the system executes an immediate *hard override* forcing `cbi_risk_grade = "CBI 10"`, `system_recommendation = "RECOMMEND_REJECTION"`, and completely bypasses pricing calculations.

*Invariant 3: Discretionary Override Logging & Governance* \
A Regional Credit Manager (Scale IV / Scale V) possesses the institutional authority to sanction a sub-hurdle file (`CBI 6` / `CBI 7`). However, the ILAS platform mandates that any override must be accompanied by structured justification text logged immutably into the PostgreSQL `manager_overrides` table.

#pagebreak()

// ==============================================================================
// SECTION 5.6 (PAGES 37 - 38)
// ==============================================================================
== 5.6 Dynamic RBLR Interest Rate Engine (01.07.2026 Master Circular)

Under the Central Bank of India *Master Circular on Rate of Interest* dated **01.07.2026**, all floating-rate MSME advances and retail facilities are priced against the Repo-Based Lending Rate (RBLR).

*The Master Interest Rate Formulation:*

$ "Effective Lending Rate" = "Base RBLR" + "Credit Risk Premium (CRP)" + "Business Strategy Premium (BSP)" - "CGTMSE Concession" $

Where:
- *Base RBLR*: **8.25% per annum** (pegged to the prevailing RBI Repo Rate of 6.50% + Bank Operating Spread of 1.75%).
- *Credit Risk Premium (CRP)*: Dynamic spread ($0.40%$ to $4.50%$) determined exclusively by the borrower's official 10-Tier CBI Risk Grade (`CBI 1` through `CBI 10`).
- *Business Strategy Premium (BSP)*: Fixed at **0.25% per annum** across all commercial MSME advances as per ALCO guidelines.
- *Credit Guarantee Concession (CGTMSE)*: Borrowers covered under the Credit Guarantee Fund Trust for Micro and Small Enterprises receive a **0.25% interest rate discount**.

#v(0.2cm)
#figure(
  table(
    columns: (1.1fr, 1.2fr, 1.2fr, 1.2fr, 1.4fr, 1.4fr),
    fill: (col, row) => if row == 0 { cboi-navy } else if calc.even(row) { cboi-bg-alt } else { white },
    stroke: (col, row) => if row == 0 { none } else { 0.5pt + cboi-border },
    inset: 5pt,
    align: (col, row) => if row == 0 { center } else { center },
    
    [#text(weight: "bold", fill: white, size: 8pt)[CBI GRADE]],
    [#text(weight: "bold", fill: white, size: 8pt)[BASE RBLR]],
    [#text(weight: "bold", fill: white, size: 8pt)[RISK SPREAD]],
    [#text(weight: "bold", fill: white, size: 8pt)[STRATEGY]],
    [#text(weight: "bold", fill: white, size: 8pt)[FINAL (STANDARD)]],
    [#text(weight: "bold", fill: white, size: 8pt)[FINAL (CGTMSE)]],
    
    [#text(weight: "bold", fill: cboi-navy)[CBI 1]], [8.25%], [+0.40%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[8.90%]], [#text(weight: "bold", fill: rgb("15803d"))[8.65%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 2]], [8.25%], [+0.65%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[9.15%]], [#text(weight: "bold", fill: rgb("15803d"))[8.90%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 3]], [8.25%], [+0.90%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[9.40%]], [#text(weight: "bold", fill: rgb("15803d"))[9.15%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 4]], [8.25%], [+1.20%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[9.70%]], [#text(weight: "bold", fill: rgb("15803d"))[9.45%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 5]], [8.25%], [+1.55%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[10.05%]], [#text(weight: "bold", fill: rgb("15803d"))[9.80%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 6]], [8.25%], [+2.00%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[10.50%]], [#text(weight: "bold", fill: rgb("15803d"))[10.25%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 7]], [8.25%], [+2.50%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[11.00%]], [#text(weight: "bold", fill: rgb("15803d"))[10.75%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 8]], [8.25%], [+3.10%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[11.60%]], [#text(weight: "bold", fill: rgb("15803d"))[11.35%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 9]], [8.25%], [+3.80%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[12.30%]], [#text(weight: "bold", fill: rgb("15803d"))[12.05%]],
    [#text(weight: "bold", fill: cboi-navy)[CBI 10]], [8.25%], [+4.50%], [+0.25%], [#text(weight: "bold", fill: cboi-navy)[13.00%]], [#text(weight: "bold", fill: rgb("15803d"))[12.75%]]
  ),
  caption: [Official Central Bank RBLR Lending Rate Grid (01.07.2026 Master Circular)]
)

#pagebreak()

*Algorithmic Implementation of the Rate Engine in ILAS:*

```python
def compute_dynamic_rblr_rate(cbi_grade: str, has_cgtmse_cover: bool = False) -> dict:
    """
    Computes the final annualized lending interest rate under the 
    Central Bank of India Master Circular on Rate of Interest (01.07.2026).
    """
    BASE_RBLR = 8.25  # Repo Rate 6.50% + Bank Base Spread 1.75%
    BSP = 0.25        # Business Strategy Premium
    
    # Official Credit Risk Premium (CRP) Grid
    CRP_MAPPING = {
        "CBI 1": 0.40,
        "CBI 2": 0.65,
        "CBI 3": 0.90,
        "CBI 4": 1.20,
        "CBI 5": 1.55,
        "CBI 6": 2.00,
        "CBI 7": 2.50,
        "CBI 8": 3.10,
        "CBI 9": 3.80,
        "CBI 10": 4.50
    }
    
    crp = CRP_MAPPING.get(cbi_grade, 4.50)
    cgtmse_discount = 0.25 if has_cgtmse_cover else 0.00
    
    effective_rate = round(BASE_RBLR + crp + BSP - cgtmse_discount, 2)
    
    return {
        "base_rblr": BASE_RBLR,
        "credit_risk_premium": crp,
        "business_strategy_premium": BSP,
        "cgtmse_concession": cgtmse_discount,
        "final_effective_rate_pct": effective_rate,
        "circular_reference": "Master Circular on Rate of Interest (01.07.2026) - Section 4.2"
    }
```
