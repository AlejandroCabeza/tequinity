# Python Imports
# Third-Party Imports
# Project Imports
from src.api.rest.v1_0.routes import routes as rest_v1_0_routes


routes: tuple = (
    *rest_v1_0_routes,
)
