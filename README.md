# Лабораторная работа №4

## Описание

Реализован отдельный микросервис `message_service`, использующий MongoDB (v5.0) для хранения сообщений. Он не связан с клиентскими данными и запускается в составе общей системы с помощью `docker-compose`.

## Состав

- `message_service/` — FastAPI-сервис для работы с сообщениями.
- `message_service/database.py` — подключение к MongoDB.
- `message_service/init_db.py` — инициализация коллекции и индексов.
- `message_service/main.py` — endpoints для CRUD-операций с сообщениями.
- `message_service/models.py` — модель `Message` с sender, receiver, content.
- `message_service/requirements.txt` — зависимости сервиса.
- `docker-compose.yaml` — содержит описание всех сервисов, включая MongoDB.
- `.gitignore` — исключает `.vs/`, `wait-for-it.sh` и другие не нужные файлы.
- `message.json` — пример данных, полученных из GET-запроса.

## Как запускать

```bash
docker-compose up --build
