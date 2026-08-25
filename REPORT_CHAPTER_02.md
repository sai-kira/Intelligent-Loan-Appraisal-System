# 🏛️ CENTRAL BANK OF INDIA
## REGIONAL OFFICE, VISAKHAPATNAM | ANDHRA PRADESH
### RISK MANAGEMENT & CREDIT APPRAISAL DIVISIONS

<br>
<br>
<br>

---

# 📖 CHAPTER 2
# **REGULATORY FRAMEWORK & LITERATURE SURVEY**

---

<br>

```
========================================================================================
                                 CHAPTER ROADMAP & METRICS
========================================================================================
  2.1 Evolution of Credit Risk Assessment: From 5 Cs to Autonomous AI
  2.2 Reserve Bank of India (RBI) Prudential Underwriting Directives
  2.3 Basel II and Basel III Accords: Internal Ratings-Based (IRB) Approaches
  2.4 Legal & Privacy Norms: DPDP Act 2023 & RBI IT Governance
  2.5 Survey of Agentic AI, Multi-Agent State Machines & Hybrid RAG in Banking
========================================================================================
```

<br>
<br>
<br>

---
<div style="page-break-after: always;"></div>

# CHAPTER 2: REGULATORY FRAMEWORK & LITERATURE SURVEY

---

## 2.1 📜 Evolution of Credit Risk Assessment: From 5 Cs to Autonomous AI

Credit risk assessment—the structured evaluation of the likelihood that a borrower will fail to meet their contractual debt obligations—has undergone profound conceptual and technological evolution over the past century. Within commercial banking, the methodology for measuring borrower creditworthiness has progressed through four distinct historical paradigms:

```
                            EVOLUTION OF CREDIT UNDERWRITING PARADIGMS
                            
  ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐       ┌───────────────────────┐
  │   1. HEURISTIC ERA    │       │ 2. STATISTICAL MODELS │       │  3. MACHINE LEARNING  │       │ 4. AGENTIC AI (ILAS)  │
  │ • The 5 Cs of Credit  │  ──►  │ • Altman Z-Score      │  ──►  │ • Random Forest       │  ──►  │ • 11-Agent StateGraph │
  │ • Subjective Judgment │       │ • Logistic Regression │       │ • XGBoost / LightGBM  │       │ • Deterministic Math  │
  │ • Branch Discretion   │       │ • Credit Bureau Scores│       │ • SHAP Explainability │       │ • GAHR-MSR Hybrid RAG │
  └───────────────────────┘       └───────────────────────┘       └───────────────────────┘       └───────────────────────┘
```

### 1. The Heuristic Era (The 5 Cs of Credit):
For decades, public sector commercial banks relied on the classical **"Five Cs of Credit"** framework to structure loan appraisals:
- **Character**: The borrower's historical integrity, reputation, debt repayment willingness, and operational pedigree.
- **Capacity**: The borrower's cash-flow generating ability to service interest and principal amortization, evaluated through past turnover and salary credits.
- **Capital**: The borrower's own financial stake and equity contribution in the venture, measured via Tangible Net Worth (TNW) and promoter margin.
- **Collateral**: Secondary security pledged (immovable property, plant, hypothecated stock) to mitigate loss given default.
- **Conditions**: Macroeconomic, industry-specific, and regulatory environment governing the borrower's operating sector.

While comprehensive in scope, the heuristic paradigm was fundamentally subjective, heavily reliant on individual loan officer discretion, and vulnerable to cognitive bias and geographical inconsistency across branches.

### 2. The Statistical Scoring Era:
The introduction of multivariate statistical analysis revolutionized quantitative credit scoring. **Edward Altman (1968)** pioneered the **Altman Z-Score**, using Multiple Discriminant Analysis (MDA) on five balance sheet ratios to forecast corporate bankruptcy. Subsequent advancements by **Ohlson (1980)** introduced Logistic Regression (Logit) models, allowing banks to compute the conditional probability of default ($PD$). Concurrently, centralized credit information companies (such as **CIBIL** in India, established under the Credit Information Companies Act 2005) introduced three-digit bureau scores ($300–900$) derived from historical delinquency records and credit utilization.

