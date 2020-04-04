# Python Imports
from pathlib import Path
# Third-Party Imports
from identify import identify
# Project Imports
from src.files.file_utils import get_absolute_file_path_to_db
from src.framework.settings import ACCEPTED_FILE_TAGS, FILE_MAX_SIZE_BYTES


# Because the files are being uploaded as multipart, we can't rely
# on a content-size verification until we parse the whole file.
# Due to that the only verification (for the moment) is based on the file type.
async def verify_file_pre_write(filename: str) -> bool:
    tags = identify.tags_from_filename(filename)
    return any(tag in ACCEPTED_FILE_TAGS for tag in tags)


# Now that the files have been written we are the content size
# This would be a perfect moment to launch any other cpu-intensive verification asynchronously such as a virus scan.
async def verify_file_post_write(filename: str) -> bool:
    path: Path = get_absolute_file_path_to_db(filename)
    if path.stat().st_size > FILE_MAX_SIZE_BYTES:
        path.unlink()
        return False
    return True
