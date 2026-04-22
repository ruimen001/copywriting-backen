class CopywritingError(Exception):
    pass


class UnsupportedPlatformError(CopywritingError):
    pass


class LLMGenerationError(CopywritingError):
    pass
