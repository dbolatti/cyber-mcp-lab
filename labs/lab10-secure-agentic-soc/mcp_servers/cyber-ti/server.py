from mcp.server import MCPServer
import data as ti_data

server = MCPServer("cyber-ti")

@server.tool()
def reputation_lookup(indicator: str) -> dict:
    """Look up reputation for an indicator."""
    rep = ti_data.reputation_lookup(indicator)
    if rep is None:
        return {
            "success": False,
            "error": {
                "code": "INDICATOR_NOT_FOUND",
                "message": f"No reputation data for indicator {indicator}"
            }
        }
    return {"success": True, "data": rep}

@server.tool()
def ioc_details(ioc_id: str) -> dict:
    """Get details for an IOC."""
    ioc = ti_data.ioc_details(ioc_id)
    if ioc is None:
        return {
            "success": False,
            "error": {
                "code": "IOC_NOT_FOUND",
                "message": f"No IOC details for ID {ioc_id}"
            }
        }
    return {"success": True, "data": ioc}

@server.tool()
def threat_feed_summary() -> dict:
    """Get a summary of the threat feed."""
    summary = ti_data.threat_feed_summary()
    return {"success": True, "data": summary}

# Resources
@server.resource("ti://reputation/{indicator}")
def reputation_resource(indicator: str) -> dict:
    """Resource for reputation lookup."""
    rep = ti_data.reputation_lookup(indicator)
    if rep is None:
        return {
            "success": False,
            "error": {
                "code": "INDICATOR_NOT_FOUND",
                "message": f"No reputation data for indicator {indicator}"
            }
        }
    return {"success": True, "data": rep}

if __name__ == "__main__":
    server.run()