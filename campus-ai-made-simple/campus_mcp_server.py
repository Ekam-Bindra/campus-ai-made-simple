"""A local, read-only MCP server using fictional campus information."""
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Fictional Campus Tools")

@mcp.tool()
def get_library_hours(day: str) -> str:
    """Return fictional library hours for Friday or Saturday."""
    hours = {"friday": "Closes at 10 PM", "saturday": "Closes at 6 PM"}
    return json.dumps({"fictional": True, "day": day, "hours": hours.get(day.lower(), "Not available")})

@mcp.tool()
def list_campus_events(day: str) -> str:
    """Return fictional sample events for Friday or Saturday."""
    events = {"friday": [{"name": "Coding Circle", "start": "2 PM", "end": "3 PM", "cost": 0}],
              "saturday": [{"name": "Community Garden volunteering", "start": "10 AM", "end": "noon", "cost": 0}]}
    return json.dumps({"fictional": True, "day": day, "events": events.get(day.lower(), [])})

if __name__ == "__main__":
    mcp.run(transport="stdio")
