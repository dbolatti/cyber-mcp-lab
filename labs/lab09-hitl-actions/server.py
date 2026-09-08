import os
import secrets
import hmac
from typing import Dict, List, Optional, Any
from mcp.server import MCPServer

server = MCPServer("CyberSecurityResponse")

# In-memory state
INCIDENTS = [
    {
        "id": "INC-001",
        "type": "brute_force",
        "severity": "high",
        "source_ip": "185.220.101.5",
        "target": "web-server-01"
    },
    {
        "id": "INC-002",
        "type": "malware",
        "severity": "critical",
        "source_ip": "10.0.5.45",
        "target": "workstation-01"
    },
    {
        "id": "INC-003",
        "type": "suspicious_account",
        "severity": "high",
        "account": "jsmith"
    }
]

# Simulated security state
blocked_ips: set = set()
assets: Dict[str, str] = {
    "web-server-01": "active",
    "db-server-01": "active",
    "workstation-01": "active"
}
accounts: Dict[str, str] = {
    "admin": "enabled",
    "jsmith": "enabled",
    "svc-backup": "enabled"
}

# Proposals storage
proposals: Dict[str, Dict[str, Any]] = {}

# Helper functions
def validate_ip(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def validate_action_target(action_type: str, target: str) -> bool:
    if action_type == "block_ip":
        return validate_ip(target)
    elif action_type == "isolate_host":
        return target in assets
    elif action_type == "disable_account":
        return target in accounts
    return False

# Structured error helper
def error_response(code: str, message: str) -> Dict[str, Any]:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }

# Tools
@server.tool()
def get_incidents() -> List[Dict[str, Any]]:
    """Returns all simulated incidents."""
    # Return copies of incident dictionaries
    return [incident.copy() for incident in INCIDENTS]

@server.tool()
def get_security_state() -> Dict[str, Any]:
    """Returns the current simulated security state."""
    return {
        "blocked_ips": list(blocked_ips),
        "assets": assets.copy(),
        "accounts": accounts.copy()
    }

@server.tool()
def propose_action(action_type: str, target: str, reason: str) -> Dict[str, Any]:
    """
    Propose a security action. Does not modify state.
    Returns a proposal with a unique ID and PENDING_APPROVAL status.
    """
    # Validate action type
    if action_type not in ["block_ip", "isolate_host", "disable_account"]:
        return error_response("INVALID_ACTION_TYPE", "Invalid action type")
    
    # Validate target for action type
    if not validate_action_target(action_type, target):
        return error_response("INVALID_TARGET_FOR_ACTION", "Invalid target for action type")
    
    # Generate proposal ID
    proposal_id = secrets.token_urlsafe(32)
    
    # Store proposal
    proposal = {
        "proposal_id": proposal_id,
        "action_type": action_type,
        "target": target,
        "reason": reason,
        "status": "PENDING_APPROVAL"
    }
    proposals[proposal_id] = proposal
    
    # Return a copy of the proposal
    return proposal.copy()

@server.tool()
def approve_action(proposal_id: str, approval_code: str) -> Dict[str, Any]:
    """
    Approve a proposed action using the environment variable approval code.
    """
    # Check if proposal exists
    if proposal_id not in proposals:
        return error_response("UNKNOWN_PROPOSAL", "Proposal not found")
    
    proposal = proposals[proposal_id]
    
    # Check if proposal is in PENDING_APPROVAL state
    if proposal["status"] != "PENDING_APPROVAL":
        return error_response("INVALID_PROPOSAL_STATE", "Proposal is not pending approval")
    
    # Check if approval code is configured
    expected_code = os.environ.get("CYBERLAB_APPROVAL_CODE")
    if expected_code is None:
        return error_response("APPROVAL_CONFIGURATION_MISSING", "Approval code not configured")
    
    # Compare using hmac.compare_digest to avoid timing attacks
    if not hmac.compare_digest(approval_code, expected_code):
        return error_response("INVALID_APPROVAL", "Invalid approval code")
    
    # Update status to APPROVED
    proposal["status"] = "APPROVED"
    
    # Return a copy of the updated proposal
    return proposal.copy()

@server.tool()
def execute_action(proposal_id: str) -> Dict[str, Any]:
    """
    Execute an approved action. Only works on APPROVED proposals.
    """
    # Check if proposal exists
    if proposal_id not in proposals:
        return error_response("UNKNOWN_PROPOSAL", "Proposal not found")
    
    proposal = proposals[proposal_id]
    
    # Check proposal status
    if proposal["status"] == "PENDING_APPROVAL":
        return error_response("ACTION_NOT_APPROVED", "Action not approved")
    elif proposal["status"] == "EXECUTED":
        return error_response("ALREADY_EXECUTED", "Action already executed")
    elif proposal["status"] != "APPROVED":
        return error_response("INVALID_PROPOSAL_STATE", "Invalid proposal state for execution")
    
    # At this point, status is APPROVED
    action_type = proposal["action_type"]
    target = proposal["target"]
    
    # Execute the action (simulated)
    if action_type == "block_ip":
        blocked_ips.add(target)
    elif action_type == "isolate_host":
        assets[target] = "isolated"
    elif action_type == "disable_account":
        accounts[target] = "disabled"
    
    # Update proposal status to EXECUTED
    proposal["status"] = "EXECUTED"
    
    # Build result with defensive copies
    result = {
        "proposal_id": proposal_id,
        "action_type": action_type,
        "target": target,
        "status": "EXECUTED"
    }
    
    # Include relevant state change (copies)
    if action_type == "block_ip":
        result["blocked_ips"] = list(blocked_ips)
    elif action_type == "isolate_host":
        result["assets"] = assets.copy()
    elif action_type == "disable_account":
        result["accounts"] = accounts.copy()
    
    return result

# Run the server
if __name__ == "__main__":
    server.run()