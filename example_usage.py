"""Example usage for Cross-App State Machine Orchestrator."""
from client import CrossAppStateMachineOrchestrator

if __name__ == "__main__":
    step = CrossAppStateMachineOrchestrator.step_workflow(
        "ENRICHING",
        "lead_qualified",
        {"company": "AlphaTech", "score": 92}
    )
    print("Transition Valid:", step["valid_transition"])
    print("New State:", step["current_state"])
    print("Action Dispatched:", step["dispatched_action"])
