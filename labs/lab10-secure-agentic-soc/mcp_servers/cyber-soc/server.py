from mcp.server import MCPServer
import data as soc_data

server = MCPServer("cyber-soc")

@server.tool()
def list_alerts(filter: dict = None) -> dict:
    """List alerts, optionally filtered."""
    alerts = soc_data.list_alerts(filter)
    return {"success": True, "data": alerts}

@server.tool()
def get_alert(alert_id: str) -> dict:
    """Get a specific alert by ID."""
    alert = soc_data.get_alert(alert_id)
    if alert is None:
        return {
            "success": False,
            "error": {
                "code": "ALERT_NOT_FOUND",
                "message": f"Alert {alert_id} not found"
            }
        }
    return {"success": True, "data": alert}

@server.tool()
def get_event_chain(alert_id: str) -> dict:
    """Get the event chain for an alert."""
    events = soc_data.get_event_chain(alert_id)
    return {"success": True, "data": events}

@server.tool()
def search_logs(query: str, time_range: dict = None) -> dict:
    """Search logs (not implemented)."""
    results = soc_data.search_logs(query, time_range)
    return {"success": True, "data": results}

# Resources
@server.resource("soc://alerts")
def list_alerts_resource() -> dict:
    """Resource providing list of alert IDs."""
    alerts = soc_data.list_alerts()
    # Return just the IDs for the resource
    alert_ids = [alert["alert_id"] for alert in alerts]
    return {"success": True, "data": alert_ids}

@server.resource("soc://alerts/{alert_id}")
def get_alert_resource(alert_id: str) -> dict:
    """Resource providing a specific alert."""
    alert = soc_data.get_alert(alert_id)
    if alert is None:
        return {
            "success": False,
            "error": {
                "code": "ALERT_NOT_FOUND",
                "message": f"Alert {alert_id} not found"
            }
        }
    return {"success": True, "data": alert}

if __name__ == "__main__":
    server.run()