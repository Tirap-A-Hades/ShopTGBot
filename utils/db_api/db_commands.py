from typing import List

from asyncpg import UniqueViolationError

from utils.db_api.db_models import Item, Cart
from sqlalchemy import and_


#Добавляет товар в таблицу всех товаров
async def add_item(**kwargs):
    newitem = await Item(**kwargs).create()
    return newitem


#Добавляет товар в таблицу коризны к id пользователя
async def add_item_in_cart(user_id: int, item_id: int, count: int):
    cart = await get_cart(user_id=user_id)
    for item in cart:
        if item_id == item.item_id:
            await Cart.update.values(count=item.count+count).where(and_(Cart.user_id == user_id, Cart.item_id == item_id)).gino.status()
            return item
    item_in_cart = await Cart(user_id=user_id, item_id=item_id, count=count).create()
    return item_in_cart


#Возвращает список категорий
async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino.all()


#Возвращает список подкатегорий
async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino.all()


#Возвращает список товаров определненных категории и подкатегории
async def get_items(category_code, subcategory_code) -> List[Item]:
    items = await Item.query.where(and_(Item.category_code == category_code,
                                        Item.subcategory_code == subcategory_code)).gino.all()
    return items


#Возвращает товар по его id
async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


#Возвращает список товаров из коризны определнного пользователя по его id
async def get_cart(user_id) -> List[Cart]:
    cart = await Cart.query.where(Cart.user_id == user_id).gino.all()
    return cart


#Возвращает количество какого-то товара в корзине
async def get_count(user_id: int, item_id: int):
    cart = await Cart.query.where(Cart.user_id == user_id).gino.all()
    for item in cart:
        if item.item_id == item_id:
            return item.count


#Удалаяет из корзины определенное количество товара пользователя
async def delete_from_cart(user_id: int, item_id: int, count: int):
    cart = await get_cart(user_id)
    for item in cart:
        if item.item_id == item_id and item.count == count:
            await Cart.delete.where(and_(Cart.user_id == user_id, Cart.item_id == item_id)).gino.status()
        elif item.item_id == item_id and item.count > count:
            await Cart.update.values(count=item.count-count).where(and_(Cart.user_id == user_id, Cart.item_id == item_id)).gino.status()
        elif item.item_id == item_id and item.count < count:
            break


#Удаляет из корзины все товары пользователя
async def delete_all_from_cart(user_id: int):
    await Cart.delete.where(Cart.user_id == user_id).gino.status()


