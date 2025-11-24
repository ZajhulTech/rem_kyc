from core.infra.api.response import Response
from fastapi import APIRouter, Depends, Query
from typing import Optional
from core.userstorys.catalog_story import CatalogStory
from core.interfaces.userstorys.catalog_story import ICatalogStory
from webapi.dependencies.postgres_dependencies import get_postgres_unit_of_work

base = "/api/v1/catalogs"
Tag = "Catalogs"
router = APIRouter(tags=[Tag])

# Dependency injector
def get_user_story(uow=Depends(get_postgres_unit_of_work)) -> ICatalogStory:
    return CatalogStory(uow)  # type: ignore


@router.get(base+"/countries",
            response_model=Response,
            tags=[Tag])
async def get_countries(
    code: Optional[str] = Query(None, description="Código del país (ej: MX, US)"),
    catalog_story: CatalogStory = Depends(get_user_story)
):
    """
    Obtiene la lista de países.
    Si se proporciona un código, retorna solo ese país.
    """
    return await catalog_story.get_countries(code)

@router.get(base+"/document-types")
async def get_document_types(
    code: Optional[str] = Query(None, description="Código del tipo de documento (ej: INE, PASSPORT)"),
    catalog_story: CatalogStory = Depends(get_user_story)
):
    """
    Obtiene la lista de tipos de documento.
    Si se proporciona un código, retorna solo ese tipo.
    """
    return await catalog_story.get_document_types(code)

@router.get(base+"/risk-levels")
async def get_risk_levels(
    catalog_story: CatalogStory = Depends(get_user_story)
):
    """
    Obtiene la lista de niveles de riesgo.
    """
    return await catalog_story.get_risk_levels()

@router.get(base+"/verification-statuses")
async def get_verification_statuses(
    catalog_story: CatalogStory = Depends(get_user_story)
):
    """
    Obtiene la lista de estados de verificación.
    """
    return await catalog_story.get_verification_statuses()

@router.get(base+"/all")
async def get_all_catalogs(
    catalog_story: CatalogStory = Depends(get_user_story)
):
    """
    Obtiene todos los catálogos en una sola respuesta.
    """
    return await catalog_story.get_all_catalogs()