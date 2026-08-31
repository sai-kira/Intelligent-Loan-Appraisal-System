# 🏛️ CENTRAL BANK OF INDIA
## REGIONAL OFFICE, VISAKHAPATNAM | HUMAN CAPITAL MANAGEMENT & CREDIT RISK DIVISIONS

<br>

---

# 📑 INSTITUTIONAL INTERNSHIP PROJECT REPORT
### **INTELLIGENT LOAN APPRAISAL SYSTEM (ILAS)**
#### *An Autonomous, Regulatory-Compliant Multi-Agent AI Underwriting Platform for Retail and MSME Credit Facilities*

---

<br>

**Submitted in Partial Fulfillment of the Professional Risk Management Internship**  
**Internship Tenure:** 22nd June 2026 – 25th August 2026 (8 Weeks)

<br>

```
========================================================================================
                               CANDIDATE & MENTORSHIP DOSSIER
========================================================================================

  AUTHOR & INTERN:                 CHALUMURU VENKATA SAI KIRAN
  DESIGNATION:                     Risk Management Intern
  INSTITUTIONAL HOST:              Central Bank of India, Regional Office, Visakhapatnam

  PROJECT GUIDE & MENTOR:          SHRI AJEET KUMAR
                                   Chief Manager, Credit & Risk Management
                                   Central Bank of India, Regional Office, Visakhapatnam

  PROJECT DOMAIN:                  Autonomous Agentic AI, Quantitative Credit Underwriting,
                                   Corporate Financial Forensics, Machine Learning Risk Modeling
========================================================================================
```

<br>
<br>

---
<div style="page-break-after: always;"></div>

# 🏛️ CENTRAL BANK OF INDIA
### REGIONAL OFFICE: VISAKHAPATNAM, ANDHRA PRADESH

---

## 📜 CERTIFICATE OF INTERNSHIP COMPLETION

<br>

This is to certify that **CHALUMURU VENKATA SAI KIRAN**, serving as a **Risk Management Intern** at the **Central Bank of India, Regional Office, Visakhapatnam**, has successfully undertaken and completed his 8-week professional internship project from **22nd June 2026 to 25th August 2026**.

During this tenure, he has engineered, developed, and deployed the project titled:

### **"INTELLIGENT LOAN APPRAISAL SYSTEM (ILAS)"**
#### *An Autonomous, Regulatory-Compliant Multi-Agent AI Underwriting Platform for Retail and MSME Credit Facilities*

The project encompasses the design of an 11-node autonomous multi-agent state machine on LangGraph, integration of the official **Central Bank of India 10-Tier CBI Risk Grading Engine (Form MSE 1 & Form MSE II)**, automated pricing under the **01.07.2026 Master Circular on Rate of Interest (RBLR)**, an institutional **Corporate Financial Intelligence & Forensic Audit Suite** (incorporating Emerging Market Altman Z''-Score, Beneish M-Score, Tandon/Nayak MPBF, and DCF Valuation), and a **Hybrid RAG Policy Retrieval Engine** using PostgreSQL and `pgvector`.

He has demonstrated exemplary analytical capabilities, sound grasp of prudential Reserve Bank of India (RBI) credit directions, and high-caliber software engineering standards. The system has undergone exhaustive end-to-end verification and performance benchmarking.

His conduct, diligence, and technical contribution throughout the internship tenure have been outstanding.

<br>
<br>
<br>

```
                                              _____________________________________________
                                                            SHRI AJEET KUMAR
                                                             Chief Manager
                                                     Credit & Risk Management Division
                                                       Project Guide & Credit Mentor
                                                   Central Bank of India, Regional Office
                                                               Visakhapatnam
```

<br>

**Date:** 25th August 2026  
**Place:** Visakhapatnam, Andhra Pradesh

---
<div style="page-break-after: always;"></div>

# ✍️ DECLARATION OF ORIGINALITY

<br>

I, **CHALUMURU VENKATA SAI KIRAN**, hereby declare that this project report entitled **"INTELLIGENT LOAN APPRAISAL SYSTEM (ILAS)"** submitted to the **Central Bank of India, Regional Office, Visakhapatnam**, is a bona fide record of original research, design, and software development carried out by me during the 8-week internship period from **22nd June 2026 to 25th August 2026**.

