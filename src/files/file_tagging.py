# Python Imports
from pathlib import Path
# Third-Party Imports
from identify import identify
# Project Imports
from src.framework.settings import ACCEPTED_CODE_FILE_TAGS


def get_accepted_code_file_tags_from_filename(path: Path):
    tags = identify.tags_from_filename(str(path.resolve()))
    return (tag for tag in tags if tag in ACCEPTED_CODE_FILE_TAGS)
