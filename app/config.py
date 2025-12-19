from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Sequence

import yaml


@dataclass
class ScheduleEntry:
    cron: str
    timezone: str = "UTC"
    visibility: str = "unlisted"


@dataclass
class PerplexityConfig:
    api_key_env: str = "PERPLEXITY_API_KEY"
    model: str = "llama-3.1-sonar-large-128k-online"
    system_prompt: str = (
        "You are helping with uploading TikTok clips to YouTube Shorts. "
        "Write engaging, high-conversion metadata in Russian. "
        "Return concise results and keep hashtags short and relevant."
    )


@dataclass
class UploadDefaults:
    category_id: str = "22"
    tags: List[str] = field(default_factory=list)
    visibility: str = "unlisted"
    description_footer: str = ""


@dataclass
class YouTubeConfig:
    client_secrets_file: Path
    credentials_file: Path


@dataclass
class AppConfig:
    videos_directory: Path
    notes_directory: Optional[Path]
    upload_log: Path
    allowed_extensions: Sequence[str]
    schedule: List[ScheduleEntry]
    perplexity: PerplexityConfig
    youtube: YouTubeConfig
    upload_defaults: UploadDefaults


def _normalize_schedule(raw_schedule: Optional[List[dict]]) -> List[ScheduleEntry]:
    if not raw_schedule:
        return []

    return [
        ScheduleEntry(
            cron=item["cron"],
            timezone=item.get("timezone", "UTC"),
            visibility=item.get("visibility", "unlisted"),
        )
        for item in raw_schedule
    ]


def load_config(path: Path) -> AppConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    raw = yaml.safe_load(path.read_text(encoding="utf-8"))

    videos_directory = Path(raw["videos_directory"]).expanduser()
    notes_directory = None
    if raw.get("notes_directory"):
        notes_directory = Path(raw["notes_directory"]).expanduser()

    perplexity_raw = raw.get("perplexity", {})
    perplexity = PerplexityConfig(
        api_key_env=perplexity_raw.get("api_key_env", "PERPLEXITY_API_KEY"),
        model=perplexity_raw.get("model", "llama-3.1-sonar-large-128k-online"),
        system_prompt=perplexity_raw.get(
            "system_prompt",
            (
                "You are helping with uploading TikTok clips to YouTube Shorts. "
                "Write engaging, high-conversion metadata in Russian. "
                "Return concise results and keep hashtags short and relevant."
            ),
        ),
    )

    youtube_raw = raw["youtube"]
    youtube = YouTubeConfig(
        client_secrets_file=Path(youtube_raw["client_secrets_file"]).expanduser(),
        credentials_file=Path(youtube_raw["credentials_file"]).expanduser(),
    )

    upload_defaults_raw = raw.get("upload_defaults", {})
    upload_defaults = UploadDefaults(
        category_id=str(upload_defaults_raw.get("category_id", "22")),
        tags=upload_defaults_raw.get("tags", []),
        visibility=upload_defaults_raw.get("visibility", "unlisted"),
        description_footer=upload_defaults_raw.get("description_footer", ""),
    )

    allowed_extensions = tuple(
        ext.lower() for ext in raw.get("allowed_extensions", [".mp4", ".mov", ".mkv"])
    )

    schedule = _normalize_schedule(raw.get("schedule"))

    return AppConfig(
        videos_directory=videos_directory,
        notes_directory=notes_directory,
        upload_log=Path(raw.get("upload_log", "upload_log.json")).expanduser(),
        allowed_extensions=allowed_extensions,
        schedule=schedule,
        perplexity=perplexity,
        youtube=youtube,
        upload_defaults=upload_defaults,
    )
