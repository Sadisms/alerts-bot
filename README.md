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
Прежде всего нужно будет создать бота в @BotFather и скопировать токен.
Заполнить .env_alerts.

### Авторизация клиента
Переходим на https://my.telegram.org/apps, авторизируемся, далее нам нужны 2 поля "App api_id" и "App api_id" и надо ввести в конфиг.
Потом запускаем авторизацию:
```shell
python .\oauth_tg.py
```
Docker: 
```shell
docker-compose run oauth python3 oauth_tg.py
```

Далее нужно ввести номер телефона, потом нажать Y, далее придёт код в телеграмме его необходимо ввести.

### Запуск бота

```shell
python .\migrator.py migrate
python .\app.py
```

### Запуск в контейнере
```shell
docker-compose build --no-cache bot
docker-compose run bot python3 migrator.py migrate
docker-compose up -d 
```