from starlette.routing import Route

from .endpoints import Login, Register

routes = [
    Route("/login", Login),
    Route("/register", Register)
]
