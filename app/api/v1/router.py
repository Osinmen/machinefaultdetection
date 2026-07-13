from fastapi import APIRouter
from app.api.v1.endpoints import prediction, health, machines

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(prediction.router, tags=["Prediction"])
api_router.include_router(machines.router, tags=["Machines"])
