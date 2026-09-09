import os
import time
import hmac
from typing import Dict, List, Optional, Any, Set
from copy import deepcopy

# In-memory storage for proposals and security state
_proposals: Dict[str, dict] = {}
_blocked_ips: Set[str] = set()
_isolated_hosts: Set[str] = set()
_disabled_accounts: Set[str] = set()

# Environment variable for approval code
APPROVAL_CODE_ENV = "CYBERLAB_APPROVAL_CODE"

def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _get_approval_code() -> Optional[str]:
    """Get the approval code from environment."""
    return os.environ.get(APPROVAL_CODE_ENV)

def create_proposal(evidence_refs: List[dict], action_type: str, target: str, reason: str) -> dict:
    """Create a new proposal with deterministic target validation."""
    # Validate action_type
    allowed_actions = {"block_ip", "isolate_host", "disable_account"}
    if action_type not in allowed_actions:
        return {
            "success": False,
            "error": {
                "code": "INVALID_ACTION",
                "message": f"Action type must be one of {allowed_actions}"
            }
        }

    # Validate action/target combination per dataset
    valid_combinations = {
        "block_ip": "185.220.101.5",
        "isolate_host": "workstation-01",
        "disable_account": "jsmith"
    }
    expected_target = valid_combinations.get(action_type)
    if expected_target is None or target != expected_target:
        return {
            "success": False,
            "error": {
                "code": "INVALID_TARGET_FOR_ACTION",
                "message": f"Target {target} is not valid for action {action_type}. Expected {expected_target}"
            }
        }

    # Generate proposal ID (deterministic not required; we keep random)
    import secrets
    proposal_id = secrets.token_urlsafe(16)

    # Store proposal
    proposal = {
        "proposal_id": proposal_id,
        "evidence_refs": deepcopy(evidence_refs),
        "action_type": action_type,
        "target": target,
        "reason": reason,
        "status": "PENDING_APPROVAL",
        "created_at": _now_iso()
    }
    _proposals[proposal_id] = proposal

    # Return a copy with metadata
    response = deepcopy(proposal)
    response["metadata"] = {
        "source": "cyber-response",
        "observed_at": response["created_at"],
        "data_version": 1,  # static version for proposal until it changes
        "retrieved_at": _now_iso()
    }
    return {"success": True, "data": response}

def approve_proposal(proposal_id: str, approval_code: str) -> dict:
    """Approve a proposal with the given approval code."""
    # 1. proposal exists
    proposal = _proposals.get(proposal_id)
    if proposal is None:
        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_PROPOSAL",
                "message": f"Proposal {proposal_id} not found"
            }
        }

    # 2. proposal status is PENDING_APPROVAL
    if proposal["status"] != "PENDING_APPROVAL":
        return {
            "success": False,
            "error": {
                "code": "INVALID_STATUS",
                "message": f"Proposal {proposal_id} is not in PENDING_APPROVAL status (current: {proposal['status']})"
            }
        }

    # 3. CYBERLAB_APPROVAL_CODE exists
    expected_code = _get_approval_code()
    if expected_code is None:
        return {
            "success": False,
            "error": {
                "code": "APPROVAL_CODE_NOT_CONFIGURED",
                "message": "Approval code not configured in environment"
            }
        }

    # 4. approval credential matches using hmac.compare_digest
    if not hmac.compare_digest(approval_code.encode(), expected_code.encode()):
        return {
            "success": False,
            "error": {
                "code": "INVALID_APPROVAL",
                "message": "Invalid approval code"
            }
        }

    # 5. transition to APPROVED
    proposal["status"] = "APPROVED"
    proposal["approved_at"] = _now_iso()

    # Return a copy
    response = deepcopy(proposal)
    response["metadata"] = {
        "source": "cyber-response",
        "observed_at": response["approved_at"],
        "data_version": 1,  # version increments on status change? we keep 1 for simplicity; but could increment.
        "retrieved_at": _now_iso()
    }
    return {"success": True, "data": response}

