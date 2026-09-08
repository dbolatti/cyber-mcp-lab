from mcp.server import MCPServer
import ipaddress
from typing import Dict, Any, Union

server = MCPServer("CyberThreatIntel")

# Simulated threat intelligence reputation database
REPUTATION_DB = {
    "8.8.8.8": {
        "reputation": "benign",
        "confidence": 0.99,
        "source": "simulated-ti"
    },
    "185.220.101.5": {
        "reputation": "malicious",
        "confidence": 0.95,
        "source": "simulated-ti"
    },
    "198.51.100.22": {
        "reputation": "suspicious",
        "confidence": 0.80,
        "source": "simulated-ti"
    }
}

@server.tool()
def check_ip(ip: str) -> Dict[str, Any]:
    """
    Check the reputation of an IP address in the simulated threat intelligence database.
    
    Args:
        ip: IP address string to check
    
    Returns:
        Dictionary containing ip, ip_version, reputation, confidence, and source.
        For invalid IPs, returns an error dictionary with structured error information.
    """
    try:
        # Validate IP address
        ip_obj = ipaddress.ip_address(ip)
        ip_version = f"IPv{ip_obj.version}"
        
        # Look up in reputation database
        if ip in REPUTATION_DB:
            info = REPUTATION_DB[ip]
            return {
                "ip": ip,
                "ip_version": ip_version,
                "reputation": info["reputation"],
                "confidence": info["confidence"],
                "source": info["source"]
            }
        else:
            # Unknown valid IP
            return {
                "ip": ip,
                "ip_version": ip_version,
                "reputation": "unknown",
                "confidence": 0.50,
                "source": "simulated-ti"
            }
    except ValueError:
        # Invalid IP address
        return {
            "error": {
                "code": "INVALID_IP",
                "message": f"'{ip}' is not a valid IP address",
                "ip": ip
            }
        }

if __name__ == "__main__":
    server.run()