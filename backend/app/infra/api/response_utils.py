# infra/api/response_utils.py
from fastapi.responses import JSONResponse
from app.infra.api.response import Response

def get_response(response: Response):
    if response.success:
        return JSONResponse(status_code=200, content=response.model_dump())
    else:
        return JSONResponse(status_code=400, content=response.model_dump())

def get_custom_response(response: Response):
    if response.success:
        return JSONResponse(status_code=response.status_code or 200, content=response.model_dump())
    else:
        return JSONResponse(status_code=400, content=response.model_dump())
