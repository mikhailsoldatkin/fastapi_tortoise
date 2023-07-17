import asyncio
import json
import os

from dotenv import load_dotenv
from tortoise import Tortoise

from models import TariffModel

JSON_FILE_PATH = 'tariffs.json'


async def load_data():
    file_path = JSON_FILE_PATH
    if not os.path.exists(file_path):
        print(f"Файл '{file_path}' не найден!")
        return

    with open('tariffs.json', 'r') as file:
        data = json.load(file)

    for effective_date, tariff_list in data.items():
        for tariff in tariff_list:
            await TariffModel.get_or_create(
                effective_date=effective_date,
                cargo_type=tariff['cargo_type'],
                rate=tariff['rate'],
            )


async def main():
    load_dotenv()

    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_db = os.getenv('POSTGRES_DB')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_url = f'postgres://{postgres_user}:{postgres_password}@{db_host}:{db_port}/{postgres_db}'

    await Tortoise.init(db_url=db_url, modules={'models': ['models']})
    await Tortoise.generate_schemas()

    await load_data()

    await Tortoise.close_connections()


if __name__ == '__main__':
    asyncio.run(main())
