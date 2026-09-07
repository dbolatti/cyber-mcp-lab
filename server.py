"""CyberSecurityLab MCP Server.

Exposes a tool, resource, and prompt for educational purposes.
"""

from __future__ import annotations

from mcp.server import MCPServer

# Initialize the MCP server
server = MCPServer("CyberSecurityLab")


# Simulated threat intelligence database
THREAT_DB = {
    "8.8.8.8": {"reputation": "benign", "confidence": 0.99},
    "185.220.101.5": {"reputation": "malicious", "confidence": 0.95},
}


@server.tool()
def check_ip(ip: str) -> dict:
    """Check the reputation of an IP address using simulated threat intelligence.

    Args:
        ip: The IP address to check.

    Returns:
        A dictionary with ip, reputation, confidence, and source.
    """
    entry = THREAT_DB.get(ip, {"reputation": "unknown", "confidence": 0.50})
    return {
        "ip": ip,
        "reputation": entry["reputation"],
        "confidence": entry["confidence"],
        "source": "CyberSecurityLab simulated Threat Intelligence",
    }


@server.resource("security://assets")
def security_assets() -> dict:
    """Provide a simulated asset inventory.

    Returns:
        A dictionary mapping asset names to their details.
    """
    return {
        "web-server-01": {
            "ip": "192.168.1.10",
            "type": "web_server",
            "criticality": "high",
        },
        "db-server-01": {
            "ip": "192.168.1.20",
            "type": "database",
            "criticality": "critical",
        },
        "workstation-01": {
            "ip": "192.168.1.100",
            "type": "workstation",
            "criticality": "medium",
        },
    }


@server.prompt()
def investigate_ioc(ioc: str) -> str:
    """Generate a prompt for investigating an IOC.

    Args:
        ioc: The indicator of compromise to investigate.

    Returns:
        A concise instruction string for a cybersecurity analyst.
    """
    return (
        f"Investigate the IOC '{ioc}'. Determine:\n"
        "- IOC reputation\n"
        "- Possible associated threats\n"
        "- Potentially affected assets\n"
        "- Recommended response\n"
        "- Whether escalation is required"
    )


def main() -> None:
    """Run the MCP server."""
    server.run()


if __name__ == "__main__":
    main()