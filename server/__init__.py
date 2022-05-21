import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Mount

from .api import routes
from .api.users.endpoints import BasicAuthBackend

routes = [
    Mount("/api", routes=api.routes, name="api"),
]

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(debug=True, routes=routes, middleware=middleware)


def run_server():
    uvicorn.run("server:app", host="127.0.0.1", port=5000, log_level="info")
