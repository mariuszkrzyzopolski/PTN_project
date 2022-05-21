import datetime

import jwt
from starlette.authentication import requires, AuthenticationError, AuthenticationBackend, AuthCredentials
from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse, JSONResponse

from database.database import get_database, DB
from errors import WrongInputException, ExistingUserException, PasswordComplexException
from users.users_service import login, register

conn = get_database()
database = DB(conn)


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "authorization" not in conn.headers:
            return None
        auth = conn.headers["authorization"]
        try:
            scheme, token = auth.split()
        except (ValueError, UnicodeDecodeError):
            raise AuthenticationError('Invalid basic auth credentials')
        try:
            payload = jwt.decode(token, "secret", algorithms="HS256", options={"require": ["exp", "sub"]})
        except jwt.InvalidTokenError:
            raise AuthenticationError('Invalid token')
        return AuthCredentials(["authenticated"]), payload["sub"]


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
            {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15),
             "sub": user["login"]},
            "secret"
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
    @requires('authenticated')
    async def post(self, request):
        try:
            jwt_payload = jwt.encode(
                {"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15),
                 "sub": request.user},
                "secret"
            )
        except AuthenticationError:
            return HTMLResponse(status_code=403, content='Invalid token')
        return JSONResponse({"token": jwt_payload})
