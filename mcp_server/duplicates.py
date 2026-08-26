from pathlib import Path
import hashlib


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
    root = Path(directory)

    files = [path for path in root.rglob("*") if path.is_file()]

    size_groups = {}

    for path in files:
        size = path.stat().st_size
        size_groups.setdefault(size, []).append(path)

    candidates = [
        paths
        for paths in size_groups.values()
        if len(paths) > 1
    ]

    duplicate_groups = []

    for paths in candidates:
        hash_groups = {}

        for path in paths:
            file_hash = calculate_hash(path)
            hash_groups.setdefault(file_hash, []).append(path)

        for file_hash, matching_files in hash_groups.items():
            if len(matching_files) > 1:
                duplicate_groups.append({
                    "hash": file_hash,
                    "size_bytes": matching_files[0].stat().st_size,
                    "files": [str(path) for path in matching_files]
                })

    return duplicate_groups