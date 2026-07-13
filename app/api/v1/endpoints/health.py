from fastapi import APIRouter
from app.schemas.response import HealthResponse
from app.services.model_service import ModelService
from app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse, summary="API health check")
def health_check():
    return HealthResponse(
        status="ok",
        model_loaded=ModelService.is_loaded(),
        version=settings.APP_VERSION,
    )
