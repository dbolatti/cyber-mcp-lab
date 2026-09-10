# Lab 05: Simulated SIEM Integration via MCP

Status: VALIDATED / COMPLETED

## Lab Objective
Build a simulated SIEM integration through MCP to demonstrate that an AI agent should not require direct access to a SIEM backend. The MCP Server exposes a controlled, structured interface to security events.

## Architecture
```
OpenCode / LLM
       |
    MCP Client
       |
       v
CyberSecuritySIEM MCP Server
       |
       v
Simulated SIEM dataset
```

The MCP Server acts as an abstraction layer and security boundary, preventing direct LLM access to the underlying SIEM system.

## Why MCP Acts as an Abstraction/Security Boundary
- The LLM interacts only with the MCP server via defined Resources and Tools.
- The MCP server validates all inputs and controls what data is exposed.
- No direct queries, shell commands, or remote execution are possible.
- The simulation is read-only; no destructive actions are exposed.

## Resources versus Tools in this Lab
**Resources** (read-only data access):
- `security://siem/events/recent`: Returns a list of recent SIEM events.
- `security://siem/events/{event_id}`: Returns a specific event by ID.

**Tools** (parameterized operations):
- `search_events`: Filters events by severity, event_type, and source_ip.
- `get_security_summary`: Returns statistical summary of the dataset.

## Simulated SIEM Dataset
The dataset contains 8 events representing common security scenarios:
1. Failed SSH authentication
2. Malware detection
3. Firewall block
4. Authentication anomaly
5. Privilege escalation
6. Suspicious PowerShell execution
7. Port scan
8. Successful login

Each event includes: event_id, timestamp, event_type, severity, source_ip, destination_asset, username, description.

## Setup
1. Ensure Python virtual environment exists at `.\\.venv\\Scripts\\python.exe`.
2. Install dependencies: `pip install -r requirements.txt`
3. The MCP server is configured in `opencode.json`.

## Execution
The MCP server runs via stdio transport. OpenCode will spawn the server process as defined in the configuration.

## Example Queries
### Via MCP Client (OpenCode)
- Read recent events: `security://siem/events/recent`
- Get specific event: `security://siem/events/evt002`
- Search events: Use `search_events` tool with parameters.
- Get summary: Use `get_security_summary` tool.

### Example Tool Calls
```
search_events(severity="high")
search_events(severity="high", source_ip="185.220.101.5")
get_security_summary()
```

## Security Considerations
- Input validation: All tool parameters are validated and normalized.
- Error handling: Unknown event IDs return a controlled response, not raw exceptions.
- No direct system access: The server cannot execute commands, access files, or make network calls.
- Read-only: No tools for modification or remediation.

## Limitations of the Simulation
- Dataset is hardcoded and static.
- No real-time event ingestion.
- No persistent storage.
- No authentication or authorization (would be added in a real deployment).
- Severity normalization is case-insensitive but limited to predefined values.

## Files Created
- `server.py`: MCP server implementation with Resources and Tools.
- `opencode.json`: OpenCode MCP server configuration.
- `requirements.txt`: Dependencies (MCP Python SDK v2).
- `README.md`: This file.

## Assumptions
- The Python virtual environment is already set up.
- The MCP Python SDK v2 is compatible with the server implementation.
- OpenCode will correctly launch the server via the command in opencode.json.

## Uncertainties
- The exact version of the MCP SDK that provides `mcp.server.MCPServer` and `stdio_server`.
- Whether additional dependencies like starlette are required (they may be transitive).

## Validation
- Python syntax compilation: PASS
- Python server import: PASS
- MCP server connection through OpenCode: PASS
- get_security_summary tool: PASS
- search_events with severity=high: PASS
- MCP resource discovery: PASS
- read security://siem/events/evt005: PASS
- consistency with the simulated SIEM dataset: PASS
- read-only SIEM behavior: PASS

## Validated Architecture
OpenCode
→ MCP
→ cyber-siem
→ simulated SIEM dataset
→ Tools / Resources
→ MCP
→ OpenCode