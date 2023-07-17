## Проект расчета стоимости страхования на FastAPI

REST API сервис по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости.

### Технологии:

Python, FastAPI, Tortoise ORM, Docker, Docker Compose, PostgreSQL, Git

### Запуск проекта на локальной машине:

- Клонировать репозиторий:

```
https://github.com/mikhailsoldatkin/fastapi_app
```

- В директории проекта файл .env.example переименовать в .env и заполнить своими данными:

```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
DB_HOST=db
DB_PORT=5432
```

- Создать и запустить контейнеры Docker

```
docker-compose up -d
```

- Если в директории проекта присутствует файл [tariffs.json](tariffs.json), будет произведена 
загрузка тарифов из него в базу данных.


- После запуска контейнеров будут доступны следующие эндпоинты:

```
POST http://localhost:8000/save_tariffs

{
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.035"
        },
        {
            "cargo_type": "Other",
            "rate": "0.015"
        }
    ]
}

Позволяет сохранить тарифы в базу данных
```

```
POST http://localhost:8000/calculate_cost

{
    "date": "2000-07-17",
    "cargo_type": "Glass",
    "declared_price": "100.50"
}

Позволяет рассчитать стиоимость страхования по типу груза (cargo_type) и его объявленной 
стоимости (declared_price) на запрошенную дату.

Пример ответа:

{
    "cost": "3.51"
}
```

- Для остановки контейнеров Docker:

```
docker-compose down -v      # с их удалением
docker-compose stop         # без удаления
```

### Автор:

Михаил Солдаткин (c) 2023
