from mcp.server import MCPServer
from typing import Dict, List, Optional, Any

# Simulated identity database
IDENTITY_DB = {
    "alice": {
        "role": "analyst",
        "scopes": ["events:read", "assets:read"]
    },
    "bob": {
        "role": "viewer",
        "scopes": ["assets:read"]
    },
    "carol": {
        "role": "senior_analyst",
        "scopes": ["events:read", "assets:read", "summary:read"]
    }
}

# Simulated security data
ASSETS = ["web-server-01", "db-server-01", "workstation-01"]
EVENTS = [
    {"type": "failed_login", "severity": "high", "source_ip": "185.220.101.5"},
    {"type": "malware_detection", "severity": "critical", "source_ip": "10.0.5.45"},
    {"type": "firewall_block", "severity": "medium", "source_ip": "198.51.100.22"}
]

def get_identity(identity_name: str) -> Optional[Dict]:
    """Retrieve identity from the simulated database."""
    return IDENTITY_DB.get(identity_name)

def has_scope(identity_info: Dict, scope: str) -> bool:
    """Check if the identity info has the required scope."""
    return scope in identity_info["scopes"]

# Initialize MCP server
server = MCPServer("CyberSecurityIAM")

@server.tool()
def get_assets(identity: str) -> Dict[str, Any]:
    """
    Get list of assets.
    Required scope: assets:read
    """
    identity_info = get_identity(identity)
    if identity_info is None:
        return {
            "authorized": False,
            "error": {
                "code": "UNKNOWN_IDENTITY",
                "identity": identity,
                "message": "Unknown identity"
            }
        }
    if not has_scope(identity_info, "assets:read"):
        return {
            "authorized": False,
            "error": {
                "code": "ACCESS_DENIED",
                "identity": identity,
                "required_scope": "assets:read",
                "message": "Identity does not have the required scope"
            }
        }
    
    return {
        "identity": identity,
        "role": identity_info["role"],
        "authorized": True,
        "required_scope": "assets:read",
        "assets": ASSETS
    }

@server.tool()
def search_events(identity: str, severity: Optional[str] = None) -> Dict[str, Any]:
    """
    Search security events with optional severity filter.
    Required scope: events:read
    """
    identity_info = get_identity(identity)
    if identity_info is None:
        return {
            "authorized": False,
            "error": {
                "code": "UNKNOWN_IDENTITY",
                "identity": identity,
                "message": "Unknown identity"
            }
        }
    if not has_scope(identity_info, "events:read"):
        return {
            "authorized": False,
            "error": {
                "code": "ACCESS_DENIED",
                "identity": identity,
                "required_scope": "events:read",
                "message": "Identity does not have the required scope"
            }
        }
    
    # Case-insensitive severity filtering
    filtered_events = EVENTS
    if severity:
        filtered_events = [e for e in EVENTS if e["severity"].lower() == severity.lower()]
    
    return {
        "identity": identity,
        "role": identity_info["role"],
        "authorized": True,
        "required_scope": "events:read",
        "applied_filters": {"severity": severity} if severity else {},
        "result_count": len(filtered_events),
        "events": filtered_events
    }

@server.tool()
def get_security_summary(identity: str) -> Dict[str, Any]:
    """
    Get security summary.
    Required scope: summary:read
    """
    identity_info = get_identity(identity)
    if identity_info is None:
        return {
            "authorized": False,
            "error": {
                "code": "UNKNOWN_IDENTITY",
                "identity": identity,
                "message": "Unknown identity"
            }
        }
    if not has_scope(identity_info, "summary:read"):
        return {
            "authorized": False,
            "error": {
                "code": "ACCESS_DENIED",
                "identity": identity,
                "required_scope": "summary:read",
                "message": "Identity does not have the required scope"
            }
        }
    
    # Calculate summary
    total_events = len(EVENTS)
    severity_counts = {}
    for event in EVENTS:
        sev = event["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    
    return {
        "identity": identity,
        "role": identity_info["role"],
        "authorized": True,
        "required_scope": "summary:read",
        "total_events": total_events,
        "severity_counts": severity_counts
    }

if __name__ == "__main__":
    server.run()