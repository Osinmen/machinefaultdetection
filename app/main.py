from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.router import api_router
from app.services.model_service import ModelService
from app.core.exceptions import (
    ModelNotLoadedException, FeatureEngineeringException, InvalidInputException,
    model_not_loaded_handler, feature_engineering_handler, invalid_input_handler,
)

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    ModelService.load_model()
    yield
    # Cleanup on shutdown
    ModelService.unload_model()

app = FastAPI(
    title=settings.APP_NAME,
    description="Predictive machine failure detection API",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(ModelNotLoadedException, model_not_loaded_handler)
app.add_exception_handler(FeatureEngineeringException, feature_engineering_handler)
app.add_exception_handler(InvalidInputException, invalid_input_handler)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"app": settings.APP_NAME, "version": settings.APP_VERSION, "status": "running"}
