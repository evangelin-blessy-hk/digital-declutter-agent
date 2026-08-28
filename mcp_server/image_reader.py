from pathlib import Path
import base64

from mcp.types import ImageContent


SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

MAX_IMAGE_FILE_SIZE = 10_000_000


def read_image_file(path: Path) -> ImageContent:
    """
    Read an image file and return it as MCP ImageContent.
    """

    if path.suffix.lower() not in SUPPORTED_IMAGE_EXTENSIONS:
        raise ValueError(
            f"Unsupported image type: {path.suffix}"
        )

    try:
        file_size = path.stat().st_size
    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to access image file: {path}"
        ) from error

    if file_size > MAX_IMAGE_FILE_SIZE:
        raise ValueError(
            f"Image file is too large to read: {path}"
        )

    try:
        image_data = path.read_bytes()
        encoded_data = base64.b64encode(image_data).decode("ascii")

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }

        return ImageContent(
            type="image",
            data=encoded_data,
            mimeType=mime_types[path.suffix.lower()],
        )

    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to read image file: {path}"
        ) from error