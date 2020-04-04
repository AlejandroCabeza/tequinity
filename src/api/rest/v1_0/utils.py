# Python Imports
# Third-Party Imports
# Project Imports
from src.framework.settings import RUN_DETACHED_DEFAULT


def parse_run_detached_query_string(query_string) -> bool:
    run_detached_value: str = query_string.get("run_detached")
    try:
        return bool(int(run_detached_value))
    except TypeError:
        return RUN_DETACHED_DEFAULT
