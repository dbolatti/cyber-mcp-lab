# Lab 04: Dynamic MCP Resources

## Objective
The objective of this lab is to create an MCP (Model Context Protocol) server named `CyberSecurityResources` that exposes only **Resources** (no Tools or Prompts). This lab focuses on demonstrating:
- Static Resources
- Dynamic Resources (using URI templates)
- Proper MCP resource registration
- Structured data return without exposing internal errors

## Difference Between MCP Tools and Resources
- **Tools**: Functions that the LLM can invoke to perform actions (like calling an API, running a command). They have side effects.
- **Resources**: Data sources that the LLM can read (like files, database records). They are read-only and provide context.

## Static vs Dynamic Resources
- **Static Resources**: Have a fixed URI and return the same structure (though data may change). Example: `security://assets` always returns the list of assets.
- **Dynamic Resources**: Use URI templates with variables. Example: `security://assets/{asset_id}` where `{asset_id}` is a placeholder for a specific asset's ID.  
  > **Note**: In this lab, the data behind the dynamic resource is still simulated and static (hardcoded). Truly dynamic data sources (e.g., live database queries, external APIs) will be explored in later Labs.

## Resource URIs Used
1. `security://assets` - Static resource returning a list of organizational assets.
2. `security://assets/{asset_id}` - Dynamic resource returning details for a specific asset.
3. `security://events/recent` - Static resource returning recent cybersecurity events.

## Setup
1. Ensure you are in the lab directory (`lab04-dynamic-resources`).
2. The Python virtual environment (`.venv`) should already be present with the MCP SDK installed.
3. If needed, install dependencies: `pip install -r requirements.txt` (though `mcp` is already listed).

## How to Run
To start the MCP server, run:
```
.\.venv\Scripts\python.exe server.py
```
The server will communicate over stdio, ready for an MCP client (like OpenCode) to connect.

## Example OpenCode Queries
Once the server is configured in `opencode.json`, you can ask OpenCode questions like:
- "List all security assets" → should call `security://assets`
- "Get details for asset with ID 2" → should call `security://assets/2`
- "Show recent security events" → should call `security://events/recent`

## Security Considerations
- All data is simulated; no real assets or events are exposed.
- No external APIs or system files are accessed.
- Errors are handled gracefully (e.g., missing asset returns a structured error rather than raising an exception).
- The server only exposes read-only resources, preventing unintended side effects via the MCP protocol.

## Files Created/Modified
- `server.py`: Contains the MCP server implementation with three resources.
- `opencode.json`: Configures the local MCP server for OpenCode.
- `README.md`: This file.
- `requirements.txt`: Already listed `mcp`; no changes needed.

## Notes
- The server uses `MCPServer` from the MCP SDK.
- Resources are registered using the `@server.resource` decorator.
- The dynamic resource uses a URI template with `{asset_id}`.
- Data is hardcoded for simulation purposes.
- The server is started with `server.run()` which uses stdio transport.