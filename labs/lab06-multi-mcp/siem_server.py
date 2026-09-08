from mcp.server import MCPServer
from typing import Optional, List, Dict, Any

server = MCPServer("CyberSecuritySIEMMulti")

# Simulated SIEM dataset
SIMULATED_EVENTS = [
    {
        "event_id": "evt-001",
        "timestamp": "2026-09-08T10:15:00Z",
        "event_type": "failed_login",
        "severity": "high",
        "source_ip": "185.220.101.5",
        "destination_asset": "web-server-01",
        "username": "admin",
        "description": "Failed SSH login attempt from known malicious IP"
    },
    {
        "event_id": "evt-002",
        "timestamp": "2026-09-08T10:20:00Z",
        "event_type": "firewall_block",
        "severity": "medium",
        "source_ip": "198.51.100.22",
        "destination_asset": "firewall-01",
        "username": "system",
        "description": "Firewall blocked connection attempt from suspicious IP"
    },
    {
        "event_id": "evt-003",
        "timestamp": "2026-09-08T10:25:00Z",
        "event_type": "malware_detection",
        "severity": "critical",
        "source_ip": "10.0.5.45",
        "destination_asset": "workstation-12",
        "username": "john.doe",
        "description": "Malware detected on internal workstation"
    },
    {
        "event_id": "evt-004",
        "timestamp": "2026-09-08T10:30:00Z",
        "event_type": "authentication_anomaly",
        "severity": "high",
        "source_ip": "203.0.113.10",
        "destination_asset": "domain-controller-01",
        "username": "svc_account",
        "description": "Authentication anomaly detected for service account"
    },
    {
        "event_id": "evt-005",
        "timestamp": "2026-09-08T10:35:00Z",
        "event_type": "successful_login",
        "severity": "low",
        "source_ip": "192.168.1.100",
        "destination_asset": "web-server-01",
        "username": "jane.smith",
        "description": "Successful login from trusted internal IP"
    },
    {
        "event_id": "evt-006",
        "timestamp": "2026-09-08T10:40:00Z",
        "event_type": "suspicious_powershell",
        "severity": "medium",
        "source_ip": "10.0.5.45",
        "destination_asset": "workstation-12",
        "username": "john.doe",
        "description": "Suspicious PowerShell execution detected"
    }
]

@server.tool()
def search_events(source_ip: Optional[str] = None, severity: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search simulated SIEM events with optional filters.
    
    Args:
        source_ip: Optional source IP address to filter by
        severity: Optional severity level to filter by (case-insensitive)
    
    Returns:
        List of matching event dictionaries
    """
    results = SIMULATED_EVENTS
    
    if source_ip:
        results = [event for event in results if event["source_ip"] == source_ip]
    
    if severity:
        # Case-insensitive severity matching
        severity_lower = severity.lower()
        results = [event for event in results if event["severity"].lower() == severity_lower]
    
    return results

if __name__ == "__main__":
    server.run()