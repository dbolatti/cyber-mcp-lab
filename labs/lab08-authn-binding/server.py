import os
import hashlib
import hmac
from mcp.server import MCPServer

# Simulated token digests (SHA-256 of the test tokens)
TOKEN_DIGESTS = {
    "alice": "d9c4052f2d53af814ce92d99d1b9c127fd50ed67eb1319ac41015f237da210f3",
    "bob": "abd7524c1641d1c366833553c443da0a936ee3c686e609a473f8ba082b94486e",
    "carol": "6f64c86a0ed9131a5e43cbaedf138d6b990f7533068b03d211056af58dcef4f3"
}

# Identity mapping: identity -> (role, scopes)
IDENTITY_INFO = {
    "alice": ("analyst", ["events:read", "assets:read"]),
    "bob": ("viewer", ["assets:read"]),
    "carol": ("senior_analyst", ["events:read", "assets:read", "summary:read"])
}

# Simulated security data
ASSETS = ["web-server-01", "db-server-01", "workstation-01"]
EVENTS = [
    {"type": "failed_login", "severity": "high", "ip": "185.220.101.5"},
    {"type": "malware_detection", "severity": "critical", "ip": "10.0.5.45"},
    {"type": "firewall_block", "severity": "medium", "ip": "198.51.100.22"}
]

def authenticate():
    """Internal function to authenticate the session using CYBERLAB_TOKEN."""
    token = os.environ.get("CYBERLAB_TOKEN")
    if token is None:
        return {
            "authenticated": False,
            "error": {
                "code": "AUTHENTICATION_REQUIRED",
                "message": "No authentication credential was provided"
            }
        }
    # Compute SHA-256 of the token
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    # Compare with stored digests using hmac.compare_digest
    for identity, digest in TOKEN_DIGESTS.items():
        if hmac.compare_digest(token_hash, digest):
            role, scopes = IDENTITY_INFO[identity]
            return {
                "authenticated": True,
                "identity": identity,
                "role": role,
                "scopes": scopes
            }
    return {
        "authenticated": False,
        "error": {
            "code": "INVALID_CREDENTIAL",
            "message": "Authentication credential is invalid"
        }
    }

def authorize(identity_info, required_scope):
    """Internal function to check if the authenticated identity has the required scope."""
    if identity_info is None:
        return False
    return required_scope in identity_info["scopes"]

# MCP Server setup
server = MCPServer("CyberSecurityAuthN")

@server.tool()
def whoami():
    """Return the authenticated identity, role, and scopes."""
    auth_result = authenticate()
    if not auth_result["authenticated"]:
        auth_result["authorized"] = False
        return auth_result
    return {
        "authenticated": True,
        "identity": auth_result["identity"],
        "role": auth_result["role"],
        "scopes": auth_result["scopes"]
    }

@server.tool()
def get_assets():
    """Return the list of assets if the identity has assets:read scope."""
    auth_result = authenticate()
    if not auth_result["authenticated"]:
        auth_result["authorized"] = False
        return auth_result
    if not authorize(auth_result, "assets:read"):
        return {
            "authenticated": True,
            "authorized": False,
            "identity": auth_result["identity"],
            "error": {
                "code": "ACCESS_DENIED",
                "required_scope": "assets:read",
                "message": "Authenticated identity does not have the required scope"
            }
        }
    return {
        "authenticated": True,
        "authorized": True,
        "identity": auth_result["identity"],
        "role": auth_result["role"],
        "required_scope": "assets:read",
        "assets": ASSETS
    }

@server.tool()
def search_events(severity: str = None):
    """Return events, optionally filtered by severity (case-insensitive). Requires events:read scope."""
    auth_info = authenticate()
    if auth_info is None:
        return {
            "authenticated": False,
            "authorized": False,
            "error": {
                "code": "AUTHENTICATION_REQUIRED",
                "message": "No authentication credential was provided"
            }
        }
    if not authorize(auth_info, "events:read"):
        return {
            "authenticated": True,
            "authorized": False,
            "identity": auth_info["identity"],
            "error": {
                "code": "ACCESS_DENIED",
                "required_scope": "events:read",
                "message": "Authenticated identity does not have the required scope"
            }
        }
    # Filter events by severity if provided
    filtered_events = EVENTS
    if severity is not None:
        filtered_events = [e for e in EVENTS if e["severity"].lower() == severity.lower()]
    return {
        "authenticated": True,
        "authorized": True,
        "identity": auth_info["identity"],
        "role": auth_info["role"],
        "required_scope": "events:read",
        "applied_filters": {"severity": severity} if severity else {},
        "result_count": len(filtered_events),
        "events": filtered_events
    }

@server.tool()
def get_security_summary():
    """Return a summary of security events. Requires summary:read scope."""
    auth_info = authenticate()
    if auth_info is None:
        return {
            "authenticated": False,
            "authorized": False,
            "error": {
                "code": "AUTHENTICATION_REQUIRED",
                "message": "No authentication credential was provided"
            }
        }
    if not authorize(auth_info, "summary:read"):
        return {
            "authenticated": True,
            "authorized": False,
            "identity": auth_info["identity"],
            "error": {
                "code": "ACCESS_DENIED",
                "required_scope": "summary:read",
                "message": "Authenticated identity does not have the required scope"
            }
        }
    total_events = len(EVENTS)
    severity_counts = {}
    for event in EVENTS:
        sev = event["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    return {
        "authenticated": True,
        "authorized": True,
        "identity": auth_info["identity"],
        "role": auth_info["role"],
        "required_scope": "summary:read",
        "total_events": total_events,
        "severity_counts": severity_counts
    }

if __name__ == "__main__":
    server.run()