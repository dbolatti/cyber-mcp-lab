# Lab 07: Identity and Authorization

## Lab Objective
Build an educational MCP server demonstrating:
- identity context
- authentication vs authorization
- RBAC (Role-Based Access Control)
- scope-based authorization
- least privilege
- allow/deny decisions
- structured authorization errors

## Identity
In this lab, we use **simulated identities**. An identity is a string (e.g., "alice", "bob", "carol") that represents a user or system. The identity is passed as a parameter to each tool.

**Important**: Passing an identity name to a tool is **NOT real authentication**. It is a simulated identity assertion for educational purposes. A malicious caller could claim to be any identity (e.g., "alice") without proof. This vulnerability is intentional and will motivate later work with real authenticated identity.

## Authentication vs Authorization
- **Authentication (AuthN)**: Verifying who you are. Not implemented in this lab (we simulate identities).
- **Authorization (AuthZ)**: Determining what you are allowed to do. This lab focuses on authorization mechanics.

## RBAC and Scopes
- **RBAC**: Roles are assigned to identities. Each role has a set of permissions.
- **Scopes**: Fine-grained permissions (e.g., `assets:read`, `events:read`, `summary:read`). Scopes are the actual units of authorization.

## Least Privilege
Each identity is granted only the scopes necessary for their role:
- `alice` (analyst): `events:read`, `assets:read`
- `bob` (viewer): `assets:read`
- `carol` (senior_analyst): `events:read`, `assets:read`, `summary:read`

## Default Deny
Authorization follows a default-deny policy:
- If an identity is unknown, access is denied.
- If an identity lacks the required scope, access is denied.
- Only explicit grants allow access.

## Server-Side Enforcement
Authorization decisions are made **server-side** in the MCP server. The LLM (or caller) cannot influence the decision beyond providing the identity and parameters. The server checks the identity's scopes before returning any protected data.

## Why Authorization Must Not Be Delegated to the LLM
The LLM is not a trusted security boundary. Delegating authorization to the LLM would allow prompt injection or manipulation to bypass access controls. By keeping authorization on the server, we ensure that decisions are based on verified identity and scope data.

## Structured Denial
Authorization errors return a consistent structure:
```json
{
  "authorized": false,
  "error": {
    "code": "ACCESS_DENIED",
    "identity": "<identity_name>",
    "required_scope": "<required_scope>",
    "message": "Identity does not have the required scope"
  }
}
```
For unknown identities, the same structure is used with the identity name provided.

## Architecture
- **MCP Server**: Built with the MCP Python SDK.
- **Tools**: Three read-only tools:
  1. `get_assets`: Requires `assets:read` scope.
  2. `search_events`: Requires `events:read` scope, optional severity filter.
  3. `get_security_summary`: Requires `summary:read` scope.
- **Data**: Simulated assets and security events.
- **Helpers**: Internal functions `get_identity` and `authorize` (not exposed as tools).

## Expected Authorization Matrix
| Identity   | get_assets | search_events | get_security_summary |
|------------|------------|---------------|----------------------|
| alice      | ALLOW      | ALLOW         | DENY                 |
| bob        | ALLOW      | DENY          | DENY                 |
| carol      | ALLOW      | ALLOW         | ALLOW                |

## Setup and Validation Procedure
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Start the MCP server** (via OpenCode configuration or directly):
   ```bash
   python server.py
   ```
3. **Validate using an MCP client** (e.g., OpenCode):
   - Call `get_assets` with identity="alice" → should succeed.
   - Call `get_assets` with identity="bob" → should succeed.
   - Call `get_assets` with identity="unknown" → should deny.
   - Call `search_events` with identity="alice" → should succeed.
   - Call `search_events` with identity="bob" → should deny.
   - Call `get_security_summary` with identity="carol" → should succeed.
   - Call `get_security_summary` with identity="alice" → should deny.

## Security Limitations
- **Read-only only**: No tools modify state.
- **No real authentication**: Identities are simulated and can be spoofed.
- **No external access**: Server does not access filesystem, network, or subprocesses.
- **LLM cannot override**: Authorization is strictly server-side.

## Static Validation Performed
Before completion, we verified:
- `MCPServer` instantiated before decorators.
- No duplicate function names.
- No recursion.
- Helper functions (`get_identity`, `authorize`) are not exposed as MCP tools.
- Authorization occurs inside every tool before accessing protected data.
- Unknown identities fail closed (deny).
- Missing scopes fail closed (deny).
- No unnecessary imports.
- Structured return values for both success and error cases.
- `server.run()` is present.
- No filesystem access, subprocess, or external network access in the server code.