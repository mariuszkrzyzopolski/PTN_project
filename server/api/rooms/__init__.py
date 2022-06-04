from starlette.routing import Route

from .endpoints import Create, Join, SetTopic, My

routes = [
    Route("/create", Create),
    Route("/my", My),
    Route("/{room_id}/join", Join),
    Route("/{room_id}", SetTopic),

]