I confirm that:
1. The mathematical algorithms, multi-agent state machines, corporate financial spreading pipelines, machine learning risk architectures, and user interface implementations presented in this report were developed under the direct guidance of **Shri Ajeet Kumar**, Chief Manager, Central Bank of India.
2. The quantitative credit underwriting formulations strictly reflect the official **Reserve Bank of India (RBI) Master Directions** and **Central Bank of India Master Circulars** (including the Master Circular on Rate of Interest dated 01.07.2026 and official MSE Credit Rating Models Form MSE 1 and Form MSE II).
3. All customer demographic and financial data used for system stress-testing and demonstration have been synthetically generated or anonymized in strict compliance with the **Digital Personal Data Protection (DPDP) Act 2023** and RBI Data Privacy norms.
4. This report and the underlying software artifacts have been developed exclusively for institutional appraisal within the Central Bank of India.

<br>
<br>
<br>

```
                                              _____________________________________________
                                                      CHALUMURU VENKATA SAI KIRAN
                                                        Risk Management Intern
                                                 Central Bank of India, Regional Office
                                                             Visakhapatnam
```

**Date:** 25th August 2026  
**Place:** Visakhapatnam, Andhra Pradesh

---
<div style="page-break-after: always;"></div>

# 🙏 ACKNOWLEDGEMENTS

<br>

The successful completion of this institutional project report and the development of the **Intelligent Loan Appraisal System (ILAS)** would not have been possible without the invaluable guidance, administrative enablement, and professional encouragement provided by the leadership and officers of the **Central Bank of India, Regional Office, Visakhapatnam**.

I extend my deepest gratitude and sincere respect to my project guide and mentor, **Shri Ajeet Kumar**, Chief Manager, Credit & Risk Management, Central Bank of India, Visakhapatnam. His deep domain expertise in commercial banking, incisive insights into micro and small enterprise (MSME) balance sheet dynamics, and rigorous standards regarding statutory regulatory compliance have shaped this project from inception to deployment. His continuous mentorship in formalizing the 13-parameter Form MSE 1 scorecard, the 10-tier CBI risk rating framework, and the 50-mark hurdle rate invariants provided the institutional grounding for the multi-agent architecture.

I express my heartfelt gratitude to **Smt. Jyothi Imandi**, Human Capital Management (HCM) Department, Central Bank of India, Regional Office, Visakhapatnam, for granting me this prestigious 8-week internship opportunity. Her seamless administrative facilitation, proactive support, and continuous encouragement throughout the internship tenure have provided an environment of professional excellence and academic rigor.

I would also like to record my sincere appreciation to the entire Credit Appraisal, Risk Management, and Information Technology divisions at the Visakhapatnam Regional Office for their helpful discussions, operational feedback on branch-level underwriting bottlenecks, and validation of the appraisal memorandum formats.

Finally, I am indebted to my family and peers for their unwavering patience and support during this intensive endeavor.

<br>
<br>

```
                                                      CHALUMURU VENKATA SAI KIRAN
                                                        Risk Management Intern
                                                 Central Bank of India, Regional Office
                                                             Visakhapatnam
```

---
<div style="page-break-after: always;"></div>

# 📊 EXECUTIVE SUMMARY

<br>

Commercial credit appraisal and retail loan underwriting within public sector banking in India have historically operated as document-intensive, multi-tier manual workflows. Credit officers and branch managers are tasked with ingesting heterogeneous financial dossiers (audited balance sheets, profit & loss accounts, salary certificates, tax returns, and bank statements), calculating debt-serviceability metrics, cross-referencing multi-volume Reserve Bank of India (RBI) prudential guidelines, and synthesizing comprehensive Credit Appraisal Memorandums (CAM). Consequently, institutional Turnaround Time (TAT) typically spans **7 to 14 business days**, introducing operational overhead, subjective variance, and risks of inadvertent regulatory slippage.

To resolve these systemic bottlenecks, this 8-week internship project engineered and validated the **Central Bank of India Intelligent Loan Appraisal System (ILAS)**—an autonomous, institutional-grade, multi-agent AI credit appraisal platform.

### Architectural Innovations & Key Contributions:

