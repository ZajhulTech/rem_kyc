from http.client import HTTPException
from app.infra.api.exceptions import AppException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

# Configurar logging
logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI) -> None:
    """Agregar manejadores globales de excepciones"""
    
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Manejar excepciones personalizadas de la aplicación"""
        logger.warning(f"AppException: {exc.detail} - Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "path": request.url.path
            }
        )
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Manejar excepciones HTTP estándar"""
        logger.warning(f"HTTPException: {exc.detail} - Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.detail,
                "path": request.url.path
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Manejar cualquier otra excepción no capturada"""
        logger.error(f"Unhandled Exception: {str(exc)} - Path: {request.url.path}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Error interno del servidor",
                "path": request.url.path
            }
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Manejar errores de valor"""
        logger.warning(f"ValueError: {str(exc)} - Path: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": True,
                "message": str(exc),
                "path": request.url.path
            }
        )