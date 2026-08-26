from pathlib import Path
from mcp_server.filesystem import get_files

def scan_directory(directory: str) -> list[dict]:
    """
    Recursively scan a directory and return basic information
    about every file found.

    This function is read-only. It does not modify any files.
    """

    root = Path(directory).expanduser().resolve()
    files = get_files(directory)

    results = []

    for path in files:
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