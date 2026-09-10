# Lab 02: Cyber Threat Intelligence MCP Server

## Objective
Create an MCP server named "CyberSecurityThreatIntel" that exposes a tool to check IP addresses against the AbuseIPDB API for threat intelligence.

## Architecture
- **MCP Server**: Built with the MCP Python SDK v2
- **Tool**: `check_ip(ip: str) -> dict` 
- **External API**: AbuseIPDB v2 CHECK endpoint
- **Environment**: Python virtual environment with dependencies managed by requirements.txt
- **Configuration**: API key loaded from `.env` file (never hardcoded)

## Environment Setup
1. Ensure Python 3.8+ is installed
2. Create a virtual environment (if not already created):
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   .\.venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure the API key:
   - Copy `.env.example` to `.env`
   - Edit `.env` and set `ABUSEIPDB_API_KEY` to your actual AbuseIPDB API key

## How to Run the MCP Server
1. Activate the virtual environment (if not already active)
2. Start the server:
   ```bash
   python server.py
   ```
   The server will run via stdio and be ready to accept MCP tool calls.

## How to Test from OpenCode
Once the server is running, you can use the MCP tool in OpenCode:
- The server is configured in `opencode.json` as `cyber-threat-intel`
- In OpenCode, you can call the tool like:
  ```
  check_ip("8.8.8.8")
  ```
- The tool will return a normalized dictionary with threat intelligence data.

## Security Considerations
- **API Key Protection**: The AbuseIPDB API key is loaded from environment variables (`ABUSEIPDB_API_KEY`) stored in `.env`. Never commit `.env` to version control.
- **Input Validation**: IP addresses are validated using Python's `ipaddress` module before making external API calls.
- **Error Handling**: Specific error conditions (invalid IP, missing API key, timeouts, HTTP errors, malformed responses) are handled without exposing internal details.
- **Least Privilege**: The tool only returns normalized data, not the raw API response, limiting data exposure.
- **No Hardcoded Credentials**: All credentials must be provided via environment variables.
- **Timeouts**: External API calls have a 10-second timeout to prevent hanging dependencies.

## Files Created/Modified
- `server.py`: Contains the MCP server implementation
- `opencode.json`: Configures the local MCP server for OpenCode
- `requirements.txt`: Lists direct project dependencies (mcp, python-dotenv, requests)
- `.env.example`: Template for environment variables (copy to `.env` and add your API key)
- `README.md`: This file

## Notes
- Do not make real requests to AbuseIPDB during development without a valid API key.
- The server is designed to be run locally via stdio for MCP integration.

## Lab Status
**Validated/Completed**  
The following were successfully verified:
- Python syntax validation
- Successful server import
- MCP connectivity through OpenCode
- Real AbuseIPDB API integration
- Successful lookup of 185.220.101.5
- Normalized threat intelligence response
- API key remained server-side and was not exposed through the MCP result
- Invalid IP input was rejected locally before an external API call

**Architectural Flow:**
OpenCode
→ MCP
→ cyber-threat-intel server
→ AbuseIPDB API
→ normalized response
→ MCP
→ OpenCode