import json
import os
from typing import Iterable, List, Optional

import requests


class PerplexityClient:
    def __init__(self, api_key: str, model: str, system_prompt: str) -> None:
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt

    def generate_metadata(
        self,
        *,
        video_name: str,
        notes: Optional[str],
        fallback_tags: Iterable[str],
    ) -> dict:
        prompt = self._build_prompt(video_name=video_name, notes=notes)
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "response_format": {"type": "json_object"},
            },
            timeout=60,
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        parsed = json.loads(content)

        hashtags: List[str] = parsed.get("hashtags", []) or list(fallback_tags)
        if len(hashtags) < 3 and fallback_tags:
            hashtags = list({*hashtags, *fallback_tags})

        return {
            "title": parsed.get("title", video_name),
            "description": parsed.get("description", ""),
            "hashtags": hashtags,
        }

    def _build_prompt(self, *, video_name: str, notes: Optional[str]) -> str:
        notes_part = notes or (
            "Визуально охарактеризуй ролик по названию файла. "
            "Если информации недостаточно, придумай универсальный заголовок."
        )
        return (
            "Сгенерируй метаданные для YouTube Shorts. "
            "Нужно вернуть JSON с полями: "
            "`title` (до 80 символов), `description` (2-3 предложения + CTA), "
            "`hashtags` (массив из 5-10 коротких хэштегов). "
            f"Название файла: {video_name}. "
            f"Дополнительные заметки: {notes_part}"
        )


def get_api_key(env_name: str) -> str:
    api_key = os.getenv(env_name)
    if not api_key:
        raise RuntimeError(
            f"API ключ Perplexity не найден. Установите переменную окружения {env_name}."
        )
    return api_key
