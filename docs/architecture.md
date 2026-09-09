# Lab 06 Architecture

## Architecture Diagram

```
                      OpenCode / LLM
                            |
                       MCP Client
                      /          \
                     /            \
            cyber-siem          cyber-ti
           search_events        check_ip
                     \            /
                      \          /
                   evidence fusion
                         |
                   LLM inference
```

## Component Description

- **OpenCode / LLM**: The OpenCode interface hosting the language model.
- **MCP Client**: The MCP client within OpenCode that connects to servers.
- **cyber-siem**: MCP server providing the `search_events` tool for SIEM data.
- **cyber-ti**: MCP server providing the `check_ip` tool for threat intelligence.
- **evidence fusion**: The process of correlating evidence from both servers.
- **LLM inference**: The language model's reasoning based on fused evidence.

## Transport

stdin/stdout (stdio) transport is used for MCP communication.

## Lab 07 – Identity and Authorization Architecture Lessons

Lab 07 highlighted critical architectural considerations for identity, authentication, and authorization in MCP systems:

1. **Authorization must be enforced server‑side**. The MCP server is the authoritative source for access control; prompt text or LLM behavior cannot override its decisions.

2. **Authentication → Verified identity → Security context → Authorization → MCP capability** is the correct flow. Each stage must be distinct and properly implemented.

3. In this lab, identity was simulated (no cryptographic authentication). The server accepted a claimed identity and mapped it to a verified identity for authorization purposes. This demonstrates that:
   - **Claimed identity** (what the agent states) may differ from **authenticated identity** (what the server validates after authentication).
   - The **authorization decision** relies on the authenticated identity, not the claimed one.
   - Without strong authentication, a malicious agent can claim any identity and gain its permissions—a limitation of the simulation, not a flaw in authorization logic.

4. The lab reinforces that:
   - Prompt‑based attempts to bypass authorization (e.g., “act as bob”) fail when the server enforces checks based on verified identity.
   - Unknown identities are rejected with a specific error (`UNKNOWN_IDENTITY`), ensuring fail‑closed behavior.
   - Authorization decisions are deterministic and based on predefined roles/permissions (`events:read`, `summary:read`).

5. **Design implication**: Production MCP implementations must integrate strong authentication (e.g., mutual TLS, JWT) to bind the claimed identity to a cryptographically verified identity before authorization is evaluated.

6. The MCP server’s authorization logic must be independent of the LLM; it should rely solely on server‑side policies and the security context derived from authentication.

## Lab 08 – Authentication and Identity Binding Architecture Lessons

Lab 08 introduced a credential‑based authentication mechanism that separates authentication from authorization, providing the following architectural insights:

1. **Authentication is prerequisite to authorization**. The server first validates the CYBERLAB_TOKEN, derives the identity, and only then evaluates access rights.

2. **Identity is bound to a credential, not to LLM‑provided claims**. Even if the LLM asserts a different identity in a prompt, the server‑side authentication mapping prevents impersonation.

3. **Default‑deny authorization** ensures that an authenticated identity possesses only the permissions explicitly granted (e.g., alice can read events, carol can read summary, bob has none).

4. **Read‑only scope limits the impact** of any potential credential leakage; the MCP server exposes no mutative capabilities.

5. **Separation of concerns**: authentication validates the credential; authorization checks the derived identity against policy. Each can be evolved independently.

These lessons reinforce that secure MCP designs must treat authentication and authorization as distinct, server‑side enforced steps, with identity never sourced from the LLM or prompt text.

## Lab 09 – High-Impact Tools, Human-in-the-Loop and Excessive Agency Architecture Lessons

Lab 09 focuses on high-impact tools requiring human-in-the-loop approval to prevent excessive agency. The architecture enforces a clear separation between proposal and execution.

