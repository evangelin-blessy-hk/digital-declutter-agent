from pathlib import Path

def validate_file_in_root(path: str, allowed_root: str) -> Path:
    """
    Validate that a file exists inside the allowed root directory.
    """

    root = Path(allowed_root).expanduser().resolve()
    file_path = Path(path).expanduser().resolve()

    if not root.exists():
        raise ValueError(f"Allowed root does not exist: {root}")

    if not root.is_dir():
        raise ValueError(f"Allowed root is not a directory: {root}")

    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    try:
        file_path.relative_to(root)
    except ValueError:
        raise ValueError(
            f"File is outside the allowed directory: {file_path}"
        )

    return file_path

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