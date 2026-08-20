from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
import uvicorn
import uuid
import psycopg
import json
from psycopg_pool import ConnectionPool

from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command
from workflow import build_workflow

DB_URL = "postgresql://postgres:1424@localhost:5432/CentralBankDB"
pool = ConnectionPool(conninfo=DB_URL, max_size=20)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup Checkpointer DB Tables
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        PostgresSaver(conn).setup()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS applications_history (
                thread_id TEXT PRIMARY KEY,
                applicant_name TEXT,
                loan_amount REAL,
                risk_category TEXT,
                decision TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                detailed_report TEXT,
                short_report TEXT
            );
            ALTER TABLE applications_history ADD COLUMN IF NOT EXISTS application_data JSONB;
            ALTER TABLE applications_history ADD COLUMN IF NOT EXISTS manager_justification TEXT;
        """)
    yield
    pool.close()

app = FastAPI(title="CBoI Intelligent Loan Appraisal API", version="2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

workflow = build_workflow()

class ApplicationRequest(BaseModel):
    name: str
    age: int = Field(..., gt=17)
    gender: str
    marital_status: str
    category: str
    occupation: str
    gross_monthly_income: float = Field(..., ge=0)
    net_monthly_income: float = Field(..., ge=0)
    total_assets: float = Field(..., ge=0)
    avg_credit_balance_6m: float = Field(..., ge=0)
    existing_emi: float = Field(..., ge=0)
    active_lines: int = Field(..., ge=0)
    inquiries_6m: int = Field(..., ge=0)
    credit_score: int = Field(..., ge=300, le=900)
    loan_amount: float = Field(..., gt=0)
    interest_rate: Optional[float] = 0.0
    tenure_months: int = Field(..., gt=0)
    loan_type: str
    property_value: float = Field(..., ge=0)
    security_type: str
    
    # Optional MSME Parameters (Form MSE 1 & Form MSE II)
    current_ratio: Optional[float] = 1.33
    debt_equity_ratio: Optional[float] = 2.0
    sales_growth_rate: Optional[float] = 15.0
    pat_margin: Optional[float] = 10.0
    sanction_compliance: Optional[str] = "Compliant"
    stock_statement_status: Optional[str] = "Timely"
    debt_servicing_history: Optional[str] = "Within 1 month"
    inventory_compliance: Optional[str] = "Fair Compliance"
    bills_culture: Optional[bool] = True
    bill_payment_record: Optional[str] = "Prompt"
    review_documents_timely: Optional[bool] = True
    lc_bg_status: Optional[str] = "Prompt / No Facility"
    ancillary_relationship: Optional[str] = "Substantial"
    
    projected_sales_growth: Optional[float] = 15.0
    projected_pat_margin: Optional[float] = 10.0
    projected_der: Optional[float] = 2.0
    inputs_access: Optional[str] = "Locally Available / Tied up"
    market_access: Optional[str] = "Locally Available / Tied up"
    promoter_experience: Optional[str] = "Qualified and Experienced"
    bank_relationship: Optional[str] = "Existing Customer"
    premises_type: Optional[str] = "Owned"
    collateral_coverage: Optional[str] = "Covered under CGTMSE Scheme"
    cgtmse_covered: Optional[bool] = False

class ApprovalRequest(BaseModel):
    decision: str

class OverrideRequest(BaseModel):
    decision: str
    justification: str


def run_agent_workflow(initial_state: dict, config: dict, thread_id: str):
    checkpointer = PostgresSaver(pool)
    graph = workflow.compile(checkpointer=checkpointer)
    # We must use sync stream because psycopg_pool is sync.
    for event in graph.stream(initial_state, config=config):
        for k, v in event.items():
            print(f"Agent {k} finished executing.")
            
    # Once it hits the interrupt (manager_approval_agent), we update the DB status
    final_state = graph.get_state(config)
    if final_state and final_state.next and final_state.next[0] == "manager_approval_agent":
        risk_score = final_state.values.get("risk_score", {})
        detailed_report = final_state.values.get("detailed_report", "")
        short_report = final_state.values.get("short_report", "")
        applicant_data = final_state.values.get("applicant_data", {})
        import json
        with psycopg.connect(DB_URL, autocommit=True) as conn:
            conn.execute("""
                UPDATE applications_history 
                SET decision = 'WAITING_FOR_MANAGER', risk_category = %s, detailed_report = %s, short_report = %s, application_data = %s
                WHERE thread_id = %s
            """, (risk_score.get("risk_category", "Unknown"), detailed_report, short_report, json.dumps(applicant_data), thread_id))

@app.get("/")
def read_root():
    return {"message": "Welcome to the Agentic Loan Appraisal API"}

@app.post("/apply")
async def start_loan_application(req: ApplicationRequest, background_tasks: BackgroundTasks):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "messages": [],
        "applicant_data": req.model_dump(),
        "extracted_documents": [],
        "kyc_status": "PENDING",
        "bank_verification_status": "PENDING",
        "financial_metrics": {},
        "risk_score": {},
        "applicable_policies": [],
        "decision_outcome": "PENDING",
        "manager_comments": "",
        "appraisal_memo_url": "",
        "msme_scorecard": None
    }
    
    # Store initial record
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        conn.execute("""
            INSERT INTO applications_history (thread_id, applicant_name, loan_amount, risk_category, decision, application_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (thread_id, req.name, req.loan_amount, "PENDING", "PROCESSING", json.dumps(req.model_dump())))
    
    background_tasks.add_task(run_agent_workflow, initial_state, config, thread_id)
    return {"thread_id": thread_id, "status": "PROCESSING"}

