from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

class ModelNotLoadedException(Exception):
    pass

class FeatureEngineeringException(Exception):
    pass

class InvalidInputException(Exception):
    pass

async def model_not_loaded_handler(request: Request, exc: ModelNotLoadedException):
    return JSONResponse(status_code=503, content={"detail": "Model is not loaded. Please try again later."})

async def feature_engineering_handler(request: Request, exc: FeatureEngineeringException):
    return JSONResponse(status_code=422, content={"detail": f"Feature engineering failed: {str(exc)}"})

async def invalid_input_handler(request: Request, exc: InvalidInputException):
    return JSONResponse(status_code=400, content={"detail": f"Invalid input: {str(exc)}"})
