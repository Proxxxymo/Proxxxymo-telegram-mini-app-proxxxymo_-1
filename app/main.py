import argparse
from pathlib import Path

from .config import load_config
from .uploader import Uploader


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Планировщик загрузки TikTok роликов в YouTube Shorts"
    )
    parser.add_argument(
        "--config",
        default="settings.yaml",
        help="Путь до YAML-конфига (по умолчанию settings.yaml)",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Выполнить одну загрузку немедленно и выйти",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    config = load_config(config_path)

    uploader = Uploader(config)

    if args.once:
        uploader.run_once()
    else:
        uploader.run_schedule()


if __name__ == "__main__":
    main()
