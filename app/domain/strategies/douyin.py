def build_douyin_copywriting(topic: str, tone: str, keywords: list[str], target_audience: str | None = None) -> str:
    keywords_text = "、".join(keywords) if keywords else "无"
    target_text = target_audience or "未指定"
    return (
        "你是一名资深抖音短视频文案写手，请根据以下信息生成一段适合抖音口播的中文文案，"
        "要求节奏感强、口语化、吸引注意，不要输出额外解释。\n"
        f"主题：{topic}\n"
        f"语气：{tone}\n"
        f"目标人群：{target_text}\n"
        f"关键词：{keywords_text}"
    )
