from app.core.config import settings
from app.core.exceptions import LLMGenerationError, UnsupportedPlatformError
from app.domain.enums import Platform
from app.domain.strategies.douyin import build_douyin_copywriting
from app.domain.strategies.xiaohongshu import build_xiaohongshu_copywriting
from app.infrastructure.llm.client import LLMClient
from app.schemas.copywriting import CopywritingGenerateRequest, CopywritingGenerateResponse


llm_client = LLMClient(
    provider=settings.llm.provider,
    model_name=settings.llm.model_name,
    base_url=settings.llm.base_url,
    api_key=settings.llm.api_key,
    temperature=settings.llm.temperature,
    timeout=settings.llm.timeout,
)


def generate_copywriting(payload: CopywritingGenerateRequest) -> CopywritingGenerateResponse:
    try:
        if payload.platform == Platform.douyin:
            prompt = build_douyin_copywriting(
                payload.topic,
                payload.tone,
                payload.keywords,
                payload.target_audience,
            )
        elif payload.platform == Platform.xiaohongshu:
            prompt = build_xiaohongshu_copywriting(
                payload.topic,
                payload.tone,
                payload.keywords,
                payload.target_audience,
            )
        else:
            raise UnsupportedPlatformError(f"不支持的平台：{payload.platform}")

        content = llm_client.generate(prompt)
        return CopywritingGenerateResponse(platform=payload.platform, prompt=prompt, content=content)
    except UnsupportedPlatformError:
        raise
    except Exception as exc:
        raise LLMGenerationError("文案生成失败") from exc
