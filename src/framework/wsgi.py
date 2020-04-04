# Python Imports
# Third-Party Imports
from aiohttp import web
# Project Imports
from src.api.routes import routes
from src.framework.settings import SERVER_PORT, SERVER_HOST


app = web.Application()
app.add_routes(routes)
app.middlewares.append(web.normalize_path_middleware())
web.run_app(app, host=SERVER_HOST, port=SERVER_PORT)
