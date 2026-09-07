# CyberSecurityMultiTool MCP Server

## Objective
Create an MCP server that provides three cybersecurity-related tools: IP reputation checking, hash malware lookup, and SSH log analysis.

## Architecture
- Built using MCP Python SDK v2.
- Single file `server.py` implements the server and three tools.
- Uses simulated threat intelligence and malware hash databases (hardcoded dictionaries).
- Deterministic analysis; no external API calls.
- Input validation performed before processing.
- Exposes tools via MCP stdio transport.

## MCP Tools

### 1. `check_ip(ip: str) -> dict`
- **Description**: Validates IPv4/IPv6 address and returns reputation information.
- **Validation**: Uses Python `ipaddress` module.
- **Threat Intelligence Database** (simulated):
  - `8.8.8.8` → benign
  - `185.220.101.5` → malicious
- **Return Fields**:
  - `ip`: input IP string
  - `ip_version`: 4 or 6
  - `reputation`: `"benign"`, `"malicious"`, or `"unknown"`
  - `confidence`: float between 0 and 1
  - `source`: `"internal"`

### 2. `check_hash(hash_value: str) -> dict`
- **Description**: Determines hash type (MD5, SHA1, SHA256) and checks against known malware hashes.
- **Validation**: Regex for hexadecimal characters and correct length.
- **Malware Hash Database** (simulated):
  - MD5 `44d88612fea8a8f36de82e1278abb02f` (EICAR test file) → malicious
- **Return Fields**:
  - `hash`: input hash string (lowercased)
  - `hash_type`: `"MD5"`, `"SHA1"`, `"SHA256"`
  - `status`: `"malicious"` or `"unknown"`
  - `malware_family`: string or `null`
  - `confidence`: float between 0 and 1
  - `source`: `"internal"`

### 3. `analyze_log(log_line: str) -> dict`
- **Description**: Performs deterministic analysis of a log line for SSH failed login patterns.
- **Pattern**: Looks for `Failed password for <username> from <source_ip> ssh2`.
- **Extraction**:
  - `source_ip`: IPv4 address (if present and valid)
  - `username`: string
  - `protocol`: `"SSH"`
- **Classification**:
  - `event_type`: `"failed_login"` if pattern matches, else `"unknown"`
  - `severity`: `"medium"` for failed login, `"info"` otherwise
- **Return Fields**:
  - `source_ip`: extracted IP or `null`
  - `username`: extracted username or `null`
  - `protocol`: `"SSH"` or `null`
  - `event_type`: string
  - `severity`: `"low"`, `"medium"`, `"high"`, or `"info"`
  - `confidence`: float between 0 and 1
  - `source`: `"pattern_matching"` or `"no_match"`

## Setup

1. **Prerequisites**:
   - Python 3.9+
   - Virtual environment already created (`.venv`)

2. **Install Dependencies**:
   ```powershell
   .\.venv\Scripts\pip install -r requirements.txt
   ```

3. **Configuration**:
   - Ensure `opencode.json` is present in the workspace root with the MCP server definition.

## How to Run

To start the MCP server:
```powershell
.\.venv\Scripts\python.exe server.py
```
The server will run and listen for MCP tool invocations via stdio.

## Example OpenCode Prompts

After the server is running, you can use the following prompts in OpenCode:

- `check_ip("8.8.8.8")`
- `check_hash("44d88612fea8a8f36de82e1278abb02f")`
- `analyze_log("Sep  7 10:00:00 host sshd[1234]: Failed password for root from 203.0.113.1 port 22 ssh2")`

## Security Considerations

- **Input Validation**: All inputs are validated before processing to prevent injection or unexpected behavior.
- **No External Calls**: The server does not make any network calls; all data is local and simulated.
- **Deterministic Output**: No use of randomness or AI; outputs are predictable.
- **Error Handling**: Exceptions are caught and returned as structured error responses rather than being propagated to the MCP client.
- **Least Privilege**: The server runs with the privileges of the user executing it; consider running in a restricted environment.
- **No Persistent State**: The server does not store state between invocations (except the static databases).

## Files Created or Modified

- `server.py` – Main MCP server implementation.
- `opencode.json` – MCP server configuration for OpenCode.
- `requirements.txt` – Dependency list (already present, unchanged).
- `README.md` – This documentation.