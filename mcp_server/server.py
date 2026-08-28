from mcp.server.mcpserver import MCPServer
from mcp_server.scanner import scan_directory as scan_directory_fn
from mcp_server.duplicates import find_duplicates
from mcp_server.reader import read_text_file

mcp = MCPServer("digital-declutter")

@mcp.tool()
def scan_directory(directory: str) -> list[dict]:
    """
    Recursively scan a directory and return basic file information.
    """
    return scan_directory_fn(directory)


@mcp.tool()
def find_duplicate_files(directory: str) -> list[dict]:
    """
    Find files with identical contents inside a directory.
    """
    return find_duplicates(directory)


@mcp.tool(name="read_file")
def read_file_tool(path: str) -> str:
    """
    Read the contents of a supported text file.
    """
    return read_text_file(path)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )