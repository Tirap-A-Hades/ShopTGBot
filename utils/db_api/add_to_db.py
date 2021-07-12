import asyncio

from utils.db_api.db_commands import add_item
from utils.db_api.db_gino import create_db

print(1)


async def add_items():
    await add_item(name="Apple AirPods",
                   category_name="Наушники", category_code="headphones",
                   subcategory_name="Беспроводные наушники", subcategory_code="wrls headphones",
                   price=15000
                   )

    await add_item(name="JBL T100 TWS",
                   category_name="Наушники", category_code="headphones",
                   subcategory_name="Беспроводные наушники", subcategory_code="wrls headphones",
                   price=4000
                   )

    await add_item(name="SAMSUNG Buds+",
                   category_name="Наушники", category_code="headphones",
                   subcategory_name="Беспроводные наушники", subcategory_code="wrls headphones",
                   price=9000
                   )

    await add_item(name="Sony MDR-EX155",
                   category_name="Наушники", category_code="headphones",
                   subcategory_name="Проводные наушники", subcategory_code="wrd headphones",
                   price=1000
                   )

    await add_item(name="JBL QUANTUM 50",
                   category_name = "Наушники", category_code="headphones",
                   subcategory_name="Проводные наушники", subcategory_code="wrd headphones",
                   price=1200
                   )

    await add_item(name="Intel Core i9-10900 BOX",
                   category_name = "Комплектующие для ПК", category_code="PC accessories",
                   subcategory_name="Процессоры", subcategory_code="CPU",
                   price=35000
                   )

    await add_item(name="AMD Ryzen 7 3800X OEM",
                   category_name = "Комплектующие для ПК", category_code="PC accessories",
                   subcategory_name="Процессоры", subcategory_code="CPU",
                   price=30500
                   )

    await add_item(name="GIGABYTE GeForce RTX 3080 EAGLE",
                   category_name = "Комплектующие для ПК", category_code="PC accessories",
                   subcategory_name="Видеокарты", subcategory_code="GPU",
                   price=190000
                   )

    await add_item(name="ASRock AMD Radeon RX 6900 XT OC Formula",
                   category_name = "Комплектующие для ПК", category_code="PC accessories",
                   subcategory_name="Видеокарты", subcategory_code="GPU",
                   price=180000
                   )


loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(add_items())
