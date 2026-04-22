import json
from urllib import error, request


class LLMClient:
    def __init__(
        self,
        provider: str = "mock",
        model_name: str = "deepseek-chat",
        base_url: str | None = "https://api.deepseek.com",
        api_key: str | None = None,
        temperature: float = 0.7,
        timeout: float = 30.0,
    ) -> None:
        self.provider = provider
        self.model_name = model_name
        self.base_url = base_url.rstrip("/") if base_url else None
        self.api_key = api_key
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        if self.provider == "mock":
            return (
                f"[MOCK｜模型：{self.model_name}｜温度：{self.temperature}｜超时：{self.timeout}s] "
                f"{prompt}"
            )

        if not self.base_url:
            raise ValueError("base_url is required")
        if not self.api_key:
            raise ValueError("api_key is required")

        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"LLM HTTP error: {exc.code} {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"LLM network error: {exc.reason}") from exc

        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(f"Unexpected LLM response: {result}") from exc
