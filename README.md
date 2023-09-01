# Тестовое задание itworkin.
Ваша задача - написать RESTful API простого мессенджера.
### Техническое задание

##### Реализовать rest api:

Реализуемый функционал:
* Механизм авторизации
* Поиск пользователей
* Возможность отправлять личные сообщения (желательно реализовать с помощью Websockets)
* Настройки пользователя (username, аватар, номер телефона, т.п.)

Для реализации можете использовать любой фреймворк, базу данных и ORM.

### Описание 
## Использованные технологии

- Python
- FastAPI
- Websockets
- Docker
- docker compose

### Инструкция по развертыванию проекта.

1. Клонируйте репозиторий:
```
git@github.com:Yana-K38/task_itworkin.git
```
2. Создать файл .env-non-dev в корне проекта и заполнить его всеми ключами:
```
DB_HOST=db
DB_PORT=5435
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres

POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres


SECRET=zyfgtnhjdf
```
3. Собрать контейнеры:
```
docker compose up -d --build
```
##### После запуска проекта, документация будет доступна по адресу:
```http://127.0.0.1:80/docs/```
```http://127.0.0.1:80/chat/```
