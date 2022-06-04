from starlette.routing import Route

from .endpoints import Create, Join, GetRoom, My, Vote

routes = [
    Route("/create", Create),
    Route("/my", My),
    Route("/{room_id}/join", Join),
    Route("/{room_id}", GetRoom),
    Route("/{room_id}/vote", Vote),
]
