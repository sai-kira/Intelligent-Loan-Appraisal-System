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

Credit risk assessment represents one of the oldest and most fundamental disciplines in commercial finance. Historically, credit evaluation has evolved across four distinct generational epochs, progressing from qualitative relational heuristics to modern autonomous, multi-agent artificial intelligence.

```
                         THE FOUR GENERATIONS OF CREDIT UNDERWRITING
                         
  [GEN 1: Heuristic]       [GEN 2: Statistical]     [GEN 3: Machine Learning]    [GEN 4: Autonomous Agentic AI]
  • 5 Cs of Credit         • Altman Z-Score (1968)  • XGBoost / Random Forest    • Multi-Agent Graph (ILAS)
  • Branch Relational      • Logistic Regression    • Deep Neural Networks       • Deterministic Python Math
  • Subjective Scoring     • Credit Bureau (CIBIL)  • Non-Linear Patterns        • Hybrid RAG & Zero-Hallucination
  • 14-Day Manual TAT      • 7-Day Manual TAT       • Black-Box Risk Modeling    • < 45-Second Underwriting TAT
```

### 1. Generation 1: The Traditional "5 Cs of Credit" Framework
For over a century, commercial banking relied predominantly on subjective human judgment centered on the classical **5 Cs of Credit**:
* **Character**: The borrower’s reputational standing, integrity, and historical willingness to honor debt obligations.
* **Capacity**: The financial ability to service principal and interest obligations from operating cash flows, historically evaluated through crude debt-servicing ratios.
* **Capital**: The borrower's equity stake, net worth, and financial resilience to absorb unexpected business losses.
* **Collateral**: The physical or financial assets pledged as secondary repayment security in the event of liquidation.
* **Conditions**: The macroeconomic, regulatory, and sector-specific business climate affecting the borrower's operating margins.

While holistic, the 5 Cs paradigm suffered from severe human subjectivity, cognitive bias, susceptibility to regional manager inconsistencies, and an inability to process high-dimensional quantitative data at scale.

### 2. Generation 2: Parametric Statistical Scoring & Bureau Rating Models
In the late 1960s, statistical credit scoring emerged with **Edward I. Altman’s (1968) Z-Score model**, which pioneered Multivariate Discriminant Analysis (MDA) to forecast corporate bankruptcy. This was subsequently augmented by Logistic Regression ($Logit$) and Probit scoring algorithms in the 1980s, enabling commercial banks to compute empirical default odds for retail applicants. 

In India, this era culminated in the establishment of formal credit reference agencies—principally the **Credit Information Bureau (India) Limited (CIBIL)** in 2000—which standardized consumer credit scoring across a three-digit numerical spectrum ($300$ to $900$). However, bureau scores remain fundamentally backward-looking, reflecting past repayment history while remaining blind to real-time cash flow shocks, macroeconomic stress, or accounting anomalies.

### 3. Generation 3: Monolithic Machine Learning Classifiers
With the proliferation of digital financial data, banks integrated supervised machine learning models—such as Support Vector Machines (SVM), Random Forests, and Gradient Boosting Decision Trees (**XGBoost**). These models effectively captured complex non-linear feature interactions and high-order correlations. 

However, early Generation 3 systems operated as unconstrained "black boxes" lacking regulatory explainability (XAI), struggled to digest unstructured balance sheets, and frequently produced statistical predictions disconnected from official RBI Master Directions and statutory risk grades.

### 4. Generation 4: Autonomous Multi-Agent AI & Deterministic Graph Workflows
The current frontier—embodied by the **Intelligent Loan Appraisal System (ILAS)**—unifies deterministic algorithmic financial engines, supervised machine learning risk classifiers, domain-specific Retrieval-Augmented Generation (RAG), and stateful multi-agent orchestration. By assigning specialized autonomous agents to isolated underwriting functions (PII masking, document parsing, ratio computation, ML risk forecasting, and regulatory cross-referencing), Generation 4 systems achieve complete mathematical determinism, regulatory explainability, and ultra-low latency.

---

## 2.2 ⚖️ Reserve Bank of India (RBI) Prudential Underwriting Directives

