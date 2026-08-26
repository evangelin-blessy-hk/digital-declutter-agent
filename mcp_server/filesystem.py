from pathlib import Path


def get_files(directory: str) -> list[Path]:
    """
    Validate a directory and recursively return all files inside it.
    """

    root = Path(directory).expanduser().resolve()

    if not root.exists():
        raise ValueError(f"Directory does not exist: {root}")

    if not root.is_dir():
        raise ValueError(f"Path is not a directory: {root}")

    return [
        path
        for path in root.rglob("*")
        if path.is_file()
    ]