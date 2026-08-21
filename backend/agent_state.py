from typing import TypedDict, Dict, Any, List, Annotated, Optional
import operator
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class LoanApplicationState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    applicant_data: Dict[str, Any]
    extracted_documents: Annotated[List[Dict[str, Any]], operator.add]
    kyc_status: str
    bank_verification_status: str
    financial_metrics: Dict[str, Any]
    risk_score: Dict[str, Any]
    applicable_policies: Annotated[List[str], operator.add]
    decision_outcome: Optional[str]
    appraisal_memo_url: Optional[str]
    detailed_report: Optional[str]
    short_report: Optional[str]
    manager_comments: Optional[str]
    final_decision: Optional[str]
    
    # Adding specific fields for our mock process
    current_agent: str
    
    # Tracking agent decisions for explainability
    agent_logs: Annotated[List[Dict[str, Any]], operator.add]
    real_name: Optional[str]
    msme_scorecard: Optional[Dict[str, Any]]
    corporate_financial_intelligence: Optional[Dict[str, Any]]
