from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("beatport")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "beatport-mcp/1.0"




if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