As the central banking authority of India, the **Reserve Bank of India (RBI)** establishes mandatory prudential norms governing retail credit exposures, commercial advances, risk-weighted capital adequacy, and priority sector mandates. Any institutional underwriting system must enforce these statutory boundaries as inviolable mathematical constraints.

```
                           RBI PRUDENTIAL UNDERWRITING BOUNDARIES
                           
      RETAIL ADVANCES (HOUSING & CONSUMER)           MICRO & SMALL ENTERPRISES (MSME)
   ┌─────────────────────────────────────────┐    ┌─────────────────────────────────────────┐
   │ • Statutory LTV Slabs: 75% to 90% Max   │    │ • Priority Sector Lending: 40% of ANBC  │
   │ • FOIR Ceiling: Standard Cap <= 50.0%   │    │ • Micro Target: 7.5% of Adjusted ANBC   │
   │ • Mandatory RBLR External Pegging       │    │ • CGTMSE Scheme: Collateral-Free Credit │
   │ • Basel III Risk Weights: 35% to 50%    │    │ • Form MSE 1/II 10-Tier Rating Scale    │
   └─────────────────────────────────────────┘    └─────────────────────────────────────────┘
```

### 1. Loan-to-Value (LTV) Ratios and Risk Weights for Individual Housing Loans
Pursuant to RBI Master Directions on Housing Finance (*RBI/2020-21/73 DOR.No.BP.BC.24/08.12.015/2020-21*), commercial banks are legally prohibited from granting loans against real estate that breach statutory **Loan-to-Value (LTV)** ceilings. Furthermore, regulatory risk weights assigned to housing exposures are directly linked to the loan quantum and LTV threshold:

### Table 2.1: Reserve Bank of India (RBI) Statutory LTV and Risk Weight Norms

| Loan Slab (Facility Quantum) | Statutory LTV Ceiling | Applicable Risk Weight (%) | Minimum Mandatory Borrower Margin | Institutional Regulatory Purpose |
|---|:---:|:---:|:---:|---|
| **Individual Loans $\le ₹30	ext{ Lakhs}$** | **$90.0\%$** | **$35.0\%$** | **$10.0\%$** | Affordable Housing Support; Low Systemic Risk Weighting. |
| **Individual Loans $> ₹30	ext{L} \le ₹75	ext{L}$** | **$80.0\%$** | **$35.0\%$** | **$20.0\%$** | Mid-Segment Housing; Standard Prudential Capital Buffer. |
| **Individual Loans $> ₹75	ext{ Lakhs}$** | **$75.0\%$** | **$50.0\%$** | **$25.0\%$** | Premium Real Estate; Higher Capital Risk Weighting. |
| **Commercial Real Estate (CRE)** | **$60.0\%$** | **$100.0\%$** | **$40.0\%$** | Speculative Asset Protection; Strict Capital Conservation. |

### 2. Fixed Obligation to Income Ratio (FOIR) Norms
While LTV measures asset cover, the **Fixed Obligation to Income Ratio (FOIR)** evaluates the borrower's debt-serviceability and net cash flow capacity. RBI guidelines mandate that aggregate monthly debt obligations (including the proposed EMI, existing personal loans, vehicle loans, and credit card minimum payments) must not exhaust the borrower’s disposable income:

$$	ext{FOIR} = \left( rac{	ext{Proposed Loan EMI} + \sum 	ext{Existing Monthly Loan Obligations}}{	ext{Gross Monthly Income}} ight) 	imes 100$$

* **Standard Prudential Ceiling**: $	ext{FOIR} \le 50.0\%$.
* **High-Income Salaried Concession**: For borrowers with gross monthly income exceeding ₹1,50,000, credit policies permit a maximum FOIR of up to **$60.0\%$**, provided Net Take-Home Pay ($	ext{NTH}$) satisfies minimum subsistence thresholds.