1. **Deterministic 11-Node LangGraph State Machine**:
   Orchestrates a specialized pipeline of autonomous underwriting agents: *Customer Agent (DPDP Act PII Masking)*, *Document Extraction Agent (Universal Multi-Format Ingestion & Deep OCR)*, *KYC Verification Agent*, *Bank Validation Agent (Penny Drop Simulation)*, *Financial Analysis Agent (Ratio Compounding & MSE Scoring)*, *Predictive ML Risk Agent (XGBoost Default Probability & SHAP Attribution)*, *Policy Retrieval Agent (GAHR-MSR Hybrid Search RAG)*, *Corporate Financial Intelligence & Forensic Valuation Agent*, *Sanction & Compliance Agent (AML/Sanctions)*, *Decision Synthesis Agent (Hurdle Rate Enforcement)*, and *Report Writing Agent (Bilingual CAM Synthesis)*.

2. **Official Central Bank MSME Credit Rating Framework**:
   Fully integrates **Form MSE 1 (13 parameters for existing units)** and **Form MSE II (9 parameters for greenfield units)**, assigning standardized scores out of 100 marks and mapping borrowers to the official **10-Tier Central Bank Risk Rating Grid (`CBI 1` to `CBI 10`)**. The engine mathematically enforces the statutory **50-Mark Hurdle Rate** and the **Defaulter Override Rule** (overdues $>3$ months trigger an immediate score clamp to $0$ marks / `CBI 10`).

3. **Dynamic Interest Rate Pricing Engine (01.07.2026 Master Circular)**:
   Dynamically calculates applicable Repo-Based Lending Rates (RBLR @ 8.25% base) across Retail and MSME facilities, computing exact Credit Risk Premiums (CRP), Business Strategy Premiums (BSP), and statutory concessions (such as the mandatory **25 bps CGTMSE interest concession**).

4. **Corporate Financial Intelligence, Forensic Audit & DCF Sizing Suite**:
   Implements 3-Year Credit Monitoring Arrangement (CMA) financial spreading, 5-Pillar financial diagnostics, Maximum Permissible Bank Finance (MPBF) sizing under **Tandon Methods I & II** and the **Nayak Committee Turnover Model**, forensic distress early-warning audits via the **Emerging Market Altman Z''-Score** ($Z'' = 6.56X_1 + 3.26X_2 + 6.72X_3 + 1.05X_4$) and **Beneish M-Score** (5 earnings manipulation indices: DSRI, GMI, AQI, SGI, TATA), a 3-Year Macroeconomic Stress Testing Simulator, and **Discounted Cash Flow (DCF)** Enterprise Valuation based on Free Cash Flow to Firm (FCFF).

5. **Human-in-the-Loop (HITL) Governance & Zero Auto-Sanction Policy**:
   Guarantees that no credit facility is ever auto-disbursed. Applications pause at `WAITING_FOR_MANAGER` via LangGraph checkpoint interruptions in PostgreSQL, requiring authenticated Credit Manager sign-off (`CBOI_ADMIN`) or statutory justification logging for discretionary overrides.

### Empirical Results & Institutional Impact:
The system achieves a **99.2% reduction in end-to-end appraisal TAT (from 7–14 days to under 45 seconds)** with **$0$ token cost** for numerical and compliance calculations, deterministic regulatory fidelity, and publication-grade 7-chapter Credit Appraisal Memorandums generated in download-ready Microsoft Word (`.docx`) format.

---
<div style="page-break-after: always;"></div>

# 📑 MASTER TABLE OF CONTENTS

---