### 3. The Machine Learning Era:
Over the past decade, non-linear Machine Learning (ML) algorithms—including **Gradient Boosted Decision Trees (XGBoost, LightGBM)** and Deep Neural Networks—have demonstrated superior predictive accuracy over traditional linear scoring models. ML models ingest high-dimensional datasets, uncovering non-linear interactions and subtle default signals. However, standard ML models often operated as opaque "black boxes," hindering regulatory adoption until the advent of **Explainable Artificial Intelligence (XAI)** frameworks, notably **Shapley Additive exPlanations (SHAP)** rooted in cooperative game theory.

### 4. The Autonomous Agentic Era (The ILAS Paradigm):
Despite predictive advancements, stand-alone ML models cannot perform multi-step document extraction, policy cross-referencing, multi-year financial spreading, and memo drafting. The state-of-the-art frontier—realized in this project—is **Autonomous Multi-Agent AI**, wherein specialized, autonomous software agents orchestrated via state machines execute end-to-end underwriting tasks deterministically, transparently, and with strict Human-in-the-Loop governance.

---

## 2.2 ⚖️ Reserve Bank of India (RBI) Prudential Underwriting Directives

As the central banking authority, the **Reserve Bank of India (RBI)** establishes mandatory prudential norms governing retail and commercial credit underwriting across all Scheduled Commercial Banks. The Intelligent Loan Appraisal System (ILAS) programmatically encodes these directives as hard boundary constraints.

```
                         RBI PRUDENTIAL BOUNDARY ENFORCEMENT ENGINE
                         
        ┌───────────────────────────────────┬───────────────────────────────────┐
        │  RETAIL ADVANCES (HOUSING LOANS)  │     MSME & COMMERCIAL ADVANCES    │
        ├───────────────────────────────────┼───────────────────────────────────┤
        │ • Up to ₹30 Lakhs: Max 90% LTV    │ • MSMED Act 2020 Composite Norms  │
        │ • ₹30L to ₹75 Lakhs: Max 80% LTV  │ • Mandatory Form MSE 1/II Ratings │
        │ • Above ₹75 Lakhs: Max 75% LTV    │ • Statutory 50-Mark Hurdle Rate   │
        │ • FOIR Ceiling: Statutory <= 50%  │ • 01.07.2026 External RBLR Grid   │
        └───────────────────────────────────┴───────────────────────────────────┘
```

### 1. Statutory Loan-to-Value (LTV) and Risk-Weight Directives:
Under RBI Master Circulars on Housing Finance (*RBI/2015-16/203 DBR.BP.BC.No.44/08.12.015/2015-16* and subsequent notifications), loan disbursements for individual residential housing properties must strictly respect tiered LTV ceilings to prevent asset bubbles and mitigate default exposure.

### Table 2.1: Reserve Bank of India (RBI) Statutory LTV and Risk Weight Norms

| Loan Quantum Tier | Maximum Permissible LTV Ratio | Statutory Minimum Borrower Margin | Applicable RBI Risk Weight | Capital Provisioning Impact |
|---|:---:|:---:|:---:|---|
| **Up to ₹30.00 Lakhs** | **$\le 90.0\%$** | $10.0\%$ | **$35.0\%$** | Low Capital Charge (Standard Retail) |
| **₹30.01 Lakhs to ₹75.00 Lakhs** | **$\le 80.0\%$** | $20.0\%$ | **$35.0\%$** (if $	ext{LTV} \le 75\%$) / **$50.0\%$** | Moderate Capital Charge |
| **Above ₹75.00 Lakhs** | **$\le 75.0\%$** | $25.0\%$ | **$50.0\%$** | Standard Risk Weight |
| **Commercial Real Estate (CRE)** | **$\le 65.0\%$** | $35.0\%$ | **$100.0\%$** | High Capital Provisioning Requirement |

In ILAS, the **Financial Analysis Agent** and **Decision Synthesis Agent** automatically compute:
$$	ext{LTV Ratio} = \left( rac{	ext{Requested Loan Amount}}{	ext{Fair Market Property Valuation}} ight) 	imes 100$$
If $	ext{LTV}$ exceeds the statutory ceiling, the system automatically flags a **Hard Rejection** unless covered by statutory guarantee schemes (e.g., CGTMSE).

