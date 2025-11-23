import jwt
from fastapi import Request
from starlette.authentication import AuthenticationError
from typing import Dict

SECRET_KEY = "mysecretkey"  # ← cambia esto o usa un .env

def decode_jwt_from_request(request: Request) -> Dict:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise AuthenticationError("Missing or invalid Authorization header")

    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")