### 3. Priority Sector Lending (PSL) & MSME Credit Mandates
Under RBI Priority Sector Lending norms (*FIDD.CO.Plan.BC.5/04.09.01/2020-21*), Scheduled Commercial Banks must allocate at least **$40\%$ of Adjusted Net Bank Credit (ANBC)** or Credit Equivalent of Off-Balance Sheet Exposure (CEOBE) to priority sectors. Specifically:
- **Micro Enterprises Sub-Target**: At least **$7.5\%$ of ANBC** must be disbursed to micro-enterprises.
- **Credit Guarantee Scheme (CGTMSE)**: Loans to Micro and Small Enterprises up to **₹5.00 Crores** granted without third-party collateral or personal guarantees are eligible for guarantee cover ranging between **$75\%$ and $85\%$** under the Credit Guarantee Fund Trust for Micro and Small Enterprises (CGTMSE).

---

## 2.3 🏛️ Basel II and Basel III Accords: Internal Ratings-Based (IRB) Approaches

The Basel Committee on Banking Supervision (BCBS) establishes international capital standards designed to ensure commercial banks maintain adequate capital buffers against credit, market, and operational risks. 

```
                               BASEL III CAPITAL CONSERVATION ARCHITECTURE
                               
   ┌────────────────────────────────────────────────────────────────────────────────────────┐
   │                           TOTAL MINIMUM REGULATORY CAPITAL                             │
   │                    (Minimum 11.50% of Total Risk-Weighted Assets - RWA)                │
   ├────────────────────────────────────────────────────────┬───────────────────────────────┤
   │               TIER 1 CAPITAL (Min 9.50%)               │   TIER 2 CAPITAL (Max 2.0%)   │
   ├────────────────────────────┬───────────────────────────┼───────────────────────────────┤
   │ Common Equity Tier 1 (CET1)│ Capital Conservation      │ Supplementary Capital:        │
   │ Minimum 5.50% RWA          │ Buffer (CCB) = 2.50%      │ Subordinated Debt, Provisions │
   └────────────────────────────┴───────────────────────────┴───────────────────────────────┘
```

Under Basel II and Basel III frameworks adopted by the Reserve Bank of India, commercial banks evaluate credit risk via two primary methodological regimes:
1. **The Standardized Approach (SA)**: Banks apply static, regulator-prescribed risk weights to exposures based on external credit agency ratings (CRISIL, ICRA, CARE).
2. **The Internal Ratings-Based (IRB) Approach**: Banks utilize internal statistical models to estimate empirical risk parameters for every credit asset.

### Key Risk Parameters in Advanced Risk Modeling:
Under the Foundation IRB (F-IRB) and Advanced IRB (A-IRB) paradigms, the **Expected Loss ($EL$)** and regulatory capital requirements of a loan asset are calculated as a function of four structural risk drivers:

$$EL = PD 	imes LGD 	imes EAD$$

Where:
* **Probability of Default ($PD$)**: The empirical likelihood (expressed as a percentage) that a borrower will default on credit obligations over a 12-to-24 month horizon. In ILAS, $PD$ is estimated via an optimized **XGBoost classification model** and mapped to the Basel 5-Tier Default Scale.
* **Loss Given Default ($LGD$)**: The percentage of exposure lost if a default occurs, determined by collateral value, liquidation seniority, and recovery costs:
  $$LGD = 1 - 	ext{Recovery Rate} = 1 - \left( rac{	ext{Discounted Recoverable Collateral Value}}{EAD} ight)$$
* **Exposure at Default ($EAD$)**: The gross nominal exposure outstanding at the time of default, incorporating drawn term loans and Credit Conversion Factors (CCF) for undrawn working capital lines:
  $$EAD = 	ext{Drawn Balance} + (	ext{Undrawn Credit Limit} 	imes CCF)$$

### Table 2.2: Basel III Capital Adequacy Risk Weights for Retail & MSME Asset Classes

| Asset Category | Loan Facility Description | Standard Basel III Risk Weight | Capital Charge at 11.5% CRAR |
|---|---|:---:|:---:|
| **Retail: Low-Risk Housing** | Housing Loans $\le ₹30	ext{L}$ with $	ext{LTV} \le 80\%$ | **$35.0\%$** | **$4.025\%$ of Exposure** |
| **Retail: Mid-Risk Housing** | Housing Loans $> ₹75	ext{L}$ with $	ext{LTV} \le 75\%$ | **$50.0\%$** | **$5.750\%$ of Exposure** |
| **Retail: Consumer / Personal** | Unsecured Personal Loans, Consumer Credit Cards | **$125.0\%$** | **$14.375\%$ of Exposure** |
| **MSME: Investment Grade** | Rated `CBI 1` to `CBI 3` (Score $>75$), Low $PD$ | **$75.0\%$** | **$8.625\%$ of Exposure** |
| **MSME: Standard Grade** | Rated `CBI 4` to `CBI 6` (Score $51–75$), Moderate $PD$ | **$100.0\%$** | **$11.500\%$ of Exposure** |
| **MSME: Sub-Hurdle Grade** | Rated `CBI 7` to `CBI 10` (Score $\le 50$), High Default Risk | **$150.0\%$** | **$17.250\%$ of Exposure** |