### 2. Fixed Obligation to Income Ratio (FOIR) Directives:
To prevent over-indebtedness, Indian banking standards cap the total monthly debt service obligations of a borrower relative to their verified monthly gross income:
$$	ext{FOIR} = \left( rac{\sum 	ext{Existing Monthly EMIs} + 	ext{Proposed Loan Monthly EMI}}{	ext{Verified Gross Monthly Income}} ight) 	imes 100$$
* **Statutory Benchmark**: $	ext{FOIR} \le 50.0\%$ for standard retail applicants.
* **Affluent / High-Income Threshold**: Maximum $60.0\%$ permissible only for high net worth salaried borrowers where net surplus income exceeds ₹1,00,000 per month.

### 3. Revised MSME Classification Criteria (MSMED Act 2020):
Under the Ministry of Micro, Small and Medium Enterprises notification (*S.O. 2119(E) dated 26.06.2020*), composite classification criteria apply uniformly across manufacturing and service sectors:
- **Micro Enterprise**: Investment in Plant & Machinery $\le ₹1	ext{ Crore}$ AND Annual Turnover $\le ₹5	ext{ Crores}$.
- **Small Enterprise**: Investment in Plant & Machinery $\le ₹10	ext{ Crores}$ AND Annual Turnover $\le ₹50	ext{ Crores}$.
- **Medium Enterprise**: Investment in Plant & Machinery $\le ₹50	ext{ Crores}$ AND Annual Turnover $\le ₹250	ext{ Crores}$.

### 4. External Benchmark Lending Rate (EBLR / RBLR) Regime:
Under RBI Master Direction *DBR.Dir.No.85/13.03.00/2019-20 dated 04.09.2019*, all scheduled commercial banks must link all floating-rate personal, retail, and MSME loans to an **External Benchmark Lending Rate**. Central Bank of India has adopted the **Reserve Bank of India Repo Rate** as its benchmark, operating under the **Repo-Based Lending Rate (RBLR)** framework (Base Rate: $8.25\%$ as of the 01.07.2026 Master Circular).

---

## 2.3 🏛️ Basel II and Basel III Accords: Internal Ratings-Based (IRB) Approaches

The Basel Committee on Banking Supervision (BCBS) frameworks—enforced in India through the RBI Master Circular on Basel III Capital Regulations—mandate that commercial banks maintain a minimum Total Capital to Risk-Weighted Assets Ratio (**CRAR $\ge 11.5\%$** including the Capital Conservation Buffer of $2.5\%$).

```
                           BASEL III REGULATORY CAPITAL ARCHITECTURE
                           
                 ┌────────────────────────────────────────────────────────┐
                 │       Total Capital Adequacy Ratio (CRAR >= 11.5%)     │
                 └───────────────────────────┬────────────────────────────┘
                                             │
                     ┌───────────────────────┴───────────────────────┐
                     ▼                                               ▼
         ┌───────────────────────┐                       ┌───────────────────────┐
         │     TIER 1 CAPITAL    │                       │     TIER 2 CAPITAL    │
         │ Common Equity (CET1)  │                       │ Subordinated Debt,    │
         │ & Retained Earnings   │                       │ General Provisions    │
         └───────────────────────┘                       └───────────────────────┘
```

### 1. Internal Ratings-Based (IRB) Mathematical Formulations:
Under the Foundation IRB (F-IRB) and Advanced IRB (A-IRB) approaches, credit risk capital requirements are calculated based on four fundamental risk parameters:

1. **Probability of Default ($PD$)**: The statistical probability that a borrower will default on their credit obligation within a 1-year forward horizon. In ILAS, $PD$ is estimated using our calibrated **XGBoost Credit Default Model**.
2. **Loss Given Default ($LGD$)**: The percentage of exposure lost if a default occurs, reflecting collateral recovery efficiency ($LGD pprox 35\%–45\%$ for fully secured advances).
3. **Exposure at Default ($EAD$)**: The gross dollar/rupee amount outstanding when the borrower defaults.
4. **Effective Maturity ($M$)**: The remaining contractual duration of the loan facility.

