import agents
from agents.mcp import MCPServerStdio
from agents import Agent, Runner
import os
from dotenv import load_dotenv

load_dotenv()

mcp_brave = MCPServerStdio(
    name = "brave-search",
    params={
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
    ],
    "env": {
        "BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")
      },
})