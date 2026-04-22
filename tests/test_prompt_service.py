from app.domain.enums import Platform
from app.domain.strategies.douyin import build_douyin_copywriting
from app.domain.strategies.xiaohongshu import build_xiaohongshu_copywriting


def test_build_xiaohongshu_copywriting() -> None:
    content = build_xiaohongshu_copywriting("春季护肤", "natural", ["保湿", "敏感肌"])
    assert "小红书风格" in content
    assert "保湿、敏感肌" in content


def test_build_douyin_copywriting() -> None:
    content = build_douyin_copywriting("春季护肤", "natural", ["保湿", "敏感肌"])
    assert "抖音风格" in content
    assert "保湿、敏感肌" in content


def test_platform_enum_values() -> None:
    assert Platform.xiaohongshu.value == "xiaohongshu"
    assert Platform.douyin.value == "douyin"
