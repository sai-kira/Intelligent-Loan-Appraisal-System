# 🏦 Central Bank of India — Intelligent Loan Appraisal System (ILAS)
> **Autonomous, Regulatory-Compliant Multi-Agent AI Platform for Retail & MSME Credit Underwriting**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-FF6F00.svg)](https://langchain-ai.github.io/langgraph/)
[![PostgreSQL + pgvector](https://img.shields.io/badge/Database-PostgreSQL_%2B_pgvector-336791.svg)](https://github.com/pgvector/pgvector)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Proprietary_/_Institutional-green.svg)]()

---

## 📌 Executive Overview

The **Central Bank of India Intelligent Loan Appraisal System (ILAS)** is an enterprise-grade AI credit underwriting solution designed to reduce loan appraisal turnaround time (TAT) from **7–14 days down to under 60 seconds** while ensuring 100% adherence to **Reserve Bank of India (RBI)** master directions and **Central Bank of India (CBoI)** statutory credit policies.

### 🌟 Key Capabilities
- **Dual Underwriting Engines**:
  - **Retail Advances**: Evaluates FOIR cash-flow serviceability, RBI property-class Loan-to-Value (LTV) limits, and CIBIL bureau risk tiers.
  - **MSME Advances**: Implements **Form MSE 1 (Existing Units - 13 Parameters)** and **Form MSE II (Greenfield Units - 9 Parameters)**, mapping borrowers to the official **10-Tier Central Bank Risk Grades (`CBI 1` to `CBI 10`)**.
- **Prudential Hurdle Rate & Defaulter Governance**:
  - Enforces the statutory **50-Mark Hurdle Rate** (`CBI 7`–`CBI 10` automatically rejected).
  - Implements the **Defaulter Override Rule** (Overdue $> 3$ months clamps score to `0` and assigns `CBI 10`).
  - Attaches operational covenants to moderate passing grades (`CBI 5` and `CBI 6`).
- **Dynamic RBLR Interest Rate Engine**: Pegged directly to the **01.07.2026 Master Circular** (Base RBLR @ 8.25%, Repo 5.25% + Spread 1.85%, Credit Risk Premium, and CGTMSE 25 bps concessions).
- **GAHR-MSR Hybrid Policy RAG**: PostgreSQL `pgvector` dense vector search (3072 dims) + `tsvector` BM25 sparse search + Reciprocal Rank Fusion (RRF) + Cross-Encoder re-ranking.
- **Predictive Machine Learning**: XGBoost default classifier calibrated to Basel 5-tier PD % with SHAP explainability.
- **Human-In-The-Loop (HITL) Checkpoints**: LangGraph state checkpointing with formal override justifications stored in PostgreSQL.
- **Executive Portfolio Analytics**: Real-time asset quality monitoring, 10-Tier CBI distribution, product exposure allocation, and ALCO CSV export.

---

## 🏛️ System Architecture

```mermaid
graph TD
    A([📝 Applicant / Branch Submission]) --> B[1. Document Extraction Agent]
    B --> C[2. Verification & KYC Agent]
    C --> D[3. Financial Ratio Engine]
    D --> E[4. Credit Risk ML Agent - XGBoost/SHAP]
    E --> F[5. Regulatory RAG Agent - pgvector Hybrid Search]
    F --> G[6. Sanction & Compliance Agent]
    G --> H[7. Fraud & Anomaly Agent]
    H --> I{Decision Splitter}
    
    I -- Auto-Sanction Eligible --> J[8. Report Generation Agent]
    I -- Borderline / High Exposure --> K[9. Manager Approval HITL Node]
    K -- Manager Decision Approved/Rejected --> J
    
    J --> L[10. Notification & Audit Log Agent]
    L --> M([🏁 Final Sanction / Appraisal Memo Delivered])
```

---

## 📊 10-Tier Central Bank MSE Risk Matrix

| CBI Grade | Marks Range | Risk Profile | Regulatory Action |
|:---:|:---:|:---:|---|
| **CBI 1** | **$> 90$** | Exceptional Safety (Prime) | Fast-Track Approval; Best RBLR rate (8.15% - 8.40%). |
| **CBI 2** | **$81 - 90$** | Very High Safety | Approved; Preferred credit risk spread. |
| **CBI 3** | **$71 - 80$** | High Safety | Approved; Standard collateral coverage. |
| **CBI 4** | **$61 - 70$** | Adequate Safety | Approved; Standard margins and stock review. |
| **CBI 5** | **$56 - 60$** | Moderate Safety | **Conditional Sanction**: Special covenants & quarterly stock audit. |
| **CBI 6** | **$51 - 55$** | Minimum Hurdle Passing | **Conditional Sanction**: Enhanced personal guarantee required. |
| **CBI 7** | **$46 - 50$** | Ineligible / Sub-Hurdle | **REJECTED**: Fails statutory 50-mark Hurdle Rate. |
| **CBI 8** | **$41 - 45$** | Weak Capacity | **REJECTED**: Elevated financial vulnerability. |
| **CBI 9** | **$36 - 40$** | High Vulnerability | **REJECTED**: Cash deficits / severe leverage. |
| **CBI 10** | **$\le 35$** | Substantial Risk / Defaulter | **REJECTED**: Critical default risk or Defaulter Override triggered. |

---

## 📁 Repository Structure

```
├── backend/
│   ├── main.py                     # FastAPI REST API & LangGraph runner
│   ├── agent_state.py              # LangGraph TypedDict LoanApplicationState
│   ├── calculators.py              # EMI, FOIR, and RBI LTV calculators
│   ├── roi_engine.py               # Official CBoI 01.07.2026 RBLR rate engine
│   ├── msme_scoring_engine.py      # Form MSE 1 & II, CBI 1-10 grades, Hurdle Rate
│   ├── report_generator.py         # Deterministic 6-section appraisal memos
│   ├── agents/
│   │   └── agent_nodes.py          # 10 autonomous LangGraph agent nodes
│   ├── rag/
│   │   ├── ingest.py               # PostgreSQL pgvector + tsvector indexing
│   │   └── retriever.py            # GAHR-MSR Hybrid Search & Cross-Encoder
│   └── test_system_e2e_verification.py # Automated 100% verification test suite
├── frontend/
│   ├── app.py                      # Streamlit UI with 1-Click Demo Loaders & Analytics
│   ├── utils.py                    # EasyOCR extraction & Word (.docx) generator
│   └── Logo.png                    # Central Bank of India official logo
├── ml_pipeline/
│   └── models/                     # Trained XGBoost model, label encoders, feature schema
├── PROJECT_SUBMISSION_REPORT.md    # Comprehensive technical submission report
├── requirements.txt                # Production dependencies
├── .env.example                    # Environment configuration template
└── README.md                       # System documentation
```

---

## ⚙️ Installation & Quickstart

### 1. Prerequisites
- **Python**: Version 3.11, 3.12, or 3.13
- **PostgreSQL**: 16+ with `pgvector` extension installed
- **Google Gemini API Key**

### 2. Clone the Repository
```bash
git clone https://github.com/sai-kira/Intelligent-Loan-Appraisal-System.git
cd Intelligent-Loan-Appraisal-System
```

### 3. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure `.env`
Create a `.env` file in the root directory (based on `.env.example`):
```env
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/CentralBankDB
CREDIT_MANAGER_PASSCODE=CBOI_ADMIN
```

### 5. Ingest Regulatory Policy Knowledgebase (RAG)
```bash
python backend/rag/ingest.py
```

### 6. Run the Application Services

**Start the FastAPI Backend Service:**
```bash
python backend/main.py
```
*Backend runs at `http://127.0.0.1:8000` (Swagger UI at `/docs`)*

**Start the Streamlit User & Credit Manager Portal (in a new terminal):**
```bash
streamlit run frontend/app.py --server.port 8501
```
*Frontend runs at `http://localhost:8501`*

---

## 🧪 Running the Verification Test Suite

Run the full automated test suite verifying all 10 agents, 10 CBI risk grades, Hurdle Rate boundaries, and RBLR interest rates:
```bash
python -X utf8 backend/test_system_e2e_verification.py
```

---

## 👥 Authentication & Roles
- **Applicant Portal**: Public submission and real-time tracking via Tracking ID.
- **Credit Manager Portal**: Protected via passcode `CBOI_ADMIN` for HITL approvals, portfolio analytics, and override audit logs.

---
*Developed for the Central Bank of India Automated Credit Underwriting & Institutional Risk Governance Initiative.*
