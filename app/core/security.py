from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque

from fastapi import HTTPException, Request, status

from app.core.config import settings


@dataclass(frozen=True)
class RateLimitRule:
    max_requests: int
    window_seconds: int


class SlidingWindowRateLimiter:
    def __init__(self, rule: RateLimitRule) -> None:
        self.rule = rule
        self._requests: dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        window_start = now - self.rule.window_seconds
        queue = self._requests[key]

        while queue and queue[0] <= window_start:
            queue.popleft()

        if len(queue) >= self.rule.max_requests:
            return False

        queue.append(now)
        return True


_rate_limiter = SlidingWindowRateLimiter(
    RateLimitRule(
        max_requests=settings.rate_limit_max_requests,
        window_seconds=settings.rate_limit_window_seconds,
    )
)


def _is_allowed_origin(origin: str | None) -> bool:
    if not origin:
        return True
    if "*" in settings.cors_allow_origins:
        return True
    return origin in settings.cors_allow_origins


async def guard_public_api(request: Request, call_next) -> object:
    if request.url.path == "/":
        return await call_next(request)

    client_host = request.client.host if request.client else "unknown"
    origin = request.headers.get("origin")

    if not _is_allowed_origin(origin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Origin is not allowed.",
        )

    if not _rate_limiter.allow(client_host):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please slow down.",
        )

    return await call_next(request)
