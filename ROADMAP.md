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
Status: Implemented and MCP integration validated (real API call pending API key configuration)

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
Status: Implemented, static validation passed, MCP functional validation pending

## Lab 6 - MCP security controls
- authentication
- authorization
- least privilege
- approval gates
- input validation
- audit logging

## Lab 7 - MCP attack scenarios
- prompt injection
- tool poisoning
- malicious MCP server
- tool shadowing
- confused deputy
- excessive agency

## Lab 8 - Secure MCP architecture
- policy enforcement layer
- trust boundaries
- authorization per tool
- human-in-the-loop
- traceability

## Lab 9 - Multiple MCP servers
- Threat Intelligence
- SIEM
- EDR
- CMDB

## Lab 10 - Complete architecture
- OpenCode
- OpenRouter / model provider
- multiple LLMs
- multiple MCP servers
- secure orchestration