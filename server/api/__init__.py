from starlette.routing import Mount

from .users import routes

routes = [
    Mount("/users", routes=users.routes)
]
