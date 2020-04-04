# Python Imports
from pathlib import Path
# Third-Party Imports
# Project Imports
from src.framework.settings import FILE_DB_ROOT_PATH


def get_absolute_file_path_to_db(relative_path: str) -> Path:
    filepath = FILE_DB_ROOT_PATH.joinpath(relative_path).resolve()
    return filepath