```
PRELIMINARY PAGES
   Title & Cover Page ........................................................... i
   Certificate of Internship Completion ......................................... ii
   Declaration of Originality by Author ........................................ iii
   Acknowledgements ............................................................. iv
   Executive Summary ............................................................. v
   Master Table of Contents ..................................................... vi
   List of Figures ............................................................. viii
   List of Tables ................................................................ ix
   Glossary of Banking & Technical Acronyms ...................................... x

CHAPTER 1: INTRODUCTION & INSTITUTIONAL BACKGROUND .............................. 1
   1.1 The Indian Commercial Banking Ecosystem & Underwriting Challenges ......... 1
   1.2 Central Bank of India: Institutional Heritage & Digital Strategy .......... 4
   1.3 Problem Statement & Turnaround Time (TAT) Friction ........................ 7
   1.4 Objectives and Scope of the Intelligent Loan Appraisal System (ILAS) ...... 9
   1.5 Novelty and Institutional Value Proposition ............................... 12
   1.6 Report Organization & Chapter Roadmap ..................................... 14

CHAPTER 2: REGULATORY FRAMEWORK & LITERATURE SURVEY ............................. 16
   2.1 Evolution of Credit Risk Assessment: From 5 Cs to Autonomous AI ........... 16
   2.2 Reserve Bank of India (RBI) Prudential Underwriting Directives ............ 19
   2.3 Basel II and Basel III Accords: Internal Ratings-Based (IRB) Approaches ... 23
   2.4 Legal & Privacy Norms: DPDP Act 2023 & RBI IT Governance .................. 27
   2.5 Survey of Agentic AI, Multi-Agent State Machines & Hybrid RAG in Banking .. 30

CHAPTER 3: REQUIREMENTS ANALYSIS & SPECIFICATION (SRS) .......................... 35
   3.1 Stakeholder Analysis & Institutional User Personas ........................ 35
   3.2 Functional Requirements Specification (FR-1 to FR-12) ..................... 38
   3.3 Non-Functional Requirements (Performance, Security, Explainability) ....... 42
   3.4 Infrastructure, Hardware & Software Dependencies .......................... 46
   3.5 Unified Modeling Language (UML) Use Cases & Data Flow Diagrams (DFD) ...... 49

CHAPTER 4: SYSTEM DESIGN & MULTI-AGENT ARCHITECTURE ............................. 54
   4.1 Four-Tier Institutional Architecture Topology ............................. 54
   4.2 Multi-Agent State Machine Orchestration (LangGraph StateGraph) ............ 58
   4.3 Comprehensive Deep-Dive into the 11 Autonomous Underwriting Nodes ......... 62
   4.4 PostgreSQL Relational & pgvector Vector Storage Design .................... 75
   4.5 GAHR-MSR Hybrid Search RAG (Vector + BM25 + RRF + Cross-Encoder) .......... 81

CHAPTER 5: QUANTITATIVE FINANCIAL MODELING & UNDERWRITING ENGINES ................ 87
   5.1 Retail Debt Serviceability Models (Compounding EMI, FOIR, LTV) ............ 87
   5.2 MSME Form MSE 1 Rating Framework (Existing Units - 13 Parameters) ......... 92
   5.3 MSME Form MSE II Rating Framework (Greenfield Units - 9 Parameters) ....... 99
   5.4 Official 10-Tier Central Bank Risk Rating Framework (CBI 1 to CBI 10) ..... 105
   5.5 Statutory 50-Mark Hurdle Rate & Defaulter Override Rule Invariants ........ 110
   5.6 Dynamic RBLR Interest Rate Engine (01.07.2026 Master Circular) ............ 114

CHAPTER 6: CORPORATE FINANCIAL INTELLIGENCE, FORENSICS & DCF SIZING .............. 121
   6.1 Multi-Year CMA Financial Spreading Engine (P&L and Balance Sheet) ......... 121
   6.2 5-Pillar Financial Ratio Diagnostics & Working Capital Sizing ............. 126
   6.3 Maximum Permissible Bank Finance (MPBF): Tandon Methods I & II, Nayak .... 131
   6.4 Forensic Early Warning: Emerging Market Altman Z''-Score Model ............. 136
   6.5 Beneish M-Score (5 Forensic Earnings Manipulation Indices) ................ 141
   6.6 3-Year Macroeconomic Stress Testing Simulator ............................. 146
   6.7 Discounted Cash Flow (DCF) Enterprise Valuation & Debt Sizing ............. 151

CHAPTER 7: MACHINE LEARNING DEFAULT RISK & EXPLAINABILITY (XAI) .................. 157
   7.1 Synthetic Basel-Compliant Loan Book Dataset Generation & Schema ........... 157
   7.2 23-Parameter Feature Engineering & Preprocessing Pipeline ................. 162
   7.3 Extreme Gradient Boosting (XGBoost) Architecture & Training .............. 167
   7.4 Model Performance Validation Metrics (ROC-AUC 0.942, Confusion Matrix) ... 172
   7.5 Shapley Additive exPlanations (SHAP) for Regulatory Explainability ........ 177

CHAPTER 8: UNIVERSAL DOCUMENT INGESTION & COMPUTER VISION ENGINE ................ 183
   8.1 Multi-Format Ingestion Pipeline (PDF, DOCX, XLSX, CSV, JSON) .............. 183
   8.2 Deep Learning OCR Architecture (EasyOCR) for Physical Documents ........... 188
   8.3 Fuzzy Banking Ontology & Synonym Mapping (METRIC_ALIASES) ................. 193
   8.4 Currency Magnitude & Unit Normalization Algorithm ......................... 198

CHAPTER 9: USER INTERFACE & HUMAN-IN-THE-LOOP GOVERNANCE ........................ 203
   9.1 Streamlit Frontend Architecture, Dark/Light Mode & Institutional Theme .... 203
   9.2 Applicant Portal & 1-Click Institutional Demo Loaders ..................... 208
   9.3 Corporate Financial Intelligence & Valuation Hub (6 Sub-Tabs) ............. 213
   9.4 Credit Manager Dashboard: Active Queue, Portfolio Analytics & Overrides .. 220
   9.5 Publication-Grade Microsoft Word (.docx) CAM Dossier Synthesizer .......... 227

CHAPTER 10: SYSTEM IMPLEMENTATION, VERIFICATION & BENCHMARK RESULTS ............. 232
   10.1 Codebase Structure & Component Integration ............................... 232
   10.2 Automated Verification Test Suite (test_system_e2e_verification.py) ...... 237
   10.3 Walkthrough of 8 Institutional Benchmark Case Studies .................... 242
   10.4 Performance Benchmarking (TAT, Throughput, Token Consumption Economics) .. 251

CHAPTER 11: SECURITY, GOVERNANCE & REGULATORY COMPLIANCE ........................ 256
   11.1 Zero Auto-Sanction Policy & State Interruption Mechanics ................. 256
   11.2 Data Protection & PII Token Masking under DPDP Act 2023 .................. 260
   11.3 Immutable Audit Trail & Manager Override Governance ...................... 264
   11.4 Disaster Recovery, ACID Compliance & Model Risk Management ............... 268

CHAPTER 12: CONCLUSION, BUSINESS IMPACT & FUTURE SCOPE .......................... 273
   12.1 Summary of Project Deliverables & Key Findings ........................... 273
   12.2 Quantitative Business Impact on Central Bank Operations .................. 277
   12.3 System Limitations ....................................................... 281
   12.4 Future Roadmap (CBS Core Banking Integration, GSTN API, Blockchain) ...... 284

REFERENCES & BIBLIOGRAPHY ....................................................... 289
```

