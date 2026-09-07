from mcp.server import MCPServer
import ipaddress
import re

server = MCPServer("CyberSecurityMultiTool")

# Simulated threat intelligence database
THREAT_DB = {
    "8.8.8.8": {"reputation": "benign", "confidence": 0.95, "source": "internal"},
    "185.220.101.5": {"reputation": "malicious", "confidence": 0.9, "source": "internal"},
}

# Simulated malware hash database
HASH_DB = {
    # Example known malicious MD5 hash (EICAR test file)
    "44d88612fea8a8f36de82e1278abb02f": {
        "hash_type": "MD5",
        "status": "malicious",
        "malware_family": "EICAR-Test-File",
        "confidence": 0.99,
        "source": "internal",
    }
}

def validate_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

@server.tool()
def check_ip(ip: str) -> dict:
    """Check IP address reputation."""
    if not validate_ip(ip):
        return {
            "error": "Invalid IP address format",
            "ip": ip,
            "ip_version": None,
            "reputation": "invalid",
            "confidence": 0.0,
            "source": "validation"
        }
    ip_obj = ipaddress.ip_address(ip)
    ip_version = ip_obj.version
    info = THREAT_DB.get(ip, {"reputation": "unknown", "confidence": 0.5, "source": "internal"})
    return {
        "ip": ip,
        "ip_version": ip_version,
        "reputation": info["reputation"],
        "confidence": info["confidence"],
        "source": info["source"]
    }

def validate_hash(hash_str: str) -> tuple[bool, str]:
    """Validate hash and return (is_valid, hash_type)."""
    hash_str = hash_str.lower()
    # MD5: 32 hex chars
    if re.fullmatch(r'[0-9a-f]{32}', hash_str):
        return True, "MD5"
    # SHA1: 40 hex chars
    if re.fullmatch(r'[0-9a-f]{40}', hash_str):
        return True, "SHA1"
    # SHA256: 64 hex chars
    if re.fullmatch(r'[0-9a-f]{64}', hash_str):
        return True, "SHA256"
    return False, ""

@server.tool()
def check_hash(hash_value: str) -> dict:
    """Check hash against malware database."""
    is_valid, hash_type = validate_hash(hash_value)
    if not is_valid:
        return {
            "error": "Invalid hash format",
            "hash": hash_value,
            "hash_type": None,
            "status": "invalid",
            "malware_family": None,
            "confidence": 0.0,
            "source": "validation"
        }
    info = HASH_DB.get(hash_value.lower(), {
        "hash_type": hash_type,
        "status": "unknown",
        "malware_family": None,
        "confidence": 0.5,
        "source": "internal"
    })
    return {
        "hash": hash_value,
        "hash_type": info["hash_type"],
        "status": info["status"],
        "malware_family": info["malware_family"],
        "confidence": info["confidence"],
        "source": info["source"]
    }

# Simple SSH failed login pattern
SSH_FAILED_PATTERN = re.compile(
    r"Failed password for (?P<username>\S+).*from\s+(?P<source_ip>[^\s]+).*ssh2",
    re.IGNORECASE
)

@server.tool()
def analyze_log(log_line: str) -> dict:
    """Analyze a log line for SSH failed login attempts."""
    match = SSH_FAILED_PATTERN.search(log_line)
    if match:
        source_ip = match.group("source_ip")
        username = match.group("username")
        # Validate IP
        try:
            ipaddress.ip_address(source_ip)
            ip_valid = True
        except ValueError:
            ip_valid = False
        return {
            "source_ip": source_ip if ip_valid else None,
            "username": username,
            "protocol": "SSH",
            "event_type": "failed_login",
            "severity": "medium",
            "confidence": 0.85,
            "source": "pattern_matching"
        }
    else:
        return {
            "source_ip": None,
            "username": None,
            "protocol": None,
            "event_type": "unknown",
            "severity": "info",
            "confidence": 0.0,
            "source": "no_match"
        }

if __name__ == "__main__":
    server.run()