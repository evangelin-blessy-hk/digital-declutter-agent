import base64
import os
from pathlib import Path

from mcp.types import ImageContent


SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}

MAX_IMAGE_FILE_SIZE = 10_000_000


def read_image_file(path: Path, fd: int) -> ImageContent:
    """
    Read an image from an already-open file descriptor.
    """

    try:
        file_size = os.fstat(fd).st_size

        if file_size > MAX_IMAGE_FILE_SIZE:
            raise ValueError(
                f"Image file is too large to read: {path}"
            )

        image_data = os.read(
            fd,
            MAX_IMAGE_FILE_SIZE + 1,
        )

        if len(image_data) > MAX_IMAGE_FILE_SIZE:
            raise ValueError(
                f"Image file is too large to read: {path}"
            )

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

    except ValueError:
        raise

    except (PermissionError, OSError) as error:
        raise ValueError(
            f"Unable to read image file: {path}"
        ) from error