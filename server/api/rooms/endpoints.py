from typing import Optional

from pydantic import BaseModel
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from database.database import get_database, DB
from rooms.rooms_service import create_room, join_room, set_topic, joined_rooms

conn = get_database()
database = DB(conn)


class Room(BaseModel):
    name: Optional[str]
    password: Optional[str]
    topic: Optional[str]


class Create(HTTPEndpoint):
    @requires('authenticated')
    async def post(self, request):
        req = await request.json()
        room = Room(**req)
        create_room(database, room.password, request.user.display_name, room.name)
        return JSONResponse({})


class Join(HTTPEndpoint):
    @requires('authenticated')
    async def post(self, request):
        room_id = request.path_params['room_id']
        req = await request.json()
        room = Room(**req)
        join_room(database, room_id, room.password, request.user.display_name)
        return JSONResponse({})


class SetTopic(HTTPEndpoint):
    @requires('authenticated')
    async def patch(self, request):
        room_id = request.path_params['room_id']
        req = await request.json()
        room = Room(**req)
        return JSONResponse(set_topic(database, room_id, room.password, room.topic, request.user.display_name))


class My(HTTPEndpoint):
    @requires('authenticated')
    async def get(self, request):
        return JSONResponse(joined_rooms(database, request.user.display_name))