---

## 2.4 🔒 Legal & Privacy Norms: DPDP Act 2023 & RBI IT Governance

In modern digital credit underwriting, financial engineering must strictly co-exist with data privacy jurisprudence and statutory IT risk governance. The deployment of autonomous artificial intelligence systems in commercial banking is governed by two foundational regulatory statutes in India:

```
                            STATUTORY REGULATORY COMPLIANCE PILLARS
                            
     DIGITAL PERSONAL DATA PROTECTION ACT 2023            RBI IT GOVERNANCE & MODEL RISK (2023)
   ┌─────────────────────────────────────────────┐    ┌─────────────────────────────────────────────┐
   │ • Cryptographic PII Token Masking           │    │ • Zero Uncontrolled Auto-Sanctions          │
   │ • SHA-256 Irreversible Anonymization        │    │ • Mandatory Human-in-the-Loop (HITL) Gate   │
   │ • Purpose Limitation & Consent Enforcement  │    │ • Deterministic Model Risk Governance       │
   │ • Data Principal Privacy Rights Protection  │    │ • Tamper-Proof PostgreSQL Vigilance Audit   │
   └─────────────────────────────────────────────┘    └─────────────────────────────────────────────┘
```

### 1. Digital Personal Data Protection (DPDP) Act 2023 Compliance
Enacted in August 2023, the **DPDP Act 2023** establishes stringent statutory duties for commercial banks operating as *Data Fiduciaries*. The Act mandates:
* **Purpose Limitation & Data Minimization**: Personal data collected for loan appraisal cannot be repurposed or exposed to external AI model providers without explicit, informed consent.
* **Personally Identifiable Information (PII) Protection**: Real borrower names, Aadhaar numbers, Permanent Account Numbers (PAN), and mobile contact details must be cryptographically protected.
* **Architectural Implementation in ILAS**: The platform incorporates a dedicated **Customer Agent** at the perimeter of the LangGraph state machine. The agent applies an irreversible deterministic tokenization algorithm:
  $$	ext{Masked\_ID} = 	ext{"APPLICANT\_"} + 	ext{SHA256}(	ext{Real Name} \,||\, 	ext{Salt})[:4]$$
  All downstream agents (financial analysis, ML risk, policy RAG, and compliance) execute solely on masked identifiers (`APPLICANT_4427`), ensuring zero unencrypted PII leakage to external vector databases or model endpoints.

### 2. RBI Master Direction on IT Governance, Risk & Assurance (2023)
Issued in November 2023 (*RBI/2023-24/107 DoS.CO.CSITE.SEC.No.7/31.01.015/2023-24*), this directive sets out strict controls for algorithmic systems and automated credit decisioning:
* **Model Risk Management (MRM)**: Automated credit scoring models must undergo rigorous backtesting, boundary validation, and sensitivity benchmarking.
* **Prohibition of Unconstrained Auto-Disbursement**: Commercial banks must enforce explicit **Human-in-the-Loop (HITL)** governance gates. Fully automated credit sanctioning without branch credit manager oversight is strictly prohibited.
* **Tamper-Proof Audit Logging**: Every parameter, credit score, ratio computation, and discretionary manager override must be immutably recorded in a centralized relational repository for inspection by internal bank vigilance and statutory RBI audit teams.

---

## 2.5 🧠 Survey of Agentic AI, Multi-Agent State Machines & Hybrid RAG in Banking

Recent advancements in Large Language Models (LLMs) and agentic workflows have created unprecedented opportunities for financial technology. However, applying generative artificial intelligence to quantitative commercial banking requires addressing critical architectural limitations.

