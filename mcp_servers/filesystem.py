"""
Filesystem MCP Server Configuration
"""

from agents.mcp import MCPServerStdio
import os

def create_filesystem_server(dir_path=None):
    """
    Create a filesystem MCP server for accessing local files.
    
    Args:
        dir_path: Directory path to serve. If None, uses the sample_files directory.
    
    Returns:
        MCPServerStdio instance configured for filesystem access
    """
    if dir_path is None:
        # Default to sample_files directory if no path provided
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir_path = os.path.join(current_dir, "sample_files")
    
    return MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", dir_path],
        },
    )

# Available tools for Filesystem MCP Server:
# - listFiles: List files in a directory
# - readFile: Read file contents
# - writeFile: Write content to a file
# - deleteFile: Delete a file
# - mkdir: Create a directory