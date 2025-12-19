from pathlib import Path
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


class YouTubeClient:
    def __init__(self, client_secrets_file: Path, credentials_file: Path) -> None:
        self.client_secrets_file = client_secrets_file
        self.credentials_file = credentials_file
        self.service = self._build_service()

    def _build_service(self):
        creds = None
        if self.credentials_file.exists():
            creds = Credentials.from_authorized_user_file(
                str(self.credentials_file), SCOPES
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.client_secrets_file), SCOPES
                )
                creds = flow.run_local_server(port=8080, prompt="consent")
            self.credentials_file.write_text(creds.to_json(), encoding="utf-8")

        return build("youtube", "v3", credentials=creds)

    def upload_short(
        self,
        *,
        video_path: Path,
        title: str,
        description: str,
        tags: Iterable[str],
        category_id: str,
        visibility: str,
    ) -> dict:
        media = MediaFileUpload(str(video_path), resumable=True)
        body = {
            "snippet": {
                "title": title[:98],
                "description": description[:4900],
                "categoryId": category_id,
                "tags": list(tags),
            },
            "status": {"privacyStatus": visibility},
        }

        try:
            request = (
                self.service.videos()
                .insert(part="snippet,status", body=body, media_body=media)
            )
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Загрузка {int(status.progress() * 100)}%")
            return response
        except HttpError as exc:
            error_reason = exc.error_details if hasattr(exc, "error_details") else exc
            raise RuntimeError(f"Ошибка загрузки в YouTube: {error_reason}") from exc
