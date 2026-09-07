from mcp.server import MCPServer
from typing import Dict, List, Optional

# Simulated SIEM dataset
SIEM_EVENTS = [
    {
        "event_id": "evt001",
        "timestamp": "2026-09-07T10:15:00Z",
        "event_type": "failed_ssh_auth",
        "severity": "medium",
        "source_ip": "185.220.101.5",
        "destination_asset": "server01.internal.corp",
        "username": "admin",
        "description": "Failed SSH authentication attempt for user admin from 185.220.101.5"
    },
    {
        "event_id": "evt002",
        "timestamp": "2026-09-07T10:20:00Z",
        "event_type": "malware_detection",
        "severity": "high",
        "source_ip": "10.0.5.25",
        "destination_asset": "workstation12.internal.corp",
        "username": "john.doe",
        "description": "Malware detected: Trojan.GenericKD.123456 on workstation12"
    },
    {
        "event_id": "evt003",
        "timestamp": "2026-09-07T10:25:00Z",
        "event_type": "firewall_block",
        "severity": "low",
        "source_ip": "203.0.113.10",
        "destination_asset": "firewall01",
        "username": "system",
        "description": "Firewall blocked connection from 203.0.113.10 to internal web server on port 80"
    },
    {
        "event_id": "evt004",
        "timestamp": "2026-09-07T10:30:00Z",
        "event_type": "authentication_anomaly",
        "severity": "medium",
        "source_ip": "192.168.1.50",
        "destination_asset": "domain-controller01",
        "username": "service_account",
        "description": "Authentication anomaly: service account logging in at unusual hour"
    },
    {
        "event_id": "evt005",
        "timestamp": "2026-09-07T10:35:00Z",
        "event_type": "privilege_escalation",
        "severity": "high",
        "source_ip": "10.0.5.25",
        "destination_asset": "workstation12.internal.corp",
        "username": "john.doe",
        "description": "Privilege escalation attempt via CVE-2021-34527 (PrintNightmare)"
    },
    {
        "event_id": "evt006",
        "timestamp": "2026-09-07T10:40:00Z",
        "event_type": "suspicious_powershell",
        "severity": "medium",
        "source_ip": "10.0.5.30",
        "destination_asset": "workstation15.internal.corp",
        "username": "jane.smith",
        "description": "Suspicious PowerShell execution: Encoded command detected"
    },
    {
        "event_id": "evt007",
        "timestamp": "2026-09-07T10:45:00Z",
        "event_type": "port_scan",
        "severity": "low",
        "source_ip": "198.51.100.22",
        "destination_asset": "network-border",
        "username": "system",
        "description": "Port scan detected from 198.51.100.22 targeting ports 22,80,443,3389"
    },
    {
        "event_id": "evt008",
        "timestamp": "2026-09-07T10:50:00Z",
        "event_type": "successful_login",
        "severity": "info",
        "source_ip": "10.0.5.40",
        "destination_asset": "web-server01",
        "username": "alice.johnson",
        "description": "Successful login to web application from trusted internal IP"
    }
]

def normalize_severity(severity: Optional[str]) -> Optional[str]:
    if severity is None:
        return None
    return severity.lower()

def find_events(severity: Optional[str] = None, event_type: Optional[str] = None, source_ip: Optional[str] = None) -> List[Dict]:
    normalized_severity = normalize_severity(severity)
    results = []
    for event in SIEM_EVENTS:
        match = True
        if normalized_severity and event["severity"] != normalized_severity:
            match = False
        if event_type and event["event_type"] != event_type:
            match = False
        if source_ip and event["source_ip"] != source_ip:
            match = False
        if match:
            results.append(event)
    return results

def get_event_by_id(event_id: str) -> Optional[Dict]:
    for event in SIEM_EVENTS:
        if event["event_id"] == event_id:
            return event
    return None

def calculate_security_summary() -> Dict:
    total_events = len(SIEM_EVENTS)
    events_by_severity = {}
    events_by_type = {}
    unique_source_ips = set()
    high_severity_events = 0
    
    for event in SIEM_EVENTS:
        # Count by severity
        severity = event["severity"]
        events_by_severity[severity] = events_by_severity.get(severity, 0) + 1
        
        # Count by type
        event_type = event["event_type"]
        events_by_type[event_type] = events_by_type.get(event_type, 0) + 1
        
        # Unique source IPs
        unique_source_ips.add(event["source_ip"])
        
        # High severity count
        if severity == "high":
            high_severity_events += 1
     
    return {
        "total_events": total_events,
        "events_by_severity": events_by_severity,
        "events_by_type": events_by_type,
        "unique_source_ips": sorted(unique_source_ips),
        "high_severity_events": high_severity_events
    }


server = MCPServer("CyberSecuritySIEM")

@server.tool()
def get_security_summary() -> Dict:
    return calculate_security_summary()

# Resource: recent events
@server.resource("security://siem/events/recent")
def get_recent_events() -> List[Dict]:
    return SIEM_EVENTS

# Resource: specific event by ID
@server.resource("security://siem/events/{event_id}")
def get_event(event_id: str) -> Dict:
    event = get_event_by_id(event_id)
    if event is None:
        # Return controlled structured response for unknown event
        return {
            "error": "Event not found",
            "event_id": event_id,
            "available_events": [e["event_id"] for e in SIEM_EVENTS]
        }
    return event

# Tool: search events
@server.tool()
def search_events(severity: Optional[str] = None, event_type: Optional[str] = None, source_ip: Optional[str] = None) -> Dict:
    # Validate parameters
    if severity is not None and not isinstance(severity, str):
        return {"error": "severity must be a string"}
    if event_type is not None and not isinstance(event_type, str):
        return {"error": "event_type must be a string"}
    if source_ip is not None and not isinstance(source_ip, str):
        return {"error": "source_ip must be a string"}
    
    # Validate severity value if provided
    if severity is not None:
        allowed = {"info", "low", "medium", "high"}
        if severity.lower() not in allowed:
            return {"error": f"severity must be one of {sorted(allowed)}"}
    
    events = find_events(severity, event_type, source_ip)
    applied_filters = {}
    if severity:
        applied_filters["severity"] = severity.lower()
    if event_type:
        applied_filters["event_type"] = event_type
    if source_ip:
        applied_filters["source_ip"] = source_ip
    
    return {
        "applied_filters": applied_filters,
        "result_count": len(events),
        "events": events
    }

# Run server
if __name__ == "__main__":
    server.run()