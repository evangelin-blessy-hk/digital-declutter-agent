from pathlib import Path
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("digital-declutter")


@mcp.tool()
def scan_directory(directory: str) -> list[dict]:
    """
    Recursively scan a directory and return basic information
    about every file found.

    This tool is read-only. It does not modify any files.
    """

    root = Path(directory).expanduser().resolve()

    if not root.exists():
        raise ValueError(f"Directory does not exist: {root}")

    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {root}")

    results = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        try:
            stat = path.stat()

            results.append({
                "name": path.name,
                "relative_path": str(path.relative_to(root)),
                "extension": path.suffix.lower(),
                "size_bytes": stat.st_size,
            })

        except (PermissionError, OSError):
            continue

    return results


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
    )