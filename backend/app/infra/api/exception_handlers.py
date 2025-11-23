import uuid
import os
import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.infra.api.response import Response

logger = logging.getLogger(__name__)

SHOW_ERRORS = os.getenv("SHOW_ERRORS", "false").lower() == "true"

async def http_exception_handler(request: Request, exc: HTTPException):
    error_id = uuid.uuid4()
    msg = f"ID:{error_id}"

    logger.error(f"[{msg}] HTTPException: {exc.detail}")

    detail_msg = exc.detail if SHOW_ERRORS else f"Error {msg}"

    response = Response.with_error(message=detail_msg, status_code=exc.status_code)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())

async def unhandled_exception_handler(request: Request, exc: Exception):
    error_id = uuid.uuid4()
    msg = f"ID:{error_id}"

    logger.error(f"[{msg}] Unhandled exception", exc_info=exc)

    detail_msg = str(exc) if SHOW_ERRORS else f"Error {msg}"

    response = Response.with_error(message=detail_msg, status_code=HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=response.model_dump())
