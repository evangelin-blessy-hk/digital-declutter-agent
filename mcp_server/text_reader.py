from pathlib import Path


SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv"}
MAX_TEXT_FILE_SIZE = 1_000_000


def read_text_file(path: Path) -> str:
    """
    Read a supported UTF-8 text file and return its contents.
    """

    try:
        file_size = path.stat().st_size
    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to access file: {path}"
        ) from error

    if file_size > MAX_TEXT_FILE_SIZE:
        raise ValueError(
            f"Text file is too large to read: {path}"
        )

    try:
        return path.read_text(encoding="utf-8")
    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to read text file: {path}"
        ) from error