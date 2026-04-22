from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.copywriting import router as copywriting_router
from app.core.exceptions import LLMGenerationError, UnsupportedPlatformError
from app.schemas.common import ErrorResponse

app = FastAPI(title="Copywriting API")
app.include_router(copywriting_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(copywriting_router, prefix="/api/v1")

@app.exception_handler(UnsupportedPlatformError)
def unsupported_platform_handler(_: Request, exc: UnsupportedPlatformError) -> JSONResponse:
    payload = ErrorResponse(message="不支持的平台", detail=str(exc))
    return JSONResponse(status_code=400, content=payload.model_dump())


@app.exception_handler(LLMGenerationError)
def llm_generation_error_handler(_: Request, exc: LLMGenerationError) -> JSONResponse:
    payload = ErrorResponse(message="文案生成失败", detail=str(exc))
    return JSONResponse(status_code=500, content=payload.model_dump())


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Copywriting API is running"}
