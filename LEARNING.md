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

