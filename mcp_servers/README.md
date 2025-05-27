# MCP Servers Package

This package provides centralized configuration for all Model Context Protocol (MCP) servers used in the project.

## Structure

The package is organized as follows:

- `__init__.py`: Exports all servers and utility functions
- `utils.py`: Contains shared utilities and constants
- `arxiv.py`: Configuration for ArXiv MCP server
- `zotero.py`: Configuration for Zotero MCP server
- `filesystem.py`: Configuration for filesystem MCP server
- `example_adding_server.md`: Documentation for adding new servers

## Available Servers

### ArXiv Server (`mcp_arxiv`)

The ArXiv server provides tools for searching, downloading, and reading academic papers from ArXiv.

Available tools:
- `search_papers`: Search for papers with filters
- `download_paper`: Download a paper by arXiv ID
- `list_papers`: View all downloaded papers
- `read_paper`: Access content of a downloaded paper

### Zotero Server (`mcp_zotero`)

The Zotero server provides access to the user's Zotero reference management library.

### Filesystem Server (`create_filesystem_server()`)

The filesystem server provides access to local files. This is a function that creates a server instance for a specified directory.

## Usage

Import servers individually:

```python
from mcp_servers import mcp_arxiv, mcp_zotero
```

Use the utility function to run with a server:

```python
from mcp_servers import mcp_arxiv, run_with_server

async def run(server):
    # Your agent code here
    pass

await run_with_server(mcp_arxiv, run)
```

Use multiple servers together:

```python
async with mcp_arxiv as arxiv, mcp_zotero as zotero:
    # Your code using both servers
    pass
```

## Adding New Servers

See `example_adding_server.md` for instructions on adding new server types to this package.