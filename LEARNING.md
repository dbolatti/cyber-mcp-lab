# Learning Notebook - CyberSecurity MCP Lab

## Concepts Learned (Lab 01)

- **MCP Host**: The application (e.g., OpenCode) that manages connections to MCP servers.
- **MCP Client**: The component within the host that communicates with the server using the MCP protocol.
- **MCP Server**: A service exposing MCP primitives (tools, resources, prompts).
- **Tool**: A callable function that performs an action (e.g., check_ip).
- **Resource**: A read-only piece of data identified by a URI (e.g., security://assets).
- **Prompt**: A pre‑defined template or guidance that can be parameterized (e.g., investigate_ioc).
- **Tool/Function Calling vs MCP**: Traditional function calling is direct; MCP provides a standardized protocol for discovery and invocation across processes/languages.
- **stdio transport**: The default communication mechanism used by the Lab 01 server (message‑based over standard input/output).

## Lessons Learned from Lab 01

1. **Initial implementation mixed MCP low‑level Server API with the high‑level decorator API**.  
   The generated code used rom mcp.server import Server and then applied decorators that belong to the high‑level MCPServer class.

2. **Human review detected the issue**.  
   By inspecting the installed MCP SDK (mcp==2.1.1) we saw that the high‑level API is exposed via MCPServer from mcp.server.

3. **Corrected implementation to use MCPServer**.  
   Changed the import to rom mcp.server import MCPServer and instantiated server = MCPServer("CyberSecurityLab").  
   Added the explicit resource URI: @server.resource("security://assets").

4. **During repository restructuring, a Bash‑style command (mkdir -p) was incorrectly attempted in PowerShell**.  
   This highlighted the need to use PowerShell‑native commands (New-Item) when working on Windows.

These notes will grow as we progress through the labs.

