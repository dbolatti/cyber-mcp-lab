# Learning Notebook - CyberSecurity MCP Lab

## Conceptual Learning
- **MCP Host**: The application (e.g., OpenCode) that manages connections to MCP servers.
- **MCP Client**: The component within the host that communicates with the server using the MCP protocol.
- **MCP Server**: A service exposing MCP primitives (tools, resources, prompts).
- **Tool**: A callable function that performs an action (e.g., check_ip).
- **Resource**: A read-only piece of data identified by a URI (e.g., security://assets).
- **Prompt**: A pre‑defined template or guidance that can be parameterized (e.g., investigate_ioc).
- **Tool/Function Calling vs MCP**: Traditional function calling is direct; MCP provides a standardized protocol for discovery and invocation across processes/languages.
- **stdio transport**: The default communication mechanism used by the Lab 01 server (message‑based over standard input/output).
- **External API wrapping**: An MCP Server can wrap a REST API (e.g., AbuseIPDB in Lab 02) to provide tool access.
- **Multiple tools**: A single MCP Server can expose multiple tools, enabling the LLM to select the appropriate tool for a task.
- **Deterministic logic**: For learning and simulation, tools can use local deterministic logic instead of external APIs.

## Implementation Learning
- **Lab 01**: 
  - Initial implementation incorrectly mixed MCP low‑level Server API with high‑level decorator API.
  - Corrected by using `MCPServer` from `mcp.server` and applying decorators to its instance.
  - Each lab is an independent OpenCode workspace with its own `.venv`, `requirements.txt`, and `opencode.json`.
- **Lab 02**:
  - Integrated external Threat Intelligence API (AbuseIPDB) via HTTPS.
  - Implemented environment variable loading for API keys (using `.env`).
  - Added input validation, timeout handling, sanitized error messages, and response normalization.
  - Real API call pending API key configuration.
- **Lab 03**:
     - Implemented `CyberSecurityMultiTool` MCP Server exposing three tools: `check_ip`, `check_hash`, and `analyze_log`.
     - Used local deterministic logic and simulated data.
     - Demonstrated tool selection by the LLM/agent.
     - OpenCode configuration corrected for version 1.18.27 format.
     - Validated reproducibility: successfully cloned/pulled repository and recreated local .venv on a different computer.
     - MCP server correctly exposed the three tools.
     - OpenCode using Nemotron 3 Super selected appropriate tools for IP reputation, malware hash, and SSH log analysis requests.
     - A deliberately ambiguous prompt did not trigger a new MCP tool invocation because the result was already present in conversation context, showing that tool availability does not imply invocation and that LLMs may answer from existing context.
     - This demonstrates distinctions between tool-derived evidence, conversation context, and LLM-generated inference.
     - Future research topics: provenance, freshness, context contamination, auditability of agent decisions, evidence versus inference.
- **Lab 04**:
     - OpenCode successfully consumed MCP Resources using `read_mcp_resource`.
     - Static Resources implemented: `security://assets` and `security://events/recent`.
     - Resource Template implemented: `security://assets/{asset_id}`.
     - Runtime-generated Resource added: `security://runtime/session`.
     - `security://runtime/session` generates a UUID at runtime, proving that an MCP Resource can expose dynamically generated information.
     - Experimental observation:
         * First explicit MCP read: `read_mcp_resource` invoked, a runtime UUID returned.
         * Repeating the same request: `read_mcp_resource` NOT invoked, previous UUID reused from conversation context.
         * Explicitly requiring a fresh MCP read: `read_mcp_resource` invoked again, a different UUID returned.
     - Conceptual conclusion: Dynamic Resource does not imply Fresh Read.
     - Agent responses may originate from: a fresh MCP Resource read, previous conversation context, or LLM inference.
     - Security implications: freshness of operational security data, provenance of evidence, context reuse, stale security information, auditability of MCP interactions.
     - Relates to Lab 03: Tool availability does not imply Tool invocation. Resource availability does not imply Resource reading.
- **Lab 05**:
     - MCP server providing a controlled read-only abstraction layer over a simulated SIEM dataset.
     - Resources: `security://siem/events/recent` (recent events) and `security://siem/events/{event_id}` (specific event by ID).
     - Tools: `search_events` (query events with filters) and `get_security_summary` (calculated summary of event severities and counts).
     - Important design decisions:
         * One central SIEM dataset is shared by Resources and Tools.
         * Read-only interface; no remediation actions.
         * No direct SIEM access by the LLM; all interaction via MCP.
         * No arbitrary query language; only defined search_events tool.
         * No shell execution.
         * Deterministic security summary calculated in Python.
         * Severity normalization and controlled validation.
     - AI-assisted development findings:
         1. Function-name collision: internal function and MCP Tool both named `get_security_summary`, causing unintended recursion.
            Corrected by renaming internal function to `calculate_security_summary()` and keeping MCP Tool as `get_security_summary()`.
         2. Initialization-order defect: `@server.tool()` decorator applied before `server = MCPServer("CyberSecuritySIEM")` was defined, causing NameError.
            Corrected by moving decorator after server instantiation.
         3. Removal of unnecessary HTTP/ASGI imports and `stdio_server` usage in favor of the validated `MCPServer + server.run()` pattern used across the project.
     - Validation workflow for future MCP Labs:
         1. AI-assisted implementation
         2. Static review by the coding agent
         3. Human code review
         4. Python syntax/compilation check: `python -m py_compile server.py`
         5. Module import test: `python -c "import server; print('Import OK')"`
         6. MCP discovery/connectivity test
         7. Functional Tool/Resource tests
         8. Documentation update
         9. Human review before Git commit
     - Note: Compilation success does not prove runtime correctness.
           Import success does not prove MCP functional correctness.
           MCP connectivity does not prove every Tool or Resource behaves correctly.
 
## OpenCode/AI-assisted Development Observations
- Initial OpenCode-generated code often mixed low-level and high-level MCP APIs; more explicit technical prompts reduced this error.
- OpenCode sometimes generated incorrect MCP JSON format; configuration must match the installed OpenCode version (e.g., 1.18.27).
- Windows PowerShell requires explicit handling; Bash-style commands (e.g., `mkdir -p`) cause failures and must be replaced with PowerShell-native equivalents (e.g., `New-Item`).
- Each lab is an independent OpenCode workspace, requiring the user to launch OpenCode from within the lab directory.
- The repository structure is a monorepo of independent learning labs, allowing parallel experimentation.

## Security Observations
- Secrets (e.g., API keys) must remain outside version control using `.env` files and never committed to Git.
- Raw internal exceptions should not be exposed to the LLM; sanitized error messages are returned.
- Tool descriptions and contracts affect tool selection by the model; accurate and concise descriptions improve correctness.
- Input validation and response normalization prevent injection attacks and ensure safe handling of external data.
- Each lab builds on previous lessons to progressively introduce security considerations, such as secret management and error handling.

These notes accumulate chronologically as we progress through the labs.

## Lab 06 - Multi-MCP

### Architecture
```
OpenCode / LLM
           |
        MCP Client
       /          \
      /            \
 cyber-siem      cyber-ti
search_events    check_ip
      \            /
       \          /
    evidence fusion
           |
     LLM inference
```

### Functional Experiments and Findings

1. Threat Intelligence selection:
   Prompt requested reputation for 185.220.101.5.
   The agent autonomously selected:
   cyber-ti -> check_ip.
   Result: malicious, confidence 0.95.

2. SIEM selection:
   Prompt requested SIEM events involving 185.220.101.5.
   The agent autonomously selected:
   cyber-siem -> search_events.
   Result: evt-001, high severity failed login.

3. Multi-source investigation:
   The agent correlated SIEM and Threat Intelligence evidence.

4. Autonomous Multi-MCP selection:
   For 198.51.100.22, without explicitly naming the servers,
   the agent selected both:
   cyber-ti -> check_ip
   cyber-siem -> search_events.

   Threat Intelligence classified the IP as suspicious with
   confidence 0.80 and the SIEM contained a medium-severity
   firewall block event.

5. Context reuse finding:
   During one investigation of 185.220.101.5, the response reused
   results already present in conversation context and no fresh
   MCP Tool invocation was observed.

   Record the principle:

   MCP capability availability does not imply MCP invocation.

6. Freshness experiment:
   A subsequent prompt explicitly required fresh MCP Tool calls
   and prohibited reuse of previous conversation results.

   The agent then invoked both:

   cyber-siem_search_events
   cyber-ti_check_ip

   This demonstrates that dynamic or accessible security data does
   not itself guarantee fresh evidence.

7. Record the security principle:

   In security-sensitive workflows, evidence provenance and
   freshness must be explicitly controlled. Context reuse may
   otherwise cause an agent to reason over stale security data.

8. Provenance model:

   Distinguish:
   - SIEM-provided evidence
   - Threat-Intelligence-provided evidence
   - previous conversation context
   - LLM-generated inference

9. Record one grounding observation:
   An earlier response described a failed login as an
   "authenticated failed login attempt", which was not directly
   supported by the SIEM evidence. A later response correctly used
   "authentication failure".

   Record this as a minor example of semantic drift during
   evidence synthesis.

10. Lab 06 remains strictly read-only.
     No remediation or high-impact capabilities were exposed.

## Lab 07 - Identity and Authorization

### Overview
Lab 07 focused on identity handling and authorization within an MCP server that exposes `search_events` and `get_security_summary` tools. Identities (alice, bob, carol) were simulated via the MCP server's authentication layer, which mapped claimed identities to internal roles and permissions.

### Key Findings
1. The MCP server enforced authorization server-side; the LLM could not bypass checks via prompt text.
2. alice (granted `events:read`) was allowed to invoke `search_events`.
3. bob (lacking `events:read`) was denied access to `search_events` with `ACCESS_DENIED`.
4. carol (granted `summary:read`) was allowed to invoke `get_security_summary`.
5. alice (lacking `summary:read`) was denied `get_security_summary`.
6. Unknown or unmapped identities were rejected with `UNKNOWN_IDENTITY`.
7. A prompt‑based authorization bypass attempt (e.g., instructing the agent to act as bob while claiming alice) still resulted in `ACCESS_DENIED` because the server’s authorization decision is based on verified identity, not LLM‑provided claims.
8. **Security principle**: Prompt text must never be able to override server‑side authorization.
9. **Identity‑binding observation**: When the agent stated “I am alice”, the MCP server received `identity="alice"` and authorized the request because alice exists and holds `events:read`. This is not an authorization failure; it reflects an authentication/identity‑binding limitation where the server trusts the claimed identity without cryptographic verification.
10. Distinguish:
    - **claimed identity**: what the agent asserts (e.g., "I am alice").
    - **authenticated identity**: the identity verified by the server’s authentication mechanism (in this lab, simulated and based on a simple lookup).
    - **authorization decision**: the server’s evaluation of whether the authenticated identity has permission for the requested capability.
11. This lab intentionally uses simulated identity and does not implement cryptographic authentication; therefore, the binding between claimed and authenticated identity relies on the server’s internal simulation.
12. **Architectural lesson**:
    ```
    Authentication
        ↓
    Verified identity
        ↓
    Security context
        ↓
    Authorization
        ↓
    MCP capability
    ```
13. Authorization decisions must not depend on LLM judgment; they must be enforced by the MCP server independent of prompt content.
14. The lab remains read‑only; no remediation or high-impact capabilities were exposed.

### Conclusion
Lab 07 demonstrated that proper server‑side authorization prevents prompt injection attacks, while also highlighting the importance of separating authentication from authorization in MCP designs.