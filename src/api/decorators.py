# Python Imports
# Third-Party Imports
# Project Imports
from src.api.rest.v1_0.utils import parse_run_detached_query_string


def inject_path_parameter_from_url_path(decorated_method):
    def handler(view, *args, **kwargs):
        path = view.request.match_info["path"]
        return decorated_method(view, path, *args, **kwargs)
    return handler


def inject_run_detached_parameter_from_query_string(decorated_method):
    def handler(view, *args, **kwargs):
        run_detached: bool = parse_run_detached_query_string(view.request.query)
        return decorated_method(view, run_detached=run_detached, *args, **kwargs)
    return handler
