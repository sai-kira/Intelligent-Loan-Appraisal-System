import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, START, END
from agent_state import LoanApplicationState
from agents.agent_nodes import (
    customer_agent, document_agent, kyc_agent, validation_agent,
    financial_analysis_agent, ml_risk_agent, policy_retrieval_agent,
    compliance_agent, decision_agent, report_writing_agent,
    manager_approval_agent, audit_agent
)

def build_workflow():
    workflow = StateGraph(LoanApplicationState)
    
    # Add Nodes
    workflow.add_node("customer_agent", customer_agent)
    workflow.add_node("document_agent", document_agent)
    workflow.add_node("kyc_agent", kyc_agent)
    workflow.add_node("validation_agent", validation_agent)
    workflow.add_node("financial_analysis_agent", financial_analysis_agent)
    workflow.add_node("ml_risk_agent", ml_risk_agent)
    workflow.add_node("policy_retrieval_agent", policy_retrieval_agent)
    workflow.add_node("compliance_agent", compliance_agent)
    workflow.add_node("decision_agent", decision_agent)
    workflow.add_node("report_writing_agent", report_writing_agent)
    workflow.add_node("manager_approval_agent", manager_approval_agent)
    workflow.add_node("audit_agent", audit_agent)

    # Add Edges
    workflow.add_edge(START, "customer_agent")
    
    # The nodes use Command(goto=...) for dynamic routing, but we can also explicitly add edges if needed.
    # In LangGraph v0.1+, if a node returns Command(goto="node"), the edge is implicit.
    # For safety, let's add explicit fallback edges or trust the goto. 
    # Actually, if we use Command(goto=...), we don't need to add_edge for those transitions.
    # We will just add the endpoints to END.
    workflow.add_edge("audit_agent", END)
    
    return workflow

# We compile the graph in main.py so we can attach the checkpointer there.
