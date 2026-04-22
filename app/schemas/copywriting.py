from pydantic import BaseModel, Field

from app.domain.enums import Platform


class CopywritingGenerateRequest(BaseModel):
    platform: Platform = Field(..., description="平台，例如 xiaohongshu 或 douyin")
    topic: str = Field(..., min_length=1, description="文案主题")
    tone: str = Field(default="natural", description="文案语气")
    target_audience: str | None = Field(default=None, description="目标人群")
    keywords: list[str] = Field(default_factory=list, description="关键词列表")


class CopywritingGenerateResponse(BaseModel):
    platform: Platform
    prompt: str
    content: str
