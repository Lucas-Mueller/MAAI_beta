# Adding a New MCP Server

This document illustrates how to add a new MCP server to the modular structure.

## Step 1: Create a New Server Configuration File

Create a new Python file in the `mcp_servers` directory with your server configuration:

```python
# mcp_servers/my_new_server.py

"""
Configuration for My New Server
"""

from agents.mcp import MCPServerStdio
from .utils import BASE_STORAGE_PATH

# Define your server configuration
mcp_my_new_server = MCPServerStdio(
    name="my-new-server",
    params={
        "command": "my-server-command",
        "args": [
            "--param1", "value1",
            "--param2", "value2"
        ],
        "env": {
            "ENV_VAR1": "value1",
            "ENV_VAR2": "value2"
        }
    },
    client_session_timeout_seconds=120  # Adjust as needed
)

# Optional: Add documentation about available tools
# Available tools:
# - tool1: Description of tool1
# - tool2: Description of tool2
```

## Step 2: Update the Package's `__init__.py`

Update the `mcp_servers/__init__.py` file to export your new server:

```python
"""
MCP Servers Configuration Package
"""

from .arxiv import mcp_arxiv
from .zotero import mcp_zotero
from .filesystem import create_filesystem_server
from .my_new_server import mcp_my_new_server  # Add your new server here
from .utils import run_with_server, BASE_STORAGE_PATH
```

## Step 3: Update Server Config JSON (if using Claude CLI)

If you want to use the server with Claude mcp CLI, update the servers_config.json:

```json
{
  "servers": [
    {
      "name": "arxiv-mcp-server",
      "type": "stdio",
      "params": {
        "command": "arxiv-mcp-server",
        "args": [
          "--storage-path", "/path/to/storage"
        ]
      },
      "client_session_timeout_seconds": 300
    },
    {
      "name": "my-new-server",
      "type": "stdio",
      "params": {
        "command": "my-server-command",
        "args": [
          "--param1", "value1",
          "--param2", "value2"
        ],
        "env": {
          "ENV_VAR1": "value1",
          "ENV_VAR2": "value2"
        }
      },
      "client_session_timeout_seconds": 120
    }
  ]
}
```

## Step 4: Create an Example Script

Create a script that uses your new server:

```python
# use_new_server.py

import asyncio
import shutil

from agents import Agent, Runner
from agents.mcp import MCPServer

# Import your new server
from mcp_servers import mcp_my_new_server, run_with_server


async def run(mcp_server: MCPServer):
    """Function to run an agent with your new server."""
    agent = Agent(
        name="My Assistant",
        model="gpt-4.1-nano",
        instructions="""
        You have access to the tools provided by my-new-server.
        Use these tools to help answer questions.
        """,
        mcp_servers=[mcp_server],
    )

    # Example query for your server
    message = "Use my-new-server to do something interesting"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    """Main function."""
    await run_with_server(
        server=mcp_my_new_server,
        run_func=run,
        workflow_name="My New Server Example"
    )


if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    asyncio.run(main())
```

## Step 5: Using Multiple Servers

To use your new server along with existing ones:

```python
from mcp_servers import mcp_arxiv, mcp_zotero, mcp_my_new_server

# Create agent with access to multiple servers
agent = Agent(
    name="Multi-Server Assistant",
    model="gpt-4.1-nano",
    instructions="Instructions here...",
    mcp_servers=[mcp_arxiv, mcp_my_new_server, mcp_zotero],
)
```

## Benefits of This Approach

1. **Centralized Configuration**: All server configurations are in one place
2. **Consistency**: Standardized way of defining and using servers
3. **Reusability**: Import servers in any script
4. **Modularity**: Easy to add new servers
5. **Documentation**: Documentation lives with the server configuration