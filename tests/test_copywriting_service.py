import pytest

from app.core.exceptions import LLMGenerationError
from app.domain.enums import Platform
from app.schemas.copywriting import CopywritingGenerateRequest
from app.services import copywriting_service


class DummyLLMClient:
    def __init__(self) -> None:
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return f"mock-result: {prompt}"


def test_generate_copywriting_for_xiaohongshu(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_client = DummyLLMClient()
    monkeypatch.setattr(copywriting_service, "llm_client", dummy_client)

    payload = CopywritingGenerateRequest(
        platform=Platform.xiaohongshu,
        topic="春季护肤",
        tone="natural",
        keywords=["保湿", "敏感肌"],
    )

    result = copywriting_service.generate_copywriting(payload)

    assert result.platform == Platform.xiaohongshu
    assert "小红书风格" in result.content
    assert dummy_client.prompts
    assert "小红书风格" in dummy_client.prompts[0]


def test_generate_copywriting_for_douyin(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_client = DummyLLMClient()
    monkeypatch.setattr(copywriting_service, "llm_client", dummy_client)

    payload = CopywritingGenerateRequest(
        platform=Platform.douyin,
        topic="春季护肤",
        tone="natural",
        keywords=["保湿", "敏感肌"],
    )

    result = copywriting_service.generate_copywriting(payload)

    assert result.platform == Platform.douyin
    assert "抖音风格" in result.content
    assert dummy_client.prompts
    assert "抖音风格" in dummy_client.prompts[0]


def test_generate_copywriting_wraps_unknown_error(monkeypatch: pytest.MonkeyPatch) -> None:
    class BrokenLLMClient:
        def generate(self, prompt: str) -> str:
            raise RuntimeError("boom")

    monkeypatch.setattr(copywriting_service, "llm_client", BrokenLLMClient())

    payload = CopywritingGenerateRequest(
        platform=Platform.xiaohongshu,
        topic="春季护肤",
        tone="natural",
        keywords=[],
    )

    with pytest.raises(LLMGenerationError):
        copywriting_service.generate_copywriting(payload)
