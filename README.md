# Bolid Backend

Бэкенд для управления датчиками и событиями.  
Проект реализован на **Django 4.2** с использованием **Django REST Framework**, PostgreSQL и поддержкой загрузки событий из JSON.

---

## Описание проекта

API позволяет:

- CRUD операции для датчиков (`Sensor`) и событий (`Event`);
- Получение событий для конкретного датчика;
- Фильтрацию событий по `temperature` и `humidity`;
- Пагинацию списка событий;
- Импорт событий из JSON-файла;
- Валидацию данных с ограничениями:
  - `Sensor.type` — 1–3;
  - `Event.temperature` — от -273.15 до 5499;
  - `Event.humidity` — от 0 до 100.

> Примечание: При импорте событий из JSON, если датчика с указанным `sensor_id` нет в базе, он автоматически создаётся с `name="N/A"` и `type=0`.

---

## Технологии

- Python 3.11+
- Django 4.2
- Django REST Framework
- PostgreSQL
- Swagger
- Docker
- GitHub Actions
---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/acidrunn3r/Bolid-test-task
cd bolid_backend
````

### 2. Создание виртуального окружения и установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
.venv\Scripts\activate     # Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Настройка PostgreSQL

Создать базу данных и пользователя в PostgreSQL:

```sql
CREATE DATABASE <Название ДБ>;
CREATE USER <Ваш юзернейм> WITH PASSWORD <'Ваш пароль'>;
GRANT ALL PRIVILEGES ON DATABASE <Название ДБ> TO <Ваш юзернейм>;
```


### 4. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя (для админки)

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

Доступ к API:


http://127.0.0.1:8000/api/v1/


Доступ к админке:

http://127.0.0.1:8000/admin/


---
## Запуск через Docker

Проект полностью готов к запуску в Docker. Используется `docker-compose` для поднятия контейнеров Django + PostgreSQL.


### 1. Сборка и запуск

1. Клонируем репозиторий:

```bash
git clone https://github.com/acidrunn3r/Bolid-test-task
cd bolid_backend
```

2. Собираем образы и запускаем контейнеры:

```bash
docker-compose up --build -d
```

* Флаг `--build` пересобирает контейнеры при изменениях.
* Флаг `-d` запускает в фоне.

3. Проверяем статус контейнеров:

```bash
docker-compose ps
```

---

### 2. Настройка Django
Миграции и статика собираются автоматически посредтсвом entrypoint.sh

**Создание суперпользователя:**

```bash
docker-compose exec web python manage.py createsuperuser
```
---

### 3. Доступ к сервисам

