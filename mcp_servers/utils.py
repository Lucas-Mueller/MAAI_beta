"""
Utility functions and constants for MCP servers
"""

import os
import asyncio
from typing import Callable, Awaitable, Any, Optional

from agents.mcp import MCPServerStdio

# Base storage path for all data
BASE_STORAGE_PATH = "/Users/lucasmuller/Desktop/Githubg/MAAI_Tryout/mcp_server_data"

# Create necessary directories
os.makedirs(BASE_STORAGE_PATH, exist_ok=True)
os.makedirs(os.path.join(BASE_STORAGE_PATH, "arxiv"), exist_ok=True)


async def run_with_server(
    server: MCPServerStdio,
    run_func: Callable[[MCPServerStdio], Awaitable[Any]],
    workflow_name: str = "MCP Example",
    trace_func = None
):
    """
    Run an agent with the specified MCP server.
    
    Args:
        server: The MCP server to use
        run_func: Function that takes a server and runs the agent
        workflow_name: Name for the trace
        trace_func: Optional custom trace function (defaults to agents.trace)
    """
    from agents import gen_trace_id, trace
    
    if trace_func is None:
        trace_func = trace
    
    async with server as server_instance:
        trace_id = gen_trace_id()
        with trace_func(workflow_name=workflow_name, trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}\n")
            try:
                await run_func(server_instance)
            except Exception as e:
                print(f"Error running server: {str(e)}")
                raise