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