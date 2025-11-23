from fastapi import Request, Depends
from .jwt_decoder import decode_jwt_from_request
from .auth_exceptions import UnauthorizedException, ForbiddenException

def get_current_user(request: Request):
    try:
        payload = decode_jwt_from_request(request)
        return payload  # puede ser { "sub": "123", "permissions": ["products:view", ...] }
    except Exception:
        raise UnauthorizedException()

def authorize(permission: str):
    def dependency(user=Depends(get_current_user)):
        permissions = user.get("permissions", [])
        if permission not in permissions:
            raise ForbiddenException()
        return user
    return dependency