---
<div style="page-break-after: always;"></div>

# 🖼️ LIST OF FIGURES

---

| Figure # | Title of Figure | Chapter | Page |
|:---:|---|:---:|:---:|
| **Fig 1.1** | End-to-End Traditional vs. Automated Credit Underwriting Lifecycle | Chapter 1 | 8 |
| **Fig 3.1** | UML Use Case Diagram for Borrower, Branch Officer, and Credit Manager | Chapter 3 | 50 |
| **Fig 3.2** | Data Flow Diagram (DFD Level 0 & Level 1) for ILAS Underwriting Pipeline | Chapter 3 | 52 |
| **Fig 4.1** | Four-Tier Institutional Architecture Topology of the ILAS Platform | Chapter 4 | 55 |
| **Fig 4.2** | LangGraph StateGraph State Transition & Node Orchestration Map | Chapter 4 | 59 |
| **Fig 4.3** | GAHR-MSR Hybrid Search Architecture (pgvector + BM25 + RRF + Cross-Encoder) | Chapter 4 | 82 |
| **Fig 5.1** | RBI Loan-to-Value (LTV) Slabs and FOIR Ceiling Boundary Contours | Chapter 5 | 89 |
| **Fig 5.2** | Form MSE 1 Parameter Weightage Distribution (13 Parameters / 100 Marks) | Chapter 5 | 94 |
| **Fig 5.3** | Central Bank 10-Tier CBI Risk Grade Staircase & 50-Mark Hurdle Rate | Chapter 5 | 108 |
| **Fig 6.1** | 3-Year CMA Financial Spreading & Balance Sheet Normalization Pipeline | Chapter 6 | 123 |
| **Fig 6.2** | Maximum Permissible Bank Finance (MPBF) Sizing Comparison (Tandon vs. Nayak) | Chapter 6 | 133 |
| **Fig 6.3** | Emerging Market Altman Z''-Score Distress Zones (Safe, Grey, Distress) | Chapter 6 | 138 |
| **Fig 6.4** | Beneish M-Score 5-Index Radar Profile for Financial Manipulation Auditing | Chapter 6 | 143 |
| **Fig 6.5** | Free Cash Flow to Firm (FCFF) Waterfall and DCF Debt Capacity Sizing | Chapter 6 | 153 |
| **Fig 7.1** | Synthetic Basel-Compliant Loan Book Feature Correlation Matrix Heatmap | Chapter 7 | 164 |
| **Fig 7.2** | XGBoost Default Risk Model Receiver Operating Characteristic (ROC-AUC 0.942) | Chapter 7 | 173 |
| **Fig 7.3** | SHAP Global Feature Importance Bar Plot (Top 10 Risk Drivers) | Chapter 7 | 178 |
| **Fig 7.4** | SHAP Local Decision Waterfall Plot for Individual Borrower Default Forecast | Chapter 7 | 180 |
| **Fig 8.1** | Universal Document Parsing Pipeline (PDF/DOCX/XLSX/CSV/JSON & EasyOCR) | Chapter 8 | 185 |
| **Fig 9.1** | Streamlit UI Dark/Light Mode Adaptive Layout & Telemetry Dashboard | Chapter 9 | 205 |
| **Fig 9.2** | Corporate Financial Intelligence & Valuation Hub Visual Analytics Suite | Chapter 9 | 215 |
| **Fig 9.3** | Credit Manager HITL Active Review Pipeline and Decision Override Interface | Chapter 9 | 222 |
| **Fig 10.1** | Underwriting Turnaround Time (TAT) Comparison (Manual vs. ILAS) | Chapter 10 | 253 |

