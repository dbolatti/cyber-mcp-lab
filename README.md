# Cybersecurity MCP Learning Laboratory

This repository is a progressive learning and experimentation laboratory for:
- Model Context Protocol (MCP)
- Building cybersecurity MCP servers
- Studying MCP security
- Experimenting with AI-assisted software development

## Repository Structure

The repository is organized as a monorepo of independent learning laboratories (labs). Each lab is a self-contained OpenCode workspace with its own:
- Virtual environment (`.venv`)
- Dependencies (`requirements.txt`)
- OpenCode configuration (`opencode.json`)
- MCP server implementation

Labs are located in the `labs/` directory and are numbered sequentially to reflect the learning progression.

## Lab Index

| Lab | Directory | Status | Description |
|-----|-----------|--------|-------------|
| Lab 01 | `labs/lab01-basic-mcp` | ✅ Completed and validated | Basic MCP server with simulated threat intelligence: `check_ip` tool, `security://assets` resource, `investigate_ioc` prompt. Integrated with OpenCode via stdio. |
| Lab 02 | `labs/lab02-threat-intel-api` | ⚠️ Implemented, MCP integration validated | MCP server wrapping the AbuseIPDB API: `check_ip` tool with real external API calls (pending API key configuration). Includes environment variable handling, input validation, timeout handling, and response normalization. |
| Lab 03 | `labs/lab03-multiple-tools` | ✅ Implemented | MCP server exposing multiple cybersecurity tools: `check_ip`, `check_hash`, and `analyze_log`. Uses local deterministic logic and simulated data. Demonstrates tool selection by the LLM/agent. |
| Lab 04 | `labs/lab04-dynamic-resources` | ✅ Completed and validated | MCP server demonstrating dynamic MCP Resources: static resources (`security://assets`, `security://events/recent`), resource template (`security://assets/{asset_id}`), and runtime-generated resource (`security://runtime/session`). Validated OpenCode consumption of MCP Resources, observed context reuse vs fresh reads, and documented security implications. |
| Lab 05 | `labs/lab05-mcp-siem` | ⚠️ Implemented, static validation passed, MCP functional validation pending | MCP server providing a controlled read-only abstraction layer over a simulated SIEM dataset. Resources: `security://siem/events/recent`, `security://siem/events/{event_id}`. Tools: `search_events`, `get_security_summary`. AI-assisted development findings: function-name collision and initialization-order defect identified and corrected. Validation workflow established for future labs. |
| Lab 06 | `labs/lab06-multi-mcp` | ✅ Completed and validated | Multi-MCP server demonstrating autonomous tool selection across cyber-siem and cyber-ti, evidence fusion, and LLM inference with strict read-only access. |
| Lab 07 | `labs/lab07-identity-authorization` | ✅ Completed and validated | Identity and authorization lab: MCP server enforced authorization server-side; tested alice (events:read) allowed search_events, bob denied; carol (summary:read) allowed get_security_summary, alice denied; unknown identities denied UNKNOWN_IDENTITY; prompt-based authorization bypass attempts failed with ACCESS_DENIED; observed identity-binding limitation where claimed identity influenced authorization; documented security principles and architectural lessons. |
| Lab 08 | `labs/lab08-identity-binding` | ✅ Completed and validated | Authentication and identity binding: MCP server authenticates via CYBERLAB_TOKEN, derives identity server-side, enforces authorization post-authentication, default deny, read-only capabilities. |
| Lab 09 | `labs/lab09-hitl-actions` | ✅ Completed and validated | High-Impact Tools, Human-in-the-Loop and Excessive Agency |
| Lab 10 | `labs/lab10-secure-agentic-soc` | ✅ Implemented and validated | Secure multi-MCP agentic SOC lab with three MCP servers: cyber-soc, cyber-ti, cyber-response. End-to-end workflow: Incident → SOC evidence → Threat Intelligence → correlation/reasoning → proposal → human approval → execution → independent verification. |

## Setup Instructions

1. Clone the repository
2. Navigate to a lab directory (e.g., `cd labs/lab01-basic-mcp`)
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables if required (see lab-specific README)
5. Launch OpenCode from the lab directory to access the MCP server

> **Note**: Each lab is an independent OpenCode workspace. You must launch OpenCode from within the lab directory to use its configured MCP server.

## Security Focus

This laboratory emphasizes secure MCP practices:
- Secrets (e.g., API keys) are kept outside version control using `.env` files
- Internal exceptions are not exposed to the LLM; sanitized error messages are returned
- Tool descriptions and contracts are carefully crafted to influence correct tool selection by the model
- Input validation and response normalization prevent injection attacks
- Each lab builds on previous lessons to progressively introduce security considerations

See [ROADMAP.md](ROADMAP.md) for the planned learning progression.

