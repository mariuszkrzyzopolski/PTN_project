from starlette.routing import Mount

from .rooms import routes
from .users import routes

routes = [
    Mount("/users", routes=users.routes),
    Mount("/rooms", routes=rooms.routes)
]
