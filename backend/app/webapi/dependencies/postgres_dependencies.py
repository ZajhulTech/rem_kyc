import os
from sqlalchemy import text
from dotenv import load_dotenv

from app.infra.postgresql.postgres_unit_of_work import PostgresUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import logging

load_dotenv() 

DATABASE_URL = os.getenv("POSTGRES_URI")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("db")

logger.info(f"Connecting to PostgreSQL -> {DATABASE_URL}")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

def get_session() -> AsyncSession:
    return async_session_factory()

def get_postgres_unit_of_work() -> PostgresUnitOfWork:
    return PostgresUnitOfWork(session_factory=async_session_factory)

async def log_connection_info():
    async with engine.connect() as conn:

        # Obtener BD y schema actual
        result = await conn.execute(
            text("SELECT current_database(), current_schema();")
        )
        db, schema = result.fetchone()
        logger.info(f"Connected to database: {db}, schema: {schema}")

        # Listar tablas
        tables_result = await conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = :schema
            ORDER BY table_name;
        """), {"schema": schema})

        tables = [row[0] for row in tables_result.fetchall()]

        if tables:
            logger.info(f"Tables in schema '{schema}': {', '.join(tables)}")
        else:
            logger.info(f"No tables found in schema '{schema}'")
