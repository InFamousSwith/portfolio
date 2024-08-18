# Сервис обращений к MOEX
Принимает одну запись из БД, ищет историю торгов, вычисляет показатели доходности идеи, заполняет недостающие поля в БД.

Принимает json 
```
{
'key_id_ticker': '123-12-NVTK',
'ticker': 'NVTK',
'message_date': date(2023, 3, 27),
'act': 'BUY',
'percentage': 93.0,
'expectation_time': 90.0,
}
```
Отдает ответ, обновлена ли БД.

## Запуск сервиса в докере 
Создаем сеть (если ее нет )
```
docker network create --subnet=172.24.0.0/16 telegram
```

Строим образ 
```
docker build -t moex:v1 -f Dockerfile .
```
Запускаем образ в статичной сети 
```
docker run --net telegram --ip 172.24.0.12 -d --name moexer-v1 -v "$PWD":/usr/src -p 9877:5000 moex:v1
```
Если ip не добавлен в БД, добавляем его по [инструкции](https://gitlabsvr.nsd.ru/gitlab/ai/ra/postal/-/issues/6)
