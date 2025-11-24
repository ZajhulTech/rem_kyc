from app.webapi.dependencies.postgres_dependencies import log_connection_info
from fastapi import FastAPI
from app.infra.api.exception_handlers import add_exception_handlers
from fastapi.exceptions import HTTPException
from app.webapi.routers import verification_router, catalog_router


app = FastAPI(    
    title="My FastAPI App",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    await log_connection_info()

# Registrar handlers globales
add_exception_handlers(app)

app.include_router(verification_router.router)
app.include_router(catalog_router.router)