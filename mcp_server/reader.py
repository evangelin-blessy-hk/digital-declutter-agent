from mcp_server.filesystem import validate_file_in_root
from mcp_server.text_reader import (
    SUPPORTED_EXTENSIONS as TEXT_EXTENSIONS,
    read_text_file,
)
from mcp_server.pdf_reader import read_pdf_file


def read_file(path: str, allowed_root: str) -> str:
    """
    Validate a file and route it to the appropriate reader.
    """

    file_path = validate_file_in_root(path, allowed_root)

    extension = file_path.suffix.lower()

    if extension in TEXT_EXTENSIONS:
        return read_text_file(file_path)

    if extension == ".pdf":
        return read_pdf_file(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )