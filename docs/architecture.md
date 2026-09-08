# Lab 06 Architecture

## Architecture Diagram

```
                    OpenCode / LLM
                          |
                     MCP Client
                    /          \
                   /            \
          cyber-siem          cyber-ti
         search_events        check_ip
                   \            /
                    \          /
                 evidence fusion
                       |
                 LLM inference
```

## Component Description

- **OpenCode / LLM**: The OpenCode interface hosting the language model.
- **MCP Client**: The MCP client within OpenCode that connects to servers.
- **cyber-siem**: MCP server providing the `search_events` tool for SIEM data.
- **cyber-ti**: MCP server providing the `check_ip` tool for threat intelligence.
- **evidence fusion**: The process of correlating evidence from both servers.
- **LLM inference**: The language model's reasoning based on fused evidence.

## Transport

stdin/stdout (stdio) transport is used for MCP communication.

