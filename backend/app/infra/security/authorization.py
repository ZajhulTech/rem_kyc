
from fastapi import Depends
from .dependencies import authorize

def Authorize(permission: str):
    return Depends(authorize(permission))