def execute_action(proposal_id: str) -> dict:
    """Execute an approved proposal."""
    # Check proposal exists
    proposal = _proposals.get(proposal_id)
    if proposal is None:
        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_PROPOSAL",
                "message": f"Proposal {proposal_id} not found"
            }
        }

    # Check status
    if proposal["status"] != "APPROVED":
        if proposal["status"] == "PENDING_APPROVAL":
            return {
                "success": False,
                "error": {
                    "code": "ACTION_NOT_APPROVED",
                    "message": f"Proposal {proposal_id} is not approved"
                }
            }
        else:  # EXECUTED or VERIFIED
            return {
                "success": False,
                "error": {
                    "code": "ALREADY_EXECUTED",
                    "message": f"Proposal {proposal_id} has already been executed"
                }
            }

    # Extract action and target from proposal (ignore any passed-in action/target)
    action_type = proposal["action_type"]
    target = proposal["target"]

    # Simulate the effect
    if action_type == "block_ip":
        _blocked_ips.add(target)
    elif action_type == "isolate_host":
        _isolated_hosts.add(target)
    elif action_type == "disable_account":
        _disabled_accounts.add(target)
    else:
        # Should not happen due to validation in create_proposal
        return {
            "success": False,
            "error": {
                "code": "INVALID_ACTION",
                "message": f"Invalid action type {action_type}"
            }
        }

    # Update proposal status
    proposal["status"] = "EXECUTED"
    proposal["executed_at"] = _now_iso()

    # Return a copy
    response = deepcopy(proposal)
    response["metadata"] = {
        "source": "cyber-response",
        "observed_at": response["executed_at"],
        "data_version": 1,
        "retrieved_at": _now_iso()
    }
    return {"success": True, "data": response}

def verify_action(proposal_id: str) -> dict:
    """Verify that the action has been effected by checking authoritative state."""
    # Check proposal exists
    proposal = _proposals.get(proposal_id)
    if proposal is None:
        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_PROPOSAL",
                "message": f"Proposal {proposal_id} not found"
            }
        }

    # Check status
    if proposal["status"] != "EXECUTED":
        return {
            "success": False,
            "error": {
                "code": "NOT_EXECUTED",
                "message": f"Proposal {proposal_id} is not in EXECUTED status (current: {proposal['status']})"
            }
        }

    action_type = proposal["action_type"]
    target = proposal["target"]

    # Check the authoritative state
    effect_present = False
    if action_type == "block_ip":
        effect_present = target in _blocked_ips
    elif action_type == "isolate_host":
        effect_present = target in _isolated_hosts
    elif action_type == "disable_account":
        effect_present = target in _disabled_accounts
    else:
        return {
            "success": False,
            "error": {
                "code": "INVALID_ACTION",
                "message": f"Invalid action type {action_type}"
            }
        }

    if effect_present:
        # Transition to VERIFIED
        proposal["status"] = "VERIFIED"
        proposal["verified_at"] = _now_iso()

        response = deepcopy(proposal)
        response["metadata"] = {
            "source": "cyber-response",
            "observed_at": response["verified_at"],
            "data_version": 1,
            "retrieved_at": _now_iso()
        }
        return {"success": True, "data": response}
    else:
        return {
            "success": False,
            "error": {
                "code": "VERIFICATION_FAILED",
                "message": f"Expected effect for {action_type} on {target} not found in security state"
            }
        }

def get_security_state() -> dict:
    """Return a read-only view of the current security state."""
    return {
        "success": True,
        "data": {
            "blocked_ips": sorted(list(_blocked_ips)),
            "isolated_hosts": sorted(list(_isolated_hosts)),
            "disabled_accounts": sorted(list(_disabled_accounts))
        }
    }

# Resources
def _proposals_resource() -> dict:
    """Resource providing list of proposal IDs."""
    proposal_ids = list(_proposals.keys())
    return {"success": True, "data": proposal_ids}

def _proposal_resource(proposal_id: str) -> dict:
    """Resource providing a specific proposal."""
    proposal = _proposals.get(proposal_id)
    if proposal is None:
        return {
            "success": False,
            "error": {
                "code": "UNKNOWN_PROPOSAL",
                "message": f"Proposal {proposal_id} not found"
            }
        }
    # Determine latest timestamp for observed_at
    timestamps = [
        proposal.get("verified_at"),
        proposal.get("executed_at"),
        proposal.get("approved_at"),
        proposal.get("created_at")
    ]
    # Filter out None and take the latest (lexicographically works for ISO timestamps)
    valid_times = [ts for ts in timestamps if ts is not None]
    observed_at = max(valid_times) if valid_times else proposal["created_at"]

    # Return a deep copy with metadata
    proposal_copy = deepcopy(proposal)
    proposal_copy["metadata"] = {
        "source": "cyber-response",
        "observed_at": observed_at,
        "data_version": 1,
        "retrieved_at": _now_iso()
    }
    return {"success": True, "data": proposal_copy}

def _security_state_resource() -> dict:
    """Resource providing the security state."""
    state = get_security_state()
    return state