### Architecture
- **MCP Server**: CyberSecurityResponse
- **OpenCode MCP Name**: cyber-response
- **Tools**:
  - `get_incidents`: Retrieves simulated security incidents.
  - `get_security_state`: Returns current simulated security state.
  - `propose_action`: Creates a proposal for a high-impact action (block_ip, isolate_host, disable_account) requiring approval.
  - `approve_action`: Approves a pending proposal using an approval code.
  - `execute_action`: Executes an approved proposal (only if approved).
- **Data Flow**: OBSERVE (get_incidents/get_security_state) -> PROPOSE (propose_action) -> APPROVE (approve_action) -> EXECUTE (execute_action) -> VERIFY (get_incidents/get_security_state)
- **State Machine**:
  - PENDING_APPROVAL: After proposal, awaiting approval.
  - APPROVED: After successful approval.
  - EXECUTED: After execution.
- **Supported Simulated Actions**: block_ip, isolate_host, disable_account (all effects are simulated and in-memory).

### Security Design Principles
- LLM intent is not human approval.
- Prompt text must not be sufficient to approve an action.
- Approval is enforced server-side.
- Execution is allowed only for approved proposals.
- `execute_action` receives only `proposal_id`.
- Action type and target come from the stored proposal.
- Duplicate execution is rejected (returns ALREADY_EXECUTED).
- All effects are simulated and in-memory.
- No real firewall, operating-system, account, filesystem, subprocess, or network actions exist.

### Validation Status
- Static validation passed: Python compilation, Python import, MCP connectivity.
- Functional security tests passed and validated.

## Lab 10 – Secure Agentic SOC Architecture Lessons

Lab 10 demonstrates a secure multi-MCP agentic Security Operations Center (SOC) composed of three MCP servers: cyber-soc, cyber-ti, and cyber-response. The architecture highlights trust boundaries and the role of OpenCode/LLM as an orchestrator rather than a security enforcement point.

### Architecture
- **MCP Servers**:
  - `cyber-soc`: Provides SOC evidence ingestion and initial triage (e.g., `get_incidents`, `add_evidence`).
  - `cyber-ti`: Offers threat intelligence lookup (e.g., `check_ip`, `check_hash`).
  - `cyber-response`: Owns the authoritative proposal finite‑state machine (FSM) and simulated response state; exposes `propose_action`, `approve_action`, `execute_action`, and `get_proposal_state`.
- **OpenCode / LLM**: Acts as the orchestrator that sequences observations, correlates evidence, generates proposals, and requests human approval, but does not enforce security‑critical transitions.
- **Data Flow**: 
  1. Observe – retrieve incidents from cyber-soc and enrich with cyber-ti.
  2. Correlate & Reason – LLM synthesizes evidence and drafts a proposal via cyber-response `propose_action`.
  3. Approve – Human reviews and supplies approval code to cyber-response `approve_action`.
  4. Execute – Cyber-response `execute_action` runs the approved action.
  5. Verify – Independent verification by re‑querying cyber-soc and cyber-ti to confirm effect.
- **Trust Boundaries**: 
  - Each MCP server enforces its own access controls and validates inputs server‑side.
  - The LLM never directly modifies state; it only influences proposals through trusted tool calls.
  - Provenance between independent MCP servers is not cryptographically attested in the current lab; trust relies on server‑side validation and audit logs.

### Security Design Principles
- Security‑critical state transitions (e.g., moving from PENDING_APPROVAL to EXECUTED) are enforced solely by the cyber-response MCP server.
- Human natural‑language intent is not sufficient for authorization; approval requires a server‑validated code.
- Action details (type, target) are retrieved from the authoritative proposal state stored in cyber-response, not from LLM‑provided parameters.
- Execution success and independently verified effect are distinct; verification must query separate evidence sources.
- The lab demonstrated resilience against replay, fabricated proposal IDs, pre‑approval execution, invalid credentials, and target tampering.
- Secure individual components do not guarantee secure composition; cross‑MCP trust and attestation are needed for stronger guarantees.
- Agent self‑review or internal validation does not replace independent verification by separate MCP servers or human review.
