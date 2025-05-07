## Лабораторная работа №5. Redis.

```bash
docker exec -it prgrinzh-main-redis-1 redis-cli
127.0.0.1:6379> GET sender:user1
(nil)
127.0.0.1:6379> GET receiver:user2
(nil)

Запрос

$body = @{
  sender = "user1"
  receiver = "user2"
  content = "hello from redis lab"
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://localhost:8083/messages" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body


Вывод

id
--
681a95f729ee98b64fc0d6f1
