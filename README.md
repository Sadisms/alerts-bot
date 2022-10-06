# Alerts-Bot

### Установка(not docker)
ver: Python 3.10.7
```shell
copy .env_alerts.example .env_alerts
python -m venv .venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install -r custom_reqs.txt
python .\migrator.py migrate
```
Заполнить .env_alerts.


### Запуск бота

```shell
python .\app.py
```

### Запуск в контейнере
```shell
docker-compose build --no-cache bot
docker-compose run bot python3 migrator.py migrate
docker-compose up -d 
```