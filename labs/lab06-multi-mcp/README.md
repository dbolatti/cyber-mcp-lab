# Lab 06: Multi-MCP Environment

## Lab Objective
Build a Multi-MCP environment with two independent local MCP servers to study how an AI agent selects between multiple MCP servers and how it combines evidence from different security domains.

## Multi-MCP Architecture
```
                    OpenCode / LLM
                          |
                     MCP Client
                    /          \
                   /            \
        CyberSecuritySIEM   CyberThreatIntel
               |                  |
        simulated events    simulated reputation DB
```

## Server Responsibilities

### CyberSecuritySIEM (siem_server.py)
- Provides access to simulated SIEM event data
- Exposes `search_events` tool for querying security events
- Filters by source IP and severity (case-insensitive)
- Read-only, deterministic access to 6 predefined security events

### CyberThreatIntel (threat_intel_server.py)
- Provides access to simulated threat intelligence reputation data
- Exposes `check_ip` tool for IP reputation lookup
- Validates IP addresses using Python's `ipaddress` module
- Returns reputation, confidence, and source information
- Handles unknown and invalid IPs with structured responses

## Tool Separation
The two servers implement strict capability separation:
- SIEM server handles internal security event data
- Threat intelligence server handles external IP reputation data
- No overlap in functionality or data access
- Each server represents a distinct trust domain

## Why Capability Separation Matters
1. **Security Isolation**: Compromise of one server doesn't expose data from the other
2. **Clear Responsibility Boundaries**: Each server has a single, well-defined purpose
3. **Independent Scaling**: Servers can be scaled or updated independently
4. **Auditability**: Clear provenance of which server provided which information
5. **Reduced Attack Surface**: Minimal permissions granted to each MCP server

## Expected Tool-Selection Behavior
The OpenCode LLM should:
1. Route IP reputation queries to `cyber-ti check_ip`
2. Route SIEM event queries to `cyber-siem search_events`
3. For combined investigations (e.g., "investigate this IP"), potentially use both servers:
   - First check IP reputation with cyber-ti
   - Then search for related events with cyber-siem

## Provenance Implications
- Each tool response clearly indicates its source server
- Enables the LLM to attribute information to the correct domain
- Supports chain-of-thought reasoning about data origins
- Facilitates debugging and validation of AI-generated conclusions

## Security Considerations
- **Read-only**: No remediation capabilities implemented (no `block_ip`, `isolate_host`, etc.)
- **No Direct Access**: LLM cannot access underlying datasets directly
- **Simulation Only**: All data is simulated; no real network or system access
- **Controlled Errors**: Invalid inputs return structured errors, not exceptions
- **Deterministic**: Same inputs always produce same outputs for reproducibility

## Setup
1. Ensure Python virtual environment is activated (`.\\.venv\\Scripts\\Activate.ps1`)
2. Install dependencies: `pip install -r requirements.txt`
3. Verify MCP servers are properly configured in `opencode.json`

## Validation Workflow
To validate the implementation:
1. Check that both servers define their MCPServer instance before decorators
2. Verify tool function names are unique within each server
3. Confirm all decorators reference existing server instances
4. Ensure no unnecessary imports are present
5. Validate that all tool return values are structured dictionaries
6. Confirm no raw exceptions are intentionally exposed
7. Verify both entry points use `server.run()`
8. Confirm no external network, filesystem, or subprocess access

## Example Prompts

### 1. Check IP Reputation
**Prompt**: "Check the reputation of IP 185.220.101.5."
**Expected Tool**: `cyber-ti check_ip`
**Expected Result**: Malicious reputation with 0.95 confidence

### 2. Find SIEM Events
**Prompt**: "Find SIEM events involving 185.220.101.5."
**Expected Tool**: `cyber-siem search_events`
**Expected Result**: Failed SSH login event (evt-001)

### 3. Combined Investigation
**Prompt**: "Investigate IP 185.220.101.5 using all relevant MCP capabilities."
**Expected Tools**: Both `cyber-ti check_ip` and `cyber-siem search_events` may be used
**Expected Workflow**: 
1. Check IP reputation (malicious)
2. Search for related SIEM events (failed SSH login)

## Files Created
- `siem_server.py`: SIEM MCP server
- `threat_intel_server.py`: Threat intelligence MCP server
- `opencode.json`: OpenCode MCP client configuration
- `requirements.txt`: Python dependencies
- `README.md`: This documentation

## Remaining Risks or Uncertainties
1. **Server Naming**: Ensure server names match exactly what the LLM expects
2. **Tool Description Clarity**: Tool descriptions should be sufficiently detailed for LLM routing
3. **Error Handling**: Structured errors must be properly formatted for LLM consumption
4. **Dataset Realism**: While simulated, datasets should reflect realistic security scenarios
5. **Performance**: With larger datasets, filtering efficiency might become a concern (not applicable here with 6 events)