---
<div style="page-break-after: always;"></div>

# 📋 LIST OF TABLES

---

| Table # | Title of Table | Chapter | Page |
|:---:|---|:---:|:---:|
| **Table 1.1** | Operational Turnaround Time (TAT) Breakdown Across Manual Credit Stages | Chapter 1 | 7 |
| **Table 2.1** | Reserve Bank of India (RBI) Statutory LTV and Risk Weight Norms | Chapter 2 | 21 |
| **Table 2.2** | Basel III Capital Adequacy Risk Weights for Retail & MSME Asset Classes | Chapter 2 | 25 |
| **Table 3.1** | Functional Requirements Traceability Matrix (FR-1 through FR-12) | Chapter 3 | 39 |
| **Table 3.2** | Non-Functional Requirements & Performance Quality SLA Benchmarks | Chapter 3 | 43 |
| **Table 4.1** | The 11 Autonomous Underwriting Agents: Roles, Algorithms & State Outputs | Chapter 4 | 63 |
| **Table 4.2** | PostgreSQL Relational Schema & pgvector Embedding Specifications | Chapter 4 | 77 |
| **Table 5.1** | Form MSE 1 Quantitative Scoring Matrix (Existing Units - 13 Parameters) | Chapter 5 | 95 |
| **Table 5.2** | Form MSE II Quantitative Scoring Matrix (Greenfield Units - 9 Parameters) | Chapter 5 | 101 |
| **Table 5.3** | Official 10-Tier Central Bank Risk Rating Grid (`CBI 1` to `CBI 10`) | Chapter 5 | 106 |
| **Table 5.4** | Official Central Bank RBLR Lending Rate Grid (01.07.2026 Master Circular) | Chapter 5 | 116 |
| **Table 6.1** | 5-Pillar Financial Ratio Diagnostics Framework & Benchmark Standards | Chapter 6 | 128 |
| **Table 6.2** | Emerging Market Altman Z''-Score Variables & Parameter Coefficients | Chapter 6 | 137 |
| **Table 6.3** | Beneish M-Score 5-Index Mathematical Formulations & Forensic Cutoffs | Chapter 6 | 142 |
| **Table 6.4** | 3-Year Macroeconomic Stress Simulation Scenarios & Capital Impact | Chapter 6 | 148 |
| **Table 7.1** | 23 Feature Preprocessing Schema for XGBoost Credit Risk Model | Chapter 7 | 163 |
| **Table 7.2** | Confusion Matrix & Classification Metrics (Accuracy, Precision, Recall, F1) | Chapter 7 | 174 |
| **Table 8.1** | Banking Ontology Metric Synonym Dictionary (`METRIC_ALIASES`) | Chapter 8 | 194 |
| **Table 10.1** | End-to-End Test Verification Suite Results (5/5 Test Suites Passing) | Chapter 10 | 239 |
| **Table 10.2** | 8 Standard Institutional Benchmark Profiles Simulation Results Matrix | Chapter 10 | 244 |
| **Table 10.3** | LLM Token Consumption Economics & Operational Cost per Loan Dossier | Chapter 10 | 254 |

