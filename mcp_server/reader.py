from mcp_server.filesystem import validate_file_in_root


TEXT_EXTENSIONS = {".txt", ".md", ".csv"}
MAX_FILE_SIZE = 1_000_000


def read_text_file(path: str, allowed_root: str) -> str:
    """
    Read a supported text file inside an allowed directory.
    """

    file_path = validate_file_in_root(path, allowed_root)

    extension = file_path.suffix.lower()

    if extension not in TEXT_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    try:
        file_size = file_path.stat().st_size
    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to access file: {file_path}"
        ) from error

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File is too large to read: {file_path}"
        )

    try:
        return file_path.read_text(encoding="utf-8")
    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to read file: {file_path}"
        ) from error