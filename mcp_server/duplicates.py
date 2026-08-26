from pathlib import Path
import hashlib
from mcp_server.filesystem import get_files

def calculate_hash(path):
    """
    Calculate the SHA-256 hash of a file.
    """
    sha256 = hashlib.sha256()

    with path.open("rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(directory):
    """
    Find files with identical contents inside a directory.
    """
    files = get_files(directory)

    size_groups = {}

    for path in files:
        try:
            size = path.stat().st_size
            size_groups.setdefault(size, []).append(path)
        except (PermissionError, OSError):
            continue

    candidates = [
        (size, paths)
        for size, paths in size_groups.items()
        if len(paths) > 1
    ]

    duplicate_groups = []

    for size, paths in candidates:
        hash_groups = {}

        for path in paths:
            try:
                file_hash = calculate_hash(path)
            except (PermissionError, OSError):
                continue
            hash_groups.setdefault(file_hash, []).append(path)

        for file_hash, matching_files in hash_groups.items():
            if len(matching_files) > 1:
                duplicate_groups.append({
                    "hash": file_hash,
                    "size_bytes": size,
                    "files": [str(path) for path in matching_files]
                })

    return duplicate_groups