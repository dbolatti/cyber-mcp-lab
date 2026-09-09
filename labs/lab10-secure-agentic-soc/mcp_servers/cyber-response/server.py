from mcp.server import MCPServer
import data as resp_data

server = MCPServer("cyber-response")

@server.tool()
def create_proposal(evidence_refs: list, action_type: str, target: str, reason: str) -> dict:
    """Create a new proposal."""
    return resp_data.create_proposal(evidence_refs, action_type, target, reason)

@server.tool()
def approve_proposal(proposal_id: str, approval_code: str) -> dict:
    """Approve a proposal with the given approval code."""
    return resp_data.approve_proposal(proposal_id, approval_code)

@server.tool()
def execute_action(proposal_id: str) -> dict:
    """Execute an approved proposal."""
    return resp_data.execute_action(proposal_id)

@server.tool()
def verify_action(proposal_id: str) -> dict:
    """Verify that the action has been effected."""
    return resp_data.verify_action(proposal_id)

@server.tool()
def get_security_state() -> dict:
    """Get the current simulated security state."""
    return resp_data.get_security_state()

# Resources
@server.resource("response://proposals")
def proposals_resource() -> dict:
    """Resource providing list of proposal IDs."""
    return resp_data._proposals_resource()

@server.resource("response://proposals/{proposal_id}")
def proposal_resource(proposal_id: str) -> dict:
    """Resource providing a specific proposal."""
    return resp_data._proposal_resource(proposal_id)

@server.resource("response://state")
def security_state_resource() -> dict:
    """Resource providing the security state."""
    return resp_data._security_state_resource()

if __name__ == "__main__":
    server.run()