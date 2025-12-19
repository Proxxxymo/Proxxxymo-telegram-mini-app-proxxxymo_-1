# Планировщик перезаливки TikTok → YouTube Shorts

Скрипт автоматически берет ролики из локальной папки, генерирует заголовок и описание через Perplexity API и загружает их в YouTube Shorts по расписанию.

## Возможности
- Cron-расписание: например, каждый день в 12:00.
- Генерация метаданных (title/description/hashtags) через Perplexity API.
- Логи загруженных роликов, чтобы не дублировать загрузки.
- Поддержка заметок к ролику (`notes/<имя_файла>.txt`) для более точных подсказок модели.

## Подготовка окружения
1) Python 3.10+  
2) Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3) Создайте файл конфигурации:
   ```bash
   cp settings.example.yaml settings.yaml
   ```
4) Переменная окружения с ключом Perplexity:
   ```bash
   export PERPLEXITY_API_KEY="pk-..."  # возьмите ключ в аккаунте Perplexity
   ```
5) OAuth-креды для YouTube:
   - В [Google Cloud Console](https://console.cloud.google.com/apis/credentials) создайте **OAuth Client ID** для Desktop App.
   - Скачайте `client_secret.json` и положите рядом с `settings.yaml`.
   - Первый запуск откроет локальный сервер и браузер для выдачи доступа; после этого появится `token.json`.

## Как запустить
Положите ролики в папку `videos/` (или укажите другую в конфиге). При желании добавьте заметки в `notes/<имя_файла>.txt` — они пойдут в prompt.

Запуск по расписанию (использует cron-строки из `settings.yaml`):
```bash
python -m app.main --config settings.yaml
```

Разовая загрузка ближайшего неотправленного ролика:
```bash
python -m app.main --config settings.yaml --once
```

## Настройка расписания
В блоке `schedule` задаются cron-выражения. Пример — загрузка ежедневно в 12:00 по Москве и публикация сразу в паблик:
```yaml
schedule:
  - cron: "0 12 * * *"
    timezone: "Europe/Moscow"
    visibility: "public"
```
Можно добавить несколько правил (например, 12:00 и 18:00) или оставить список пустым и запускать `--once`.

## Полезные параметры конфига
- `upload_defaults.visibility`: `public`, `unlisted` или `private`.
- `upload_defaults.tags`: базовые теги, которые попадут в описание и список тегов.
- `upload_defaults.description_footer`: подпись, добавляемая к каждому описанию.
- `allowed_extensions`: какие видео-файлы брать из папки.

## Что происходит под капотом
1. Скрипт ищет первый файл в `videos_directory`, который ещё не загружался (учитывается `upload_log.json`).
2. Собирает заметки из `notes_directory` (если есть), отправляет prompt в Perplexity и получает title/description/hashtags.
3. Собирает описание: текст + `description_footer` + хэштеги.
4. Загружает ролик в YouTube Shorts через `youtube.v3.videos.insert`.
5. Логирует успешную загрузку, чтобы не дублировать.

## Отладка
- Проверьте, что `PERPLEXITY_API_KEY` задан и валиден.
- Убедитесь, что включен YouTube Data API v3 и OAuth-креды корректны.
- Для теста без расписания запустите `--once`, чтобы увидеть полный вывод в терминале.
