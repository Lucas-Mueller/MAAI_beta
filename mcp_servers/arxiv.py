"""
ArXiv MCP Server Configuration
"""

from agents.mcp import MCPServerStdio
from .utils import BASE_STORAGE_PATH

# ArXiv MCP Server using the direct command approach (recommended)
mcp_arxiv = MCPServerStdio(
    name="arxiv-mcp-server",
    params={
        "command": "arxiv-mcp-server",  # Use the direct command
        "args": [
            "--storage-path", BASE_STORAGE_PATH
        ],
    },
    client_session_timeout_seconds=300  # 5 minutes timeout
)

# Alternative configuration using uv
mcp_arxiv_uv = MCPServerStdio(
    name="arxiv-mcp-server-uv",
    params={
        "command": "uv",
        "args": [
            "tool",
            "run",
            "arxiv-mcp-server",
            "--storage-path", BASE_STORAGE_PATH
        ],
    },
    client_session_timeout_seconds=300
)

# Available tools in ArXiv MCP Server:
# 1. search_papers: Search for papers with filters
#    - query: Search term
#    - max_results: Maximum number of results (default: 10)
#    - date_from: Start date (YYYY-MM-DD)
#    - categories: List of arXiv categories (e.g., ["cs.AI", "cs.LG"])
#
# 2. download_paper: Download a paper by arXiv ID
#    - paper_id: arXiv ID (e.g., "2401.12345")
#
# 3. list_papers: View all downloaded papers
#
# 4. read_paper: Access content of a downloaded paper
#    - paper_id: arXiv ID
#
# Special Prompts:
# - deep-paper-analysis: Comprehensive paper analysis workflow
# - paper_id: arXiv ID to analyze