import os
from _decimal import ROUND_DOWN
from datetime import date
from decimal import Decimal
from typing import Dict, List, Union

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from models import TariffModel

load_dotenv()

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_db = os.getenv('POSTGRES_DB')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_url = f'postgres://{postgres_user}:{postgres_password}@{db_host}:{db_port}/{postgres_db}'


class Tariff(BaseModel):
    date: date
    cargo_type: str
    declared_price: Decimal


class Cost(BaseModel):
    cost: Decimal


class Message(BaseModel):
    message: str


app = FastAPI()


@app.post("/calculate_cost", response_model=Union[Cost, Message])
async def calculate_cost(request: Tariff):
    """ Возвращает стоимость страхования в зависимости от типа груза и объявленной стоимости """

    try:
        month = request.date.month
        year = request.date.year
        date_obj = date(year, month, 1)
        tariff = await TariffModel.get(
            effective_date=date_obj,
            cargo_type=request.cargo_type
        )
        cost = tariff.rate * request.declared_price
        return Cost(cost=cost.quantize(Decimal("0.00"), rounding=ROUND_DOWN))

    except DoesNotExist:
        return {"message": "Не найдена ставка для указанных типа груза и даты!"}


@app.post("/save_tariffs", response_model=Message)
async def save_tariffs(tariffs: Dict[str, List[Dict[str, str]]]):
    """ Эндпойнт для сохранения тарифов в базу данных """

    for effective_date, tariff_list in tariffs.items():
        for tariff in tariff_list:
            await TariffModel.get_or_create(
                effective_date=effective_date,
                cargo_type=tariff['cargo_type'],
                rate=Decimal(tariff['rate']),
            )

    return {"message": "Тарифы успешно сохранены!"}


register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['models']},
    generate_schemas=True,
)
