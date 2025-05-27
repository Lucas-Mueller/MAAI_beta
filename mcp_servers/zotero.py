"""
Zotero MCP Server Configuration
"""

from agents.mcp import MCPServerStdio

# Zotero MCP Server Configuration
mcp_zotero = MCPServerStdio(
    name="zotero",
    params={
        "command": "zotero-mcp",
        "args": [],
        "env": {
            "ZOTERO_LOCAL": "true",
            # Add your Zotero API key and library ID if using web API
            # "ZOTERO_API_KEY": "YOUR_API_KEY",
            # "ZOTERO_LIBRARY_ID": "YOUR_LIBRARY_ID",
        },
    },
)

# Available tools for Zotero MCP Server:
# - Search for items in Zotero library
# - Access bibliographic data
# - Read PDFs stored in Zotero
# - Access attached notes and annotations
# - Retrieve citation data