@app.get("/pending")
async def get_pending():
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT thread_id, applicant_name, loan_amount, risk_category FROM applications_history WHERE decision = 'WAITING_FOR_MANAGER' ORDER BY created_at DESC")
            records = cur.fetchall()
    return [{"thread_id": r[0], "applicant_name": r[1], "loan_amount": r[2], "risk_category": r[3]} for r in records]

@app.get("/status/{thread_id}")
async def get_status(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    
    checkpointer = PostgresSaver(pool)
    graph = workflow.compile(checkpointer=checkpointer)
    state = graph.get_state(config)
        
    if not state or not state.values:
        return {"status": "INITIALIZING"}
        
    if not state.next:
        current_status = "COMPLETED"
    else:
        is_waiting = state.next[0] == "manager_approval_agent"
        current_status = "WAITING_FOR_MANAGER" if is_waiting else "PROCESSING"
    
    return {
        "status": current_status,
        "financial_metrics": state.values.get("financial_metrics"),
        "risk_score": state.values.get("risk_score"),
        "applicable_policies": state.values.get("applicable_policies"),
        "agent_logs": state.values.get("agent_logs", []),
        "decision_outcome": state.values.get("decision_outcome"),
        "memo_url": state.values.get("appraisal_memo_url"),
        "detailed_report": state.values.get("detailed_report"),
        "short_report": state.values.get("short_report")
    }

@app.post("/approve/{thread_id}")
async def approve_loan(thread_id: str, req: ApprovalRequest):
    config = {"configurable": {"thread_id": thread_id}}
    
    checkpointer = PostgresSaver(pool)
    graph = workflow.compile(checkpointer=checkpointer)
    state = graph.get_state(config)
    if not state:
        raise HTTPException(status_code=404, detail="Application thread not found")
        
    for event in graph.stream(Command(resume=req.decision), config=config):
        for k, v in event.items():
            print(f"Agent {k} finished executing.")
            
    final_state = graph.get_state(config)
    
    # Save to history DB
    applicant_data = final_state.values.get("applicant_data", {})
    risk_score = final_state.values.get("risk_score", {})
    decision = final_state.values.get("decision_outcome", "Unknown")
    name = final_state.values.get("real_name", applicant_data.get("name", "Unknown"))
    
    detailed_report = final_state.values.get("detailed_report", "")
    short_report = final_state.values.get("short_report", "")
    
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        conn.execute("""
            INSERT INTO applications_history (thread_id, applicant_name, loan_amount, risk_category, decision, detailed_report, short_report, application_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (thread_id) DO UPDATE SET 
                decision = EXCLUDED.decision,
                detailed_report = EXCLUDED.detailed_report,
                short_report = EXCLUDED.short_report,
                application_data = EXCLUDED.application_data
        """, (thread_id, name, applicant_data.get("loan_amount", 0), risk_score.get("risk_category", "Unknown"), decision, detailed_report, short_report, json.dumps(applicant_data)))
        
    return {
        "thread_id": thread_id,
        "status": "COMPLETED",
        "final_decision": decision,
        "manager_comments": final_state.values.get("manager_comments")
    }

@app.post("/override/{thread_id}")
async def override_decision(thread_id: str, req: OverrideRequest):
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        conn.execute("""
            UPDATE applications_history 
            SET decision = %s, manager_justification = %s 
            WHERE thread_id = %s
        """, (f"{req.decision} (Overridden)", req.justification, thread_id))
    return {"status": "COMPLETED", "final_decision": f"{req.decision} (Overridden)"}

@app.get("/history")
async def get_history():
    with psycopg.connect(DB_URL, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT thread_id, applicant_name, loan_amount, risk_category, decision, created_at, detailed_report, short_report, application_data, manager_justification FROM applications_history ORDER BY created_at DESC")
            records = cur.fetchall()
            
    history = []
    for r in records:
        history.append({
            "thread_id": r[0],
            "applicant_name": r[1],
            "loan_amount": r[2],
            "risk_category": r[3],
            "decision": r[4],
            "created_at": r[5].isoformat() if r[5] else None,
            "detailed_report": r[6],
            "short_report": r[7],
            "application_data": r[8] if r[8] else {},
            "manager_justification": r[9]
        })
    return history

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
