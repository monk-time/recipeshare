# RecipeShare

### Описание
Онлайн-сервис и API для продуктового помощника. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Сервис размещен по адресу: https://recipeshare.hopto.org/. Полная документация к API находится в файле [docs/openapi-schema.yml](docs/openapi-schema.yml) и доступна по эндпоинту `/api/docs/`.

### Используемые технологии
- Python 3.11
- Django
- Django REST Framework
- PostgreSQL
- Node.js
- React
- Gunicorn
- Nginx
- Docker
- GitHub Actions
- Pytest

### Как развернуть проект локально
1. Клонировать репозиторий:
    ```bash
    git clone git@github.com:monk-time/foodgram-project-react.git
    cd foodgram-project-react/infra/
    ```

#### Отладочный запуск через сервер Django
2. Включить режим отладки и использование базы данных SQLite:
    ```bash
    export DJANGO_DEBUG=True
    export DJANGO_USE_SQLITE=True
    ```
3. Запустить сервер Django. По желанию БД можно заполнить тестовыми данными:
    ```bash
    python manage.py runserver
    python manage.py load
    ```

#### Запуск через Docker Compose
2. Создать в папке infra/ файл `.env` с переменными окружения, заполненный по образцу [.env.example](infra/.env.example).
3. Собрать и запустить докер-контейнеры через Docker Compose:
    ```bash
    docker compose up --build
    ```

### Как развернуть проект на сервере
1. Создать папку recipeshare/ с файлом `.env` в домашней директории сервера, заполненный по образцу [.env.example](infra/.env.example).
    ```bash
    cd ~
    mkdir recipeshare
    nano recipeshare/.env
    ```
2. Настроить в nginx перенаправление запросов на порт 10000:
    ```nginx
    server {
        server_name <...>;
        server_tokens off;

        location / {
            proxy_pass http://127.0.0.1:10000;
        }
    }
    ```
3. Получить HTTPS-сертификат для доменного имени:
    ```nginx
    sudo certbot --nginx
    ```
3. Добавить в GitHub Actions следующие секреты:
    - DOCKER_USERNAME - логин от Docker Hub
    - DOCKER_PASSWORD - пароль от Docker Hub
    - SSH_KEY - закрытый ssh-ключ для подключения к серверу
    - SSH_PASSPHRASE - passphrase от этого ключа
    - USER - имя пользователя на сервере
    - HOST - IP-адрес сервера
    - TELEGRAM_TO - ID телеграм-аккаунта для оповещения об успешном деплое
    - TELEGRAM_TOKEN - токен телеграм-бота
4. При первом коммите в ветку master будет выполнен полный деплой проекта. Подробнее см. [main.yml](.github/workflows/main.yml).

### Об авторе
Дмитрий Богорад [@monk-time](https://github.com/monk-time)
