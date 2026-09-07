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

