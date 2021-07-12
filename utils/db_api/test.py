import asyncio

from utils.db_api.db_commands import delete_all_from_cart, get_cart, get_item
from utils.db_api.db_gino import create_db

user_id = 636432020
item_id = 9
count = 2


async def test(user_id):
    cart = await get_cart(int(user_id))
    print(cart)
    for items in cart:
        item = await get_item(items.item_id)
        text = f"{item.name} {items.count}шт"
        print(text)

loop = asyncio.get_event_loop()
loop.run_until_complete(create_db())
loop.run_until_complete(test(user_id))
