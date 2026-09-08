# Lab 08: Authentication and Identity Binding in MCP

## Lab Objective
Demonstrate authentication and identity binding in a local MCP environment, correcting the principal weakness from Lab 07 where the LLM could select identity by passing an `identity` parameter.

## Authentication vs Authorization
- **Authentication**: Verifying who you are (using a credential).
- **Authorization**: Determining what you are allowed to do (based on identity and policy).

In this lab:
- Authentication is performed server-side by validating a token provided via the `CYBERLAB_TOKEN` environment variable.
- Authorization is performed server-side by checking the authenticated identity's scopes against the required scope for each tool.
- The LLM cannot influence authentication or authorization through prompt text.

## Claimed Identity vs Verified Identity
- **Claimed Identity**: An identity asserted by the client (e.g., via a parameter). This lab does not accept claimed identity as input.
- **Verified Identity**: The identity derived from validating the credential. This is the only identity used for authorization.

## Identity Binding
The verified identity is bound to the MCP session at authentication time and used for all subsequent tool invocations in that session. The LLM cannot change this identity during the session.

## Token Hashing
For security, the server does not store plaintext tokens. Instead, it stores SHA-256 digests of the tokens. During authentication:
1. The token from `CYBERLAB_TOKEN` is hashed.
2. The hash is compared to the stored digests using `hmac.compare_digest` to prevent timing attacks.
3. If a match is found, the associated identity is retrieved.

## Environment-Based Credential Injection
The token is supplied to the MCP process via the `CYBERLAB_TOKEN` environment variable. OpenCode inherits this environment variable when launching the MCP server.

## Least Privilege and Default Deny
- Each tool requires a specific scope (e.g., `assets:read`, `events:read`, `summary:read`).
- The authorization function uses default deny: if the identity does not have the required scope, access is denied.
- The `whoami` tool requires no scope (only authentication).

## Why Identity is Not a Tool Parameter
In Lab 07, accepting an `identity` parameter allowed the LLM to impersonate any identity. By removing this parameter and deriving identity solely from the credential, we prevent identity spoofing via prompt text.

## Why Prompt Text Cannot Change Authenticated Identity
Authentication occurs before tool execution, using only the environment variable. The LLM has no way to influence the `CYBERLAB_TOKEN` variable or the authentication process through tool parameters.

## Test Setup
Three simulated identities are available:

| Identity | Role | Token (for testing) | Scopes |
|----------|------|---------------------|--------|
| alice    | analyst | `lab08-alice-token-2026` | `events:read`, `assets:read` |
| bob      | viewer  | `lab08-bob-token-2026`   | `assets:read` |
| carol    | senior_analyst | `lab08-carol-token-2026` | `events:read`, `assets:read`, `summary:read` |

**Note**: These tokens are for educational purposes only and must never be reused outside this lab.

To test, set the `CYBERLAB_TOKEN` environment variable in the shell where OpenCode is launched:
```powershell
$env:CYBERLAB_TOKEN = "lab08-alice-token-2026"
```
Then start OpenCode. The MCP server will authenticate the session as the corresponding identity.

## Threat Model
- **Threat**: LLM attempts to bypass authentication or impersonate another identity.
- **Mitigation**: 
  - No identity or token parameters in tools.
  - Server-side authentication and authorization.
  - Token comparison via `hmac.compare_digest`.
  - Default deny authorization.
- **Limitation**: This is an educational model. Production systems should use OAuth/OIDC with short-lived credentials and secure token storage.

## Static Validation Performed
Before completion, we verified:
- `MCPServer` instantiated before decorators.
- No tool accepts `identity` or `token` parameters.
- `authenticate()` and `authorize()` are internal functions (not exposed as tools).
- `hmac.compare_digest` used for digest comparison.
- No plaintext tokens appear in `server.py`.
- Missing token results in `AUTHENTICATION_REQUIRED`.
- Invalid token results in `INVALID_CREDENTIAL`.
- Valid token binds to exactly one identity.
- Authorization occurs after authentication.
- No duplicate function names.
- No recursion.
- No raw exceptions exposed.
- No token logging.
- `server.run()` exists.
- No filesystem, subprocess, or network access in the server.

## Conclusion
This lab demonstrates a secure pattern for identity binding in MCP environments, where authentication and authorization are strictly server-side and the LLM cannot influence the verified identity.