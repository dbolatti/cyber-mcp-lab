# Lab 01 Architecture

## Components

`mermaid
flowchart TD
    A[User] -->|Interacts with| B[OpenCode]
    B -->|Uses LLM| C[LLM]
    C -->|MCP Client| D[MCP Client (inside OpenCode)]
    D -->|MCP Protocol| E[CyberSecurityLab MCP Server]
    E -->|Exposes| F[Tool: check_ip]
    E -->|Exposes| G[Resource: security://assets]
    E -->|Exposes| H[Prompt: investigate_ioc]
`

### Role of Each Component

- **User**: The person interacting with the system via OpenCode.
- **OpenCode**: The IDE/agent that acts as an MCP host. It provides the chat interface, manages the LLM, and includes an MCP client for server communication.
- **LLM**: The language model (e.g., GPT‑4) that generates text and decides when to invoke tools.
- **MCP Client**: The component inside OpenCode that connects to MCP servers using the MCP protocol, forwards tool invocations, and returns results.
- **CyberSecurityLab MCP Server**: The Python server exposing the three MCP primitives:
  - **Tool check_ip**: Simulated threat‑intelligence lookup.
  - **Resource security://assets**: Static asset inventory.
  - **Prompt investigate_ioc**: Guidance for investigating an indicator of compromise.
- **Cybersecurity services**: In this lab the services are simulated; in later labs they will be real threat‑intelligence feeds, asset databases, etc.

## Transport

The Lab 01 server uses **stdio transport**, meaning it communicates over standard input and output streams. This is suitable for local development and testing with MCP Inspector or OpenCode.

