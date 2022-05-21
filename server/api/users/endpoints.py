import datetime

import jwt
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse, JSONResponse

from database.database import get_database, DB
from errors import WrongInputException, ExistingUserException, PasswordComplexException
from users.users_service import login, register

conn = get_database()
database = DB(conn)


class Login(HTTPEndpoint):
    async def post(self, request):
        user = await request.json()
        try:
            login(database, user["login"], user["password"])
        except WrongInputException:
            return HTMLResponse(status_code=401, content="Wrong login/password")
        except KeyError:
            return HTMLResponse(status_code=400, content='{"error": "wrong_data"}')
        jwt_payload = jwt.encode(
            {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)},
            user["login"],
        )
        return JSONResponse({"token": jwt_payload})


class Register(HTTPEndpoint):
    async def post(self, request):
        user = await request.json()
        try:
            register(database, user["login"], user["password"])
        except WrongInputException:
            return HTMLResponse(status_code=401, content="Wrong login/password")
        except KeyError:
            return HTMLResponse(status_code=400, content='{"error": "wrong_data"}')
        except ExistingUserException:
            return HTMLResponse(status_code=400, content='{"error": "existing_user"}')
        except PasswordComplexException:
            return HTMLResponse(status_code=400, content='{"error": "password must be more secure"}')
        return JSONResponse({})


class Refresh(HTTPEndpoint):
    async def post(self, request):
        if request.user.is_authenticated:
            jwt_payload = jwt.encode(
                {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)},
            )