* Django API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
* Админка: [http://localhost:8000/admin/](http://localhost:8000/admin/)

> Контейнер PostgreSQL слушает на `db:5432`. В `docker-compose.yml` уже настроены переменные окружения для базы данных.

---

### 4. Остановка и удаление

```bash
docker-compose down
```

* Для очистки данных базы — добавить флаг `-v`:

```bash
docker-compose down -v
```

---

## API

### Датчики (`Sensor`)

| Метод  | URL                     | Описание        |
|--------|-------------------------|-----------------|
| GET    | `/api/v1/sensors/`      | Список датчиков |
| GET    | `/api/v1/sensors/{id}/` | Детали датчика  |
| POST   | `/api/v1/sensors/`      | Создать датчик  |
| PUT    | `/api/v1/sensors/{id}/` | Обновить датчик |
| DELETE | `/api/v1/sensors/{id}/` | Удалить датчик  |

Пример тела POST/PUT:

```json
{
  "id": 1,
  "name": "Датчик 1",
  "type": 2
}
```

### События (`Event`)

| Метод  | URL                    | Описание         |
|--------|------------------------|------------------|
| GET    | `/api/v1/events/`      | Список событий   |
| GET    | `/api/v1/events/{id}/` | Детали события   |
| POST   | `/api/v1/events/`      | Создать событие  |
| PUT    | `/api/v1/events/{id}/` | Обновить событие |
| DELETE | `/api/v1/events/{id}/` | Удалить событие  |

Пример тела POST/PUT:

```json
{
  "sensor_id": 1,
  "name": "N/A",
  "temperature": 20,
  "humidity": 50
}
```

#### Фильтры и пагинация

Поддерживаются query params:

* `?sensor_id=1` — фильтр по датчику
* `?temperature_min=10&temperature_max=25` — фильтр по температуре
* `?humidity_min=30&humidity_max=60` — фильтр по влажности
* `?limit=10&offset=0` — пагинация

---

### Импорт событий из JSON

**URL:**

```
POST /api/v1/events/upload-json/
```

**Пример запроса через `curl`:**

```bash
curl -X POST http://127.0.0.1:8000/api/v1/events/upload-json/ \
  -F 'file=@events.json'
```

**Пример успешного ответа:**

```json
{
  "status": "ok",
  "imported_count": 16,
  "imported_events": {
    "imported": [246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261],
    "failed": [
      {
        "sensor_id": 1,
        "error": {
          "humidity": ["Убедитесь, что это значение меньше либо равно 100."]
        }
      },
      {
        "sensor_id": 3,
        "error": {
          "temperature": ["Убедитесь, что это значение меньше либо равно 5499.0."]
        }
      },
      {
        "sensor_id": 5,
        "error": {
          "name": ["Название события может содержать только русские и латинские буквы, цифры, _,  и N/A."]
        }
      },
      {
        "sensor_id": 1,
        "error": {
          "temperature": ["Значение “abcde” должно быть числом с плавающей точкой."]
        }
      }
    ]
  },
  "message": "Импорт завершён успешно."
}
```
---
## Swagger

Интерактивная документация по API доступна через Swagger UI:
[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) или http://localhost:8000/swagger/


### Возможности

- Просмотр всех эндпоинтов для `Sensor` и `Event`.
- Тестирование CRUD операций прямо из браузера.
- Загрузка JSON-файлов через `/api/v1/events/upload-json/`.
- Валидация всех полей моделей:
  - `Sensor.type` — значения от 1 до 3;
  - `Event.temperature` — от -273.15 до 5499;
  - `Event.humidity` — от 0 до 100.
- Параметры фильтрации (`temperature_min`, `temperature_max`, `humidity_min`, `humidity_max`) и пагинации (`limit`, `offset`) отображаются автоматически.
- Просмотр структуры ответов, включая `imported_events` с детализацией успешных и неудачных импортов.

Swagger позволяет быстро тестировать API и понимать структуру запросов и ответов без необходимости писать `curl` вручную.



---
# Тестирование
Проект включает модульные и интеграционные тесты для моделей и REST API.
## 1. Модели
### SensorModelTest
- Проверяет модель Sensor:
- Создание сенсора с корректными данными
- Валидацию имени сенсора (недопустимые символы)
- Обновление и удаление сенсора 
### EventModelTest
- Проверяет модель Event:
- Создание события, связанного с сенсором
- Обязательность привязки события к сенсору
- Валидацию всех полей события
## 2. API для сенсоров
- SensorAPITest проверяет CRUD-операции через REST API:
- Получение списка сенсоров (GET /sensors/)
- Создание сенсора (POST /sensors/)
- Получение конкретного сенсора (GET /sensors/<id>/)
- Обновление сенсора (PUT /sensors/<id>/)
- Удаление сенсора (DELETE /sensors/<id>/)
## 3. API для событий
- EventAPITest проверяет CRUD-операции для событий:
- Получение списка событий (GET /events/)
- Создание события (POST /events/)
- Получение конкретного события (GET /events/<id>/)
- Обновление события (PUT /events/<id>/)
- Удаление события (DELETE /events/<id>/)
## 4. Загрузка событий из JSON
- UploadJSONTest проверяет возможность массовой загрузки событий:
- Загрузка JSON-файла с массивом событий (POST /events/upload-json/)
- Проверка успешного создания всех событий в базе
## 5. Запуск тестов
### Запуск всех тестов проекта
```bash
python manage.py test
```
*Все тесты написаны с использованием `django.test.TestCase` и `rest_framework.test.APIClient` и покрывают модели, API и функциональность загрузки JSON.*
___
## CI/CD
### Continuous Integration (CI)

Проект настроен для автоматического тестирования через **GitHub Actions**.  

Каждый пуш или pull request в ветку `main` запускает workflow `Django CI`, который выполняет следующие шаги:

1. Поднимает контейнер **PostgreSQL** для тестовой базы.
2. Устанавливает Python-зависимости.
   > Для ускорения сборки используется **кэш pip**, который сохраняет установленные пакеты между запусками workflow. Это позволяет не скачивать все зависимости заново при каждом пуше.
3. Проверяет код на стиль с помощью `flake8`.
4. Применяет миграции и проверяет их корректность.
5. Запускает все **Django-тесты**.
6. Проверяет статические файлы (`collectstatic`).
7. Строит Docker-образ для тестового окружения.
   > Для ускорения сборки используется **кэш Docker-слоёв**.
> `DJANGO_SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` заданы в Secrets в GItHub Actions

Таким образом, проект автоматически проверяется на работоспособность после каждого изменения.
### Continuous Delivery (CD)

Проект настроен на автоматический деплой на **Render** после успешного прохождения CI:

1. После успешного выполнения workflow `Django CI` запускается шаг **Trigger Render Deploy**.
2. GitHub Actions отправляет запрос к API Render для создания нового деплоя.
3. Render поднимает контейнер с приложением, применяет миграции и собирает статические файлы (через `entrypoint.sh`).
4. Сайт становится доступен по публичному [URL](https://bolid-test-task.onrender.com).

> Для CD используются следующие Secrets в GitHub Actions:
>
> * `RENDER_API_KEY` — API-ключ Render
> * `RENDER_SERVICE_ID` — ID сервиса Render

Таким образом, каждое изменение в ветке `main` после успешных тестов автоматически деплоится на продакшн, минимизируя ручные действия.

---
## Логи

* Все предупреждения и ошибки при импорте JSON логируются через `logging`.
* Рекомендуется проверять консоль при загрузке данных.

---

## Админка

* Все модели (`Sensor` и `Event`) доступны в админке Django.
* Можно управлять данными напрямую через UI.

---

## Структура проекта

```
├── .githubs
│   └── workflows
│       └── ci.yml
├── Dockerfile
├── .flake8
├── .gitignore
├── README.md
├── bolid_backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── pyproject.toml
├── requirements.txt
└── sensors
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── filters.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── 0002_alter_event_created_at_alter_event_humidity_and_more.py
    │   └── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── utils.py
    └── views.py
```

---
## Известные баги

* При заходе на /api/v1/events/upload-json/ выводится ошибка 405, так как DRF автоматически посылает запрос GET, и отсутствует форма для загрузки файла. 
  Чтобы загрузить файл, нужно послать любой невалидный запрос, и тогда появится форма *(Лучше пользоваться Swagger)*

___
## Планируемые улучшения

* CD через GitHub Actions

---

## Контакты

Автор: Александр Липов

