import uuid
from mcp.server import MCPServer

server = MCPServer("CyberSecurityResources")

# Static resource: list of assets
@server.resource("security://assets")
def get_assets():
    assets = [
        {
            "id": "1",
            "hostname": "web-server-01",
            "ip": "192.168.1.10",
            "asset_type": "Web Server",
            "criticality": "High",
            "owner": "IT Team",
            "status": "Active"
        },
        {
            "id": "2",
            "hostname": "db-server-01",
            "ip": "192.168.1.11",
            "asset_type": "Database Server",
            "criticality": "High",
            "owner": "Database Admin",
            "status": "Active"
        },
        {
            "id": "3",
            "hostname": "workstation-01",
            "ip": "192.168.1.20",
            "asset_type": "Workstation",
            "criticality": "Medium",
            "owner": "Employee",
            "status": "Active"
        },
        {
            "id": "4",
            "hostname": "firewall-01",
            "ip": "192.168.1.1",
            "asset_type": "Firewall",
            "criticality": "High",
            "owner": "Security Team",
            "status": "Active"
        }
    ]
    return {"assets": assets}

# Dynamic resource: single asset by ID
@server.resource("security://assets/{asset_id}")
def get_asset(asset_id: str):
    # Simulated lookup
    assets = {
        "1": {
            "id": "1",
            "hostname": "web-server-01",
            "ip": "192.168.1.10",
            "asset_type": "Web Server",
            "criticality": "High",
            "owner": "IT Team",
            "status": "Active",
            "details": "Exposed to internet, runs Apache"
        },
        "2": {
            "id": "2",
            "hostname": "db-server-01",
            "ip": "192.168.1.11",
            "asset_type": "Database Server",
            "criticality": "High",
            "owner": "Database Admin",
            "status": "Active",
            "details": "Contains customer data"
        },
        "3": {
            "id": "3",
            "hostname": "workstation-01",
            "ip": "192.168.1.20",
            "asset_type": "Workstation",
            "criticality": "Medium",
            "owner": "Employee",
            "status": "Active",
            "details": "Used by John Doe"
        },
        "4": {
            "id": "4",
            "hostname": "firewall-01",
            "ip": "192.168.1.1",
            "asset_type": "Firewall",
            "criticality": "High",
            "owner": "Security Team",
            "status": "Active",
            "details": "Perimeter firewall"
        }
    }
    if asset_id in assets:
        return assets[asset_id]
    else:
        # Return a controlled structured response for missing asset
        return {
            "error": "Asset not found",
            "asset_id": asset_id,
            "message": f"No asset found with ID {asset_id}"
        }

@server.resource("security://runtime/session")
def get_runtime_session():
    return {
        "session_id": str(uuid.uuid4()),
        "source": "runtime-generated"
    }

# Static resource: recent events
@server.resource("security://events/recent")
def get_recent_events():
    events = [
        {
            "event_id": "evt001",
            "timestamp": "2026-09-07T10:00:00Z",
            "event_type": "Failed SSH Login",
            "severity": "Medium",
            "source_ip": "203.0.113.5",
            "destination_asset": "web-server-01",
            "description": "Multiple failed SSH login attempts from unknown source"
        },
        {
            "event_id": "evt002",
            "timestamp": "2026-09-07T09:30:00Z",
            "event_type": "Malware Detection",
            "severity": "High",
            "source_ip": "192.168.1.20",
            "destination_asset": "workstation-01",
            "description": "Antivirus detected trojan.workstation-01.exe"
        },
        {
            "event_id": "evt003",
            "timestamp": "2026-09-07T09:15:00Z",
            "event_type": "Blocked Connection",
            "severity": "Low",
            "source_ip": "198.51.100.10",
            "destination_asset": "firewall-01",
            "description": "Firewall blocked suspicious outbound connection"
        },
        {
            "event_id": "evt004",
            "timestamp": "2026-09-07T08:45:00Z",
            "event_type": "Authentication Anomaly",
            "severity": "Medium",
            "source_ip": "10.0.0.5",
            "destination_asset": "db-server-01",
            "description": "Unusual login time for service account"
        }
    ]
    return {"events": events}

if __name__ == "__main__":
    server.run()