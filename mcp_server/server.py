from mcp.server.mcpserver import MCPServer
from mcp_server.scanner import scan_directory
from mcp_server.duplicates import find_duplicates

mcp = MCPServer("digital-declutter")


@mcp.tool()
def scan_directory_tool(directory: str) -> list[dict]:
    """
    Recursively scan a directory and return basic file information.
    """
    return scan_directory(directory)


@mcp.tool()
def find_duplicate_files(directory: str) -> list[dict]:
    """
    Find files with identical contents inside a directory.
    """
    return find_duplicates(directory)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )