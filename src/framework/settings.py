# Python Imports
import json
from pathlib import Path
# Third-Party Imports
# Project Imports


with open("../settings.json", "r") as settings_file:
    app_settings = json.loads(settings_file.read())


# SERVER
SERVER_HOST: str = app_settings["SERVER"]["HOST"]
SERVER_PORT: int = app_settings["SERVER"]["PORT"]


# FILES DATABASE
FILE_DB_ROOT: str = app_settings["FILES"]["DATABASE"]["ROOT_DIRECTORY"]
FILE_DB_ROOT_PATH: Path = Path(FILE_DB_ROOT)
FILE_DB_ROOT_PATH.mkdir(parents=True, exist_ok=True)  # Initialise the directory if it doesn't exist


# FILE TYPES
PYTHON_FILE_TAG: str = app_settings["FILES"]["TAGS"]["PYTHON"]
JAVASCRIPT_FILE_TAG: str = app_settings["FILES"]["TAGS"]["JAVASCRIPT"]


ACCEPTED_CODE_FILE_TAGS: (str,) = (
    PYTHON_FILE_TAG,
    JAVASCRIPT_FILE_TAG
)

ACCEPTED_FILE_TAGS: (str,) = (
    *ACCEPTED_CODE_FILE_TAGS,
    app_settings["FILES"]["TAGS"]["PLAIN-TEXT"],
    app_settings["FILES"]["TAGS"]["IMAGE"]
)


# FILE SIZE
FILE_MAX_SIZE_BYTES: int = app_settings["FILES"]["MAX_SIZE_BYTES"]


# CODE EXECUTION
RUN_DETACHED_DEFAULT: bool = app_settings["CODE_EXECUTION"]["RUN_DETACHED_DEFAULT"]
