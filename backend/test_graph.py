import asyncio
from workflow import build_workflow
from langgraph.checkpoint.memory import MemorySaver
import uuid

async def run_test():
    checkpointer = MemorySaver()
    workflow = build_workflow()
    graph = workflow.compile(checkpointer=checkpointer)
    
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "messages": [],
        "applicant_data": {
            "name": "John Doe",
            "loan_amount": 5_000_000,
            "interest_rate": 8.5,
            "tenure_months": 240,
            "gross_monthly_income": 100000,
            "existing_emi": 20000,
            "property_value": 7_000_000,
            "loan_type": "Home Loan",
            "credit_score": 750
        },
        "extracted_documents": [],
        "kyc_status": "PENDING",
        "bank_verification_status": "PENDING",
        "financial_metrics": {},
        "risk_score": {},
        "applicable_policies": [],
        "decision_outcome": "PENDING",
        "manager_comments": "",
        "appraisal_memo_url": "",
        "current_agent": "START"
    }
    
    print("Starting Application Process...")
    async for event in graph.astream(initial_state, config=config):
        for k, v in event.items():
            print(f"--- Agent Completed: {k} ---")
            
    # Print the state at interrupt
    state = graph.get_state(config)
    print("\n[INTERRUPT] Waiting for manager approval...")
    print(f"Current Decision: {state.values.get('decision_outcome')}")
    
    print("\nSimulating Manager Approval...")
    from langgraph.types import Command
    async for event in graph.astream(Command(resume="APPROVED"), config=config):
        for k, v in event.items():
            print(f"--- Agent Completed: {k} ---")
            
    final_state = graph.get_state(config)
    print("\n[PROCESS COMPLETE]")
    print(f"Final Decision: {final_state.values.get('decision_outcome')}")
    print(f"Manager Comments: {final_state.values.get('manager_comments')}")
    
if __name__ == "__main__":
    asyncio.run(run_test())
