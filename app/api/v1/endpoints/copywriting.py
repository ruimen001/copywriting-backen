from fastapi import APIRouter

from app.schemas.copywriting import (
    CopywritingGenerateRequest,
    CopywritingGenerateResponse,
)
from app.services.copywriting_service import generate_copywriting

router = APIRouter(prefix="/copywriting", tags=["copywriting"])


@router.post("/generate", response_model=CopywritingGenerateResponse)
def generate_copywriting_endpoint(
    payload: CopywritingGenerateRequest,
) -> CopywritingGenerateResponse:
    return generate_copywriting(payload)
