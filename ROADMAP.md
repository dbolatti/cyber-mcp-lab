# Learning Roadmap: MCP Cybersecurity Lab

## Lab 1 - Basic MCP Server
- Tool
- Resource
- Prompt
- OpenCode integration
Status: Completed

## Lab 2 - External Threat Intelligence API
- Replace simulated check_ip data with a real external API
- Environment variables
- Secret handling
- Error handling
- API timeout and rate limiting
Status: Completed and validated

## Lab 3 - Multiple cybersecurity tools
- check_ip
- check_hash
- analyze_log
Status: Validated

## Lab 4 - MCP Resources
- asset inventory
- incidents
- security policies
- dynamic resources
Status: Completed

## Lab 5 - MCP + SIEM
- Controlled read-only abstraction layer over simulated SIEM dataset
- Resources: security://siem/events/recent, security://siem/events/{event_id}
- Tools: search_events, get_security_summary
Status: Completed and validated

## Lab 6 - Multi-MCP
- Cyber-siem and cyber-ti MCP servers
- Autonomous tool selection
- Evidence fusion
- LLM inference

Status: Completed

## Lab 7 - MCP attack scenarios
- prompt injection
- tool poisoning
- malicious MCP server
- tool shadowing
- confused deputy
- excessive agency
Status: Completed and validated

## Lab 8 - Authentication and Identity Binding
- Credential-based authentication via CYBERLAB_TOKEN
- SHA-256 token digests stored server-side
- hmac.compare_digest for secure comparison
- Server-side identity derivation from credential
- Post-authentication authorization with default deny
- Read-only capabilities

Status: Completed and validated

## Lab 9 - High-Impact Tools, Human-in-the-Loop and Excessive Agency
- MCP server: CyberSecurityResponse
- Tools: get_incidents, get_security_state, propose_action, approve_action, execute_action
- Supported simulated actions: block_ip, isolate_host, disable_account
- Architecture: OBSERVE -> PROPOSE -> APPROVE -> EXECUTE -> VERIFY
- State machine: PENDING_APPROVAL -> APPROVED -> EXECUTED
Status: Completed and validated

## Lab 10 - Secure Agentic SOC
- Multi-MCP SOC lab with servers: cyber-soc, cyber-ti, cyber-response
- End-to-end workflow: Incident → SOC evidence → Threat Intelligence → correlation/reasoning → proposal → human approval → execution → independent verification
Status: Completed and validated

The MCP lab sequence (Labs 01-10) is now complete.



Future work:
- stale context and provenance
- fabricated or conflicting evidence
- cross-MCP trust and attestation
- stronger out-of-band HITL authorization
- security of multi-agent or multi-MCP composition