```
                              THE AGENTIC RAG SYSTEM PARADIGM
                              
   [User Loan Request] ──► [LangGraph StateGraph] ──► [GAHR-MSR Hybrid RAG Engine]
                                  │                            │
                                  ▼                            ▼
                      [11 Specialized Agents]     ┌──────────────────────────────┐
                      • Customer PII Node         │ 1. Dense Vector (pgvector)   │
                      • Financial Ratio Node      │ 2. Sparse Lexical (tsvector) │
                      • ML Default Risk Node      │ 3. Reciprocal Rank Fusion    │
                      • Report Synthesizer Node   │ 4. Cross-Encoder Re-Ranking  │
                                                  └──────────────────────────────┘
```

### 1. The Fallacy of Monolithic, Unconstrained LLMs in Finance
Early experiments with generative AI in finance utilized monolithic, single-prompt LLMs (e.g., zero-shot GPT-4 or Claude). These architectures suffered from fatal vulnerabilities in institutional banking:
* **Mathematical Hallucinations**: LLMs perform auto-regressive token probability estimation rather than exact arithmetic, leading to hallucinated debt ratios, incorrect interest compounding, and invalid LTV calculations.
* **Token Cost Explosion**: Ingesting multi-page balance sheets and hundred-page regulatory circulars into single LLM context windows incurs excessive latency and prohibitive API operational costs ($>\$0.10$ per loan dossier).
* **State Loss & Non-Determinism**: Monolithic prompts cannot guarantee strict, reproducible adherence to statutory branch credit policies.

### 2. Multi-Agent State Machine Architecture (LangGraph)
To overcome these limitations, recent research (Wu et al., 2023; Chase et al., 2024) advocates for **deterministic multi-agent state machines**. In this architecture, loan appraisal is modeled as a stateful, directed graph:

$$G = (V, E, S)$$

Where:
* $V = \{v_1, v_2, \dots, v_{11}\}$ represents isolated agent nodes, each specializing in a single domain (e.g., OCR, ratio analysis, ML risk, or compliance).
* $E \subseteq V 	imes V$ defines conditional transition edges governed by strict mathematical thresholds (such as the 50-mark Hurdle Rate).
* $S$ is a globally typed state object (`LoanApplicationState`) persisted transactionally in PostgreSQL (`PostgresSaver`).

Crucially, mathematical calculations are delegated entirely to local Python mathematical engines ($0$ token consumption), while LLMs are restricted strictly to narrative synthesis and semantic policy retrieval.

### 3. Graph-Agentic Hybrid RAG (GAHR-MSR) in Policy Retrieval
Standard naive vector retrieval (RAG) fails in banking because regulatory Master Directions contain dense statutory keywords, circular numbers, and precise numeric thresholds that semantic embeddings alone often miss. State-of-the-art financial information retrieval requires a **Hybrid Search Architecture**:

1. **Dense Vector Search**: Computes cosine similarity across 3072-dimensional vector embeddings stored in PostgreSQL via `pgvector` to capture high-level semantic intent:
   $$	ext{Sim}_{	ext{dense}}(q, d) = rac{\mathbf{e}_q \cdot \mathbf{e}_d}{\|\mathbf{e}_q\| \|\mathbf{e}_d\|}$$
2. **Sparse Lexical Search**: Computes BM25 full-text keyword matching using PostgreSQL inverted indices (`tsvector` and `tsquery`) to match exact circular codes, acronyms (e.g., "CGTMSE", "RBLR", "FOIR"), and loan ceilings.
3. **Reciprocal Rank Fusion (RRF)**: Merges dense and sparse result lists into a unified relevance ranking without requiring score normalization:
   $$RRF\_Score(d \in D) = \sum_{m \in \{	ext{dense}, 	ext{sparse}\}} rac{1}{k + rank_m(d)} \quad (	ext{where } k = 60)$$
4. **Cross-Encoder Re-Ranking**: Passes the top candidate passages through a deep transformer cross-encoder (`ms-marco-MiniLM-L-6-v2`) to perform full token-level query-document cross-attention, ensuring only verbatim, legally authoritative policy clauses are cited in the final Credit Appraisal Memorandum.

---
