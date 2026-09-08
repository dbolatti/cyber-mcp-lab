# Lab 09: High-Impact Tools, Human-in-the-Loop and Excessive Agency

Status: Completed and validated

## Objective
This lab studies security controls for MCP agents capable of high-impact actions, focusing on Human-in-the-Loop, excessive agency, server-side enforcement, approval binding, and state-machine enforcement.

## Architecture
```
OBSERVE -> PROPOSE -> APPROVE -> EXECUTE -> VERIFY
```
MCP server: CyberSecurityResponse  
OpenCode MCP: cyber-response  
All actions are simulated and in-memory.

## MCP Tools
- get_incidents
- get_security_state
- propose_action
- approve_action
- execute_action

Supported actions:
- block_ip
- isolate_host
- disable_account

## State Machine
PENDING_APPROVAL -> APPROVED -> EXECUTED  
Direct PENDING_APPROVAL -> EXECUTED transition is rejected.

## Functional Security Validation
Ten tests passed:
1. Proposal creation -> PENDING_APPROVAL
2. Execution without approval -> ACTION_NOT_APPROVED
3. Prompt-based approval bypass -> rejected
4. Wrong approval code -> INVALID_APPROVAL
5. Valid approval -> APPROVED
6. Approved execution -> EXECUTED
7. Independent verification with get_security_state
8. Duplicate execution -> ALREADY_EXECUTED
9. Fabricated proposal_id -> UNKNOWN_PROPOSAL
10. Attempted modification of an approved action/target cannot change the authoritative server-side proposal

## Security Conclusions
- LLM intent is not authorization.
- Natural-language claims cannot override server-side state.
- Approval is bound to the stored proposal.
- execute_action receives only proposal_id.
- action_type and target are retrieved from authoritative server-side state.
- Duplicate execution is rejected.
- Execution should be independently verified.
- Deterministic server-side controls constrain non-deterministic agent behavior.

## Educational Limitation
CYBERLAB_APPROVAL_CODE is an educational HITL mechanism and not production-grade out-of-band approval because the approval credential still travels through an MCP Tool argument controlled by the agent.  
The lab performs no real firewall, OS, account, filesystem, subprocess, or network modifications.