import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from .config import AppConfig, ScheduleEntry
from .perplexity_client import PerplexityClient, get_api_key
from .youtube_client import YouTubeClient


@dataclass
class UploadEntry:
    video_path: str
    youtube_id: str
    uploaded_at: str
    scheduled_for: Optional[str] = None


class UploadLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._entries: Dict[str, UploadEntry] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            for _, entry in data.items():
                upload_entry = UploadEntry(**entry)
                self._entries[upload_entry.video_path] = upload_entry

    def mark_uploaded(
        self, *, video_path: Path, youtube_id: str, scheduled_for: Optional[str]
    ) -> None:
        entry = UploadEntry(
            video_path=str(video_path),
            youtube_id=youtube_id,
            uploaded_at=datetime.now().isoformat(),
            scheduled_for=scheduled_for,
        )
        self._entries[str(video_path)] = entry
        self._persist()

    def already_uploaded(self, video_path: Path) -> bool:
        return str(video_path) in self._entries

    def _persist(self) -> None:
        serialized = {k: asdict(v) for k, v in self._entries.items()}
        self.path.write_text(json.dumps(serialized, indent=2, ensure_ascii=False))


class Uploader:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        api_key = get_api_key(config.perplexity.api_key_env)
        self.perplexity = PerplexityClient(
            api_key=api_key,
            model=config.perplexity.model,
            system_prompt=config.perplexity.system_prompt,
        )
        self.youtube = YouTubeClient(
            client_secrets_file=config.youtube.client_secrets_file,
            credentials_file=config.youtube.credentials_file,
        )
        self.config.videos_directory.mkdir(parents=True, exist_ok=True)
        if self.config.notes_directory:
            self.config.notes_directory.mkdir(parents=True, exist_ok=True)
        self.config.upload_log.parent.mkdir(parents=True, exist_ok=True)
        self.log = UploadLog(config.upload_log)

    def run_once(self, *, override_visibility: Optional[str] = None) -> Optional[dict]:
        video = self._next_video()
        if not video:
            print("Нет новых видео для загрузки.")
            return None

        visibility = override_visibility or self.config.upload_defaults.visibility
        notes = self._load_notes(video)
        metadata = self.perplexity.generate_metadata(
            video_name=video.name,
            notes=notes,
            fallback_tags=self.config.upload_defaults.tags,
        )

        description_footer = self.config.upload_defaults.description_footer.strip()
        full_description = metadata["description"]
        if description_footer:
            full_description = f"{full_description}\n\n{description_footer}"

        hashtags = metadata["hashtags"]
        if hashtags:
            full_description = f"{full_description}\n\n" + " ".join(
                f"#{tag.lstrip('#')}" for tag in hashtags
            )

        upload_response = self.youtube.upload_short(
            video_path=video,
            title=metadata["title"],
            description=full_description,
            tags=hashtags or self.config.upload_defaults.tags,
            category_id=self.config.upload_defaults.category_id,
            visibility=visibility,
        )

        youtube_id = upload_response["id"]
        self.log.mark_uploaded(
            video_path=video,
            youtube_id=youtube_id,
            scheduled_for=datetime.now().isoformat(),
        )
        print(f"Видео {video.name} загружено как https://youtube.com/shorts/{youtube_id}")
        return upload_response

    def _next_video(self) -> Optional[Path]:
        candidates = sorted(
            [
                path
                for path in self.config.videos_directory.iterdir()
                if path.suffix.lower() in self.config.allowed_extensions
            ]
        )

        for candidate in candidates:
            if not self.log.already_uploaded(candidate):
                return candidate
        return None

    def _load_notes(self, video_path: Path) -> Optional[str]:
        if not self.config.notes_directory:
            return None
        notes_file = self.config.notes_directory / f"{video_path.stem}.txt"
        if notes_file.exists():
            return notes_file.read_text(encoding="utf-8")
        return None

    def run_schedule(self) -> None:
        if not self.config.schedule:
            print("Расписание не задано. Выполните run_once или добавьте cron в конфиге.")
            return

        scheduler = BackgroundScheduler()
        for item in self.config.schedule:
            self._add_job(scheduler, item)

        scheduler.start()
        print("Планировщик запущен. Нажмите Ctrl+C для остановки.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("Планировщик остановлен.")

    def _add_job(self, scheduler: BackgroundScheduler, entry: ScheduleEntry) -> None:
        trigger = CronTrigger.from_crontab(entry.cron, timezone=entry.timezone)
        scheduler.add_job(
            self.run_once,
            trigger=trigger,
            kwargs={"override_visibility": entry.visibility},
            name=f"Upload @ {entry.cron} ({entry.timezone})",
        )
        print(f"Запланировано: {entry.cron} ({entry.timezone}) visibility={entry.visibility}")
