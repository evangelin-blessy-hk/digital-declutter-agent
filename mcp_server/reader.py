import os
from mcp_server.filesystem import (
    open_validated_file,
    validate_file_in_root,
)
from mcp_server.text_reader import (
    SUPPORTED_EXTENSIONS as TEXT_EXTENSIONS,
    read_text_file,
)
from mcp_server.pdf_reader import read_pdf_file
from mcp_server.image_reader import (
    SUPPORTED_IMAGE_EXTENSIONS,
    read_image_file,
)


def read_file(path: str, allowed_root: str):
    """
    Validate a file and route it to the appropriate reader.
    """

    file_path = validate_file_in_root(path, allowed_root)

    extension = file_path.suffix.lower()

    if extension in TEXT_EXTENSIONS:
        return read_text_file(file_path)

    if extension == ".pdf":
        return read_pdf_file(file_path)

    if extension in SUPPORTED_IMAGE_EXTENSIONS:
        fd, validated_path = open_validated_file(path, allowed_root)

        try:
            return read_image_file(validated_path, fd)
        finally:
            os.close(fd)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )