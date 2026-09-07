# CyberSecurity MCP Lab

An educational laboratory to learn the Model Context Protocol (MCP) through practical cybersecurity examples.

## Project Purpose

The goal of this project is to understand and experiment with the Model Context Protocol (MCP) by building a simple MCP server that exposes core MCP primitives: **Tool**, **Resource**, and **Prompt**. The server is designed for learning and is intentionally kept simple—using simulated data and avoiding external dependencies—to focus on MCP concepts.

## Current Architecture

```mermaid
graph TD
    A[MCP Client (e.g., OpenCode)] -->|MCP Protocol| B(CyberSecurityLab MCP Server)
    B -->|Tool| C[check_ip: Threat Intelligence Lookup]
    B -->|Resource| D[security://assets: Asset Inventory]
    B -->|Prompt| E[investigate_ioc: Investigation Guidance]
```

The server is implemented in Python using the official MCP Python SDK and communicates via stdio transport, making it easy to connect with MCP hosts like OpenCode.

## Requirements

- Windows 11
- PowerShell
- Python 3.9+
- MCP Python SDK (version 2.1.1)

## Setup Instructions

### 1. Clone the Repository
```powershell
git clone <repository-url>
cd cyber-mcp-lab
```

### 2. Create a Python Virtual Environment
```powershell
python -m venv .venv
```

### 3. Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```
*(This installs the MCP Python SDK.)*

## Running the MCP Server

With the virtual environment activated, start the server:
```powershell
python server.py
```
The server will run and listen for MCP connections over stdio.

## Connecting with OpenCode

This project includes an `opencode.json` file that configures OpenCode to connect to the locally running MCP server.

Once the server is running (`python server.py`), OpenCode can automatically discover and connect to it via the MCP protocol, allowing the LLM to invoke the `check_ip` tool, read the `security://assets` resource, and use the `investigate_ioc` prompt.

## MCP Primitives Implemented

### Tool: `check_ip`
- **Purpose:** Simulates a threat intelligence lookup for an IP address.
- **Input:** `ip: string`
- **Output:** Structured data with `ip`, `reputation`, `confidence`, and `source`.
- **Example Invocation (via OpenCode or MCP Inspector):**
  ```json
  {
    "name": "check_ip",
    "arguments": { "ip": "185.220.101.5" }
  }
  ```
- **Example Response:**
  ```json
  {
    "ip": "185.220.101.5",
    "reputation": "malicious",
    "confidence": 0.95,
    "source": "CyberSecurityLab simulated Threat Intelligence"
  }
  ```

### Resource: `security://assets`
- **Purpose:** Provides a simulated asset inventory.
- **URI:** `security://assets`
- **Output:** JSON object mapping asset names to their details (IP, type, criticality).
- **Example Contents:**
  ```json
  {
    "web-server-01": { "ip": "192.168.1.10", "type": "web_server", "criticality": "high" },
    "db-server-01": { "ip": "192.168.1.20", "type": "database", "criticality": "critical" },
    "workstation-01": { "ip": "192.168.1.100", "type": "workstation", "criticality": "medium" }
  }
  ```

### Prompt: `investigate_ioc`
- **Purpose:** Generates a concise instruction for a cybersecurity analyst to investigate an Indicator of Compromise (IOC).
- **Input:** `ioc: string`
- **Output:** A formatted string guiding the investigation.
- **Example Invocation:**
  ```json
  {
    "name": "investigate_ioc",
    "arguments": { "ioc": "185.220.101.5" }
  }
  ```
- **Example Output:**
  ```
  Investigate the IOC '185.220.101.5'. Determine:
  - IOC reputation
  - Possible associated threats
  - Potentially affected assets
  - Recommended response
  - Whether escalation is required
  ```

## Understanding MCP Concepts

- **OpenCode as MCP Host/Client:** OpenCode acts as an MCP host that can discover and connect to MCP servers. It routes LLM function calls to the appropriate MCP server via the MCP protocol.
- **MCP Server:** The `CyberSecurityLab` server exposes MCP primitives (tools, resources, prompts) that clients can invoke.
- **LLM Tool Calling:** When the LLM decides to use a tool, OpenCode (as the MCP client) sends a tool invocation request to the MCP server, which executes the tool and returns the result.
- **Difference Between Tool, Resource, and Prompt:**
  - **Tool:** A callable function that performs an action (e.g., checking an IP's reputation).
  - **Resource:** A read-only piece of data (e.g., an asset inventory) identified by a URI.
  - **Prompt:** A pre-defined template or guidance (e.g., investigation steps) that can be parameterized and sent to the LLM.

## Current Limitations

- **Simulated Data:** All data (threat intelligence, asset inventory) is simulated; no real external APIs are called.
- **No External APIs:** The server does not make any network calls to external services.
- **No Authentication:** The server does not implement any authentication or authorization mechanisms.
- **No Destructive Actions:** All operations are read-only or simulations; no real-world state is modified.

## Security Note

In future labs where we introduce write or high-impact tools (e.g., `block_ip`, `isolate_endpoint`), we will implement proper security controls including authentication, authorization, least privilege, approval gates, input validation, and audit logging. Never expose destructive tools without these safeguards.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the planned learning progression.

---

*This project is for educational purposes only and is not intended for production use.*