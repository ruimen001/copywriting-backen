def build_xiaohongshu_copywriting(topic: str, tone: str, keywords: list[str], target_audience: str | None = None) -> str:
    keywords_text = "、".join(keywords) if keywords else "无"
    target_text = target_audience or "未指定"
    return (
        "你是一名资深小红书文案写手，请根据以下信息生成一段适合小红书发布的中文文案，"
        "要求自然、有种草感、适合笔记风格，不要输出额外解释。\n"
        f"主题：{topic}\n"
        f"语气：{tone}\n"
        f"目标人群：{target_text}\n"
        f"关键词：{keywords_text}"
    )
