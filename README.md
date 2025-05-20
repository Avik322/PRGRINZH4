# Лабораторная работа № 6  
**CQRS + Kafka + Redis + MongoDB**

## Кратко
Добавлен событийный контур для сообщений:

POST → message_service → Kafka → message_consumer → MongoDB
↑
└── Redis-cache

markdown
Копировать
Редактировать

* **Командная модель** (`message_service`, порт 8083) публикует событие `messages` в Kafka и сбрасывает кэш.  
* **Читательская модель** (`message_consumer`) читает события, пишет их в MongoDB, инвалидирует Redis.

## Запуск

```bash
git clone https://github.com/Avik322/PRGRINZH4.git
cd PRGRINZH4/prgrinzh-main
docker compose up --build -d
Сервис	Порт
Message API	8083
Kafka (external)	9093
Redis	6379
MongoDB	27017

Быстрый тест
bash
Копировать
Редактировать
# создать сообщение
curl -X POST http://localhost:8083/messages \
     -H "Content-Type: application/json" \
     -d '{"sender":"alice","receiver":"bob","text":"hello"}'

# получить по получателю (первый раз из Mongo, затем из Redis)
curl http://localhost:8083/messages/receiver/bob
