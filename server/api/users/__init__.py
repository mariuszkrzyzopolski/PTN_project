from starlette.routing import Route

from .endpoints import Login, Register, Refresh

routes = [
    Route("/login", Login),
    Route("/register", Register),
    Route("/refresh", Refresh)
]