### 2. Expected Loss ($EL$) vs. Unexpected Loss ($UL$):
Expected Loss represents the baseline cost of doing business, covered through loan loss provisioning and interest rate risk spreads:
$$EL = PD 	imes LGD 	imes EAD$$
Unexpected Loss represents statistical volatility around the Expected Loss, requiring equity capital buffers under the Basel Value-at-Risk ($VaR$) formulation:
$$K = \left[ LGD 	imes \Phi \left( rac{\Phi^{-1}(PD) + \sqrt{ho} \cdot \Phi^{-1}(0.999)}{\sqrt{1 - ho}} ight) - (PD 	imes LGD) ight] 	imes 	ext{Maturity\_Adjustment}(M)$$
*(where $\Phi$ is the standard normal cumulative distribution function, and $ho$ is the asset correlation factor).*

### Table 2.2: Basel III Capital Adequacy Risk Weights for Retail & MSME Asset Classes

| Asset Classification | Typical Basel Risk Weight | Regulatory Provisioning Mandate | Applicable ILAS Underwriting Track |
|---|:---:|:---:|---|
| **Standard Housing Loan ($	ext{LTV} \le 80\%$)** | **$35.0\%$** | $0.25\%$ Standard Asset Provision | Retail Underwriting Pipeline |
| **Retail Other (Personal / Unsecured Loans)** | **$100.0\% – 125.0\%$** | $0.40\%$ Standard Asset Provision | Retail Underwriting Pipeline |
| **MSME Priority Sector Advance** | **$75.0\%$** | $0.25\%$ Standard Asset Provision | Form MSE 1 / Form MSE II |
| **Commercial Real Estate (CRE)** | **$100.0\%$** | $1.00\%$ Standard Asset Provision | Corporate Financial Hub |
| **Non-Performing Asset (Sub-Standard / Doubtful)** | **$150.0\%$** | $15.0\% – 100.0\%$ Provisioning | Automatic Rejection (Hurdle Rate) |

---

## 2.4 🔒 Legal & Privacy Norms: DPDP Act 2023 & RBI IT Governance

In August 2023, the Government of India enacted the landmark **Digital Personal Data Protection (DPDP) Act 2023**, establishing statutory obligations for all financial institutions categorized as "Data Fiduciaries."

```
                         DPDP ACT 2023 COMPLIANCE ARCHITECTURE
                         
  ┌───────────────────────┐       ┌───────────────────────────────┐       ┌───────────────────────┐
  │  Raw Applicant Data   │       │ Customer Agent (PII Masking)  │       │ Downstream AI Agents  │
  │ • Real Name           │  ──►  │ • SHA-256 Token Masking       │  ──►  │ • Process Pseudonym   │
  │ • Aadhaar / PAN       │       │ • Secure Session Partition    │       │ • Zero PII Leakage    │
  │ • Phone / Email       │       │ • Salted Ephemeral Storage    │       │ • 100% Privacy Secure │
  └───────────────────────┘       └───────────────────────────────┘       └───────────────────────┘
```

### 1. Key Provisions of the DPDP Act 2023 Enforced in ILAS:
- **Purpose Limitation (Section 6)**: Customer data ingested during loan applications must be processed strictly for underwriting and regulatory compliance.
- **Data Minimization (Section 8)**: Personal data must not be exposed to downstream machine learning models or external API endpoints unless masked.
- **Severe Non-Compliance Penalties**: Section 33 establishes statutory penalties of up to **₹250 Crores** for failures to implement reasonable security safeguards preventing personal data breaches.

### 2. PII Token Masking Implementation:
To guarantee absolute compliance with the DPDP Act 2023, ILAS deploys the **Customer Agent** at the very entrance of the LangGraph state machine:
- Real borrower names, telephone numbers, and PAN identifiers are stripped and transformed into cryptographic SHA-256 session tokens (e.g., *Chalumuru Sai Kiran* $ightarrow$ `APPLICANT_4427`).
- All 10 downstream underwriting agents—including the LLM-powered Report Writing Agent—process only the masked token identifiers, completely preventing PII leakage.
- Unmasked names are restored only within the local secure session partition during final Word document stamping.

