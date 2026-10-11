"""Cross-App Event Trigger & State Machine Orchestrator.
100% Python Standard Library.
"""

import json
import hashlib

class CrossAppStateMachineOrchestrator:
    """Evaluates incoming webhook events and advances deterministic cross-app workflow states."""
    
    TRANSITIONS = {
        ("IDLE", "lead_captured"): ("ENRICHING", "trigger_clearbit_and_score_lead"),
        ("ENRICHING", "lead_qualified"): ("NOTIFYING_SALES", "post_slack_deal_room_alert"),
        ("NOTIFYING_SALES", "meeting_booked"): ("COMPLETED", "sync_crm_opportunity_stage")
    }
    
    @classmethod
    def step_workflow(cls, current_state: str, event_name: str, payload: dict) -> dict:
        key = (current_state.upper(), event_name.lower())
        if key not in cls.TRANSITIONS:
            return {
                "valid_transition": False,
                "previous_state": current_state,
                "current_state": current_state,
                "dispatched_action": "none",
                "message": f"No transition defined for event '{event_name}' from state '{current_state}'."
            }
            
        next_state, action = cls.TRANSITIONS[key]
        return {
            "valid_transition": True,
            "previous_state": current_state,
            "current_state": next_state,
            "dispatched_action": action,
            "context_hash": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
        }
