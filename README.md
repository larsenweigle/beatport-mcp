# beatport-mcp
[MCP](https://modelcontextprotocol.io/introduction) for the Beatport Developer API. This is currently a WIP. Updates will be posted daily.

## Set Up

**Step 1: Obtaining Your Access Token**

To obtain an access token, you can follow the steps outlined [here](https://api.beatport.com/v4/docs/).

**Step 2: Clone this Repository**

Clone this repository to your local machine

**Step 3: Start up the Beatport MCP server**

You will need to do a couple things for this step.

First, locate the `claude_desktop_config.json` on your local machine. For Mac this can be found at ~/Library/Application\ Support/Claude/claude_desktop_config.json. For Windows, you can find it at %APPDATA%/Claude/claude_desktop_config.json.

Next, update the config JSON file to contain the following:

```json
"beatport": {
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/beatport_mcp",
      "run",
      "beatport-mcp"
    ],
    "env": {
      "CLIENT_ID"=YOUR_CLIENT_ID,
      "ACCESS_TOKEN"=YOUR_ACCESS_TOKEN,
      "REFRESH_TOKEN"=YOUR_REFRESH_TOKEN
    }
  }
```