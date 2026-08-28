from pathlib import Path


TEXT_EXTENSIONS = {".txt", ".md", ".csv"}


def read_text_file(path: str) -> str:
    """
    Read a supported text file and return its contents.
    """

    file_path = Path(path).expanduser().resolve()

    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    extension = file_path.suffix.lower()

    if extension not in TEXT_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    try:
        return file_path.read_text(encoding="utf-8")

    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to read file: {file_path}"
        ) from error