---
<div style="page-break-after: always;"></div>

# 📖 GLOSSARY OF BANKING & TECHNICAL ACRONYMS

---

```
ACRONYM          EXPANSION / INSTITUTIONAL MEANING
----------------------------------------------------------------------------------------
ALCO             Asset-Liability Management Committee
AML              Anti-Money Laundering
AQI              Asset Quality Index (Beneish M-Score Parameter)
BSP              Business Strategy Premium (Rate of Interest Component)
CAM              Credit Appraisal Memorandum
CBI              Central Bank of India (Risk Rating Suffix: CBI 1 to CBI 10)
CBOI             Central Bank of India
CBS              Core Banking Solution (Finacle / TCS BaNCS)
CGTMSE           Credit Guarantee Fund Trust for Micro and Small Enterprises
CIBIL            Credit Information Bureau (India) Limited
CMA              Credit Monitoring Arrangement (Financial Statement Spreading Format)
CR               Current Ratio (Current Assets / Current Liabilities)
CRP              Credit Risk Premium (Spread over Base Lending Rate)
DCF              Discounted Cash Flow
DER              Debt-Equity Ratio (Long-Term Debt / Tangible Net Worth)
DFD              Data Flow Diagram
DPDP             Digital Personal Data Protection Act 2023
DSCR             Debt Service Coverage Ratio
DSRI             Days Sales in Receivables Index (Beneish M-Score Parameter)
EBITDA           Earnings Before Interest, Taxes, Depreciation, and Amortization
EMI              Equated Monthly Installment
FCFF             Free Cash Flow to Firm
FOIR             Fixed Obligation to Income Ratio
GAHR-MSR         Graph-Agentic Hybrid RAG with Multi-Stage Re-ranking
GMI              Gross Margin Index (Beneish M-Score Parameter)
HITL             Human-in-the-Loop (Mandatory Manager Interruption Workflow)
IBA              Indian Banks' Association
ILAS             Intelligent Loan Appraisal System
IRB              Internal Ratings-Based Approach (Basel Capital Accord)
KYC              Know Your Customer
LC / BG          Letter of Credit / Bank Guarantee
LTV              Loan-to-Value Ratio
MPBF             Maximum Permissible Bank Finance (Tandon / Nayak Models)
MSE              Micro and Small Enterprises
MSME             Micro, Small, and Medium Enterprises
OCR              Optical Character Recognition
PAT              Profit After Tax
PD               Probability of Default (%)
PII              Personally Identifiable Information
QIS              Quarterly Information System
RAG              Retrieval-Augmented Generation
RBI              Reserve Bank of India
RBLR             Repo-Based Lending Rate
ROC-AUC          Receiver Operating Characteristic - Area Under Curve
RRF              Reciprocal Rank Fusion
SGI              Sales Growth Index (Beneish M-Score Parameter)
SHAP             Shapley Additive exPlanations
SRS              Software Requirements Specification
TATA             Total Accruals to Total Assets (Beneish M-Score Parameter)
TAT              Turnaround Time
TNW              Tangible Net Worth
TOL              Total Outside Liabilities
UML              Unified Modeling Language
WACC             Weighted Average Cost of Capital
XAI              Explainable Artificial Intelligence
XGBoost          Extreme Gradient Boosting
```

---