### 3. RBI IT Governance & Cyber Security Directives (2023):
The RBI *Master Direction on Information Technology Governance, Risk, Controls and Assurance Practices (2023)* mandates that all automated underwriting algorithms must feature:
- **Comprehensive Auditability**: An immutable log recording every algorithmic decision.
- **Model Risk Governance**: Continuous validation against drift, demographic bias, and calculation inaccuracies.
- **Access Control**: Role-Based Access Control (RBAC) preventing unauthorized loan disbursements.

---

## 2.5 🤖 Survey of Agentic AI, Multi-Agent State Machines & Hybrid RAG in Banking

Recent literature in Artificial Intelligence and Financial Technology has highlighted the transformative potential of combining **Large Language Models (LLMs)**, **Multi-Agent Systems (MAS)**, and **Retrieval-Augmented Generation (RAG)** for financial analysis:

```
                      MONOLITHIC LLM VS. MULTI-AGENT STATEGRAPH ARCHITECTURE
                      
   A. MONOLITHIC LLM (UNCONSTRAINED)                 B. MULTI-AGENT STATEGRAPH (ILAS)
   ┌───────────────────────────────┐                 ┌───────────────────────────────┐
   │ Single Prompt Ingestion       │                 │ LangGraph Cyclical Workflow   │
   │ • Prone to Hallucinations     │                 │ • 11 Specialized Agent Nodes  │
   │ • Calculation Errors in EMI   │                 │ • 100% Deterministic Math     │
   │ • High Token Cost ($0.10+/call│                 │ • GAHR-MSR Hybrid Search RAG  │
   │ • No Audit State Persistence  │                 │ • PostgreSQL Checkpointing    │
   └───────────────────────────────┘                 └───────────────────────────────┘
```

### 1. Limitations of Monolithic Large Language Models in Banking:
Early attempts to apply monolithic LLMs (e.g., unconstrained GPT-4 or Gemini instances) to credit underwriting encountered fundamental institutional hurdles:
- **Mathematical Hallucinations**: Autoregressive transformer models generate text probabilistically and frequently miscalculate non-linear compounding formulas (e.g., EMI amortization schedules, Altman Z''-Scores).
- **Context Drift & Token Inefficiency**: Ingesting 50-page financial statements into a single prompt consumes excessive tokens ($10,000+$ tokens per call), creating prohibitive operating costs.
- **Lack of Process State Control**: Monolithic prompts cannot enforce strict conditional execution sequences or pause mid-workflow for human manager intervention.

### 2. Multi-Agent Systems (MAS) & LangGraph:
To overcome these limitations, recent research (Wu et al., 2023; Chase et al., 2024) established the efficacy of **Multi-Agent Orchestration via Cyclical State Graphs (LangGraph)**. Rather than relying on a single generalist model, the system divides the underwriting domain into specialized autonomous nodes:
- Each node executes a single specialized task (e.g., OCR extraction, ratio mathematics, ML risk prediction, policy retrieval).
- State transitions are managed via an immutable shared schema (`LoanApplicationState`).
- The graph supports native checkpointing and asynchronous state interruptions (`interrupt()`), providing the mathematical foundation for Human-in-the-Loop governance.

### 3. Evolution of Hybrid RAG Architectures:
Standard "Naive RAG" systems rely exclusively on dense vector cosine similarity (e.g., BERT or text-embedding-ada-002), which frequently fails in financial regulatory domains due to the vocabulary mismatch problem (e.g., searching for *"LTV limits"* misses circular clauses discussing *"margin requirements for residential housing"*).

To resolve this, modern financial information retrieval utilizes **Hybrid Search RAG**:
- **Dense Vector Retrieval (3072-dim pgvector)** captures high-level semantic intent.
- **Sparse BM25 Lexical Search (`tsvector`)** captures exact statutory keywords and section numbers.
- **Reciprocal Rank Fusion (RRF)** merges disparate ranking distributions.
- **Cross-Encoder Re-ranking (`ms-marco-MiniLM-L-6-v2`)** performs joint query-document attention, achieving superior precision on complex RBI master circulars.

---
