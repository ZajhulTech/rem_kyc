from fastapi import Depends, HTTPException
from .security_scheme import auth_scheme
from .jwt_decoder import verify_token

def get_current_user(credentials=Depends(auth_scheme)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return payload
