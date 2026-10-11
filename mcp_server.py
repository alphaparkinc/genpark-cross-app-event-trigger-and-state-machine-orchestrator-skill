"""MCP server for Cross-App State Machine Orchestrator."""
import sys
import json
from client import CrossAppStateMachineOrchestrator

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "advance_workflow_state",
                "description": "Advances cross-app state machine based on incoming event trigger",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "current_state": {"type": "string"},
                        "event_name": {"type": "string"},
                        "payload": {"type": "object"}
                    },
                    "required": ["current_state", "event_name", "payload"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "advance_workflow_state":
            args = params.get("arguments", {})
            res = CrossAppStateMachineOrchestrator.step_workflow(
                args.get("current_state", ""),
                args.get("event_name", ""),
                args.get("payload", {})
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
