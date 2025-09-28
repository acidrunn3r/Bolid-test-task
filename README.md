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
- django-filter

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
CREATE DATABASE bolid_db;
CREATE USER postgres WITH PASSWORD 'pass123';
GRANT ALL PRIVILEGES ON DATABASE bolid_db TO postgres;
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
[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)


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
├── .flake8
├── .gitignore
├── README.md
├── bolid_backend
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── pyproject.toml
├── requirements.txt
└── sensors
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── filters.py
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

* Наличие тестов
* Запуск проекта через Docker 
* CI/CD через GitHub Actions

---

## Контакты

Автор: Александр Липов

