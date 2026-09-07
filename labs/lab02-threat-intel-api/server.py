import os
import ipaddress
import requests
from dotenv import load_dotenv
from mcp.server import MCPServer

load_dotenv()  # Load environment variables from .env

server = MCPServer("CyberSecurityThreatIntel")

@server.tool()
def check_ip(ip: str) -> dict:
    """
    Check an IP address against AbuseIPDB.
    
    Args:
        ip: IP address string (IPv4 or IPv6)
        
    Returns:
        Normalized dictionary with threat intelligence data
    """
    # Validate IP address
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return {"error": "Invalid IP address"}
    
    # Get API key from environment
    API_KEY = os.getenv("ABUSEIPDB_API_KEY")
    if not API_KEY:
        return {"error": "API key not configured"}
    
    # Prepare request
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }
    params = {
        "ipAddress": str(ip_obj),
        "maxAgeInDays": 90
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return {"error": "Request timeout"}
    except requests.exceptions.HTTPError:
        return {"error": "HTTP error"}
    except requests.exceptions.RequestException:
        return {"error": "Request failed"}
    
    try:
        data = response.json()
    except ValueError:
        return {"error": "Malformed JSON response"}
    
    # Check if we have the expected structure
    if "data" not in data:
        return {"error": "Unexpected response structure"}
    
    abuse_data = data["data"]
    
    # Normalize response
    result = {
        "ip": abuse_data.get("ipAddress"),
        "ip_version": ip_obj.version,
        "public": abuse_data.get("isPublic", True),
        "abuse_confidence_score": abuse_data.get("abuseConfidenceScore"),
        "country_code": abuse_data.get("countryCode"),
        "usage_type": abuse_data.get("usageType"),
        "isp": abuse_data.get("isp"),
        "domain": abuse_data.get("domain"),
        "total_reports": abuse_data.get("totalReports"),
        "last_reported_at": abuse_data.get("lastReportedAt"),
        "source": "AbuseIPDB"
    }
    
    # Replace empty strings with None for consistency
    for key, value in result.items():
        if value == "":
            result[key] = None
    
    return result

if __name__ == "__main__":
    server.run()