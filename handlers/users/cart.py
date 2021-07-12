from typing import Union

from aiogram import types

from keyboards.inline.cart_kb import delete_all_cd, cart_kb, delete_cd, delete_kb, get_count_to_delete_kb
from loader import dp
from aiogram.dispatcher.filters import Command

from utils.db_api.db_commands import get_cart, get_item, delete_from_cart
from utils.db_api.db_models import Cart


#Отправка коризны пользователю
@dp.message_handler(Command("cart"))
async def show_cart(message: types.Message):
    await cart(message)


#Формирует сообщение корзины
async def cart(message: Union[types.Message, types.CallbackQuery], **kwargs):
    cart = await get_cart(user_id=message.from_user.id)
    cart_list = []
    for item in cart:
        item_id = item.item_id
        count = item.count
        item = await get_item(item_id=item_id)

        cart_list.append({"item_id": item_id,
                          "item_name": item.name,
                          "price": item.price,
                          "count": count})
    text = []
    num = 1
    priceSum = 0
    for item in cart_list:
        text.append(f"<b>{num}){item['item_name']}</b> {item['count']} шт.\n"
                    f"{item['price']}руб за 1 шт.")
        num += 1
        priceSum += int(item['price']) * int(item['count'])

    text.append(f"<b>Общая стоимость: {priceSum}руб</b>")
    if isinstance(message, types.Message):
        await message.answer('\n\n'.join(text), reply_markup=cart_kb(user_id=message.from_user.id))
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text('\n\n'.join(text), reply_markup=cart_kb(user_id=message.from_user.id))


#Очистка корзины
@dp.callback_query_handler(delete_all_cd.filter())
async def delete_all_from_cart(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await Cart.delete.where(Cart.user_id == user_id).gino.status()
    await call.message.edit_text('Корзина очищена')


#Выбор товара для изменения его количества
async def choice_item_to_delete_from_cart(call: types.CallbackQuery, user_id, **kwargs):
    markup = await delete_kb(user_id)
    await call.message.edit_text('Выберите товар, у которого вы хотите изменить количество', reply_markup=markup)


#Выбрать количества товарва, чтобы убрать из корзины
async def get_count_to_delete(call: types.CallbackQuery, user_id, item_id, **kwargs):
    markup = await get_count_to_delete_kb(user_id=user_id, item_id=item_id)
    await call.message.edit_text('Какое количество товара убрать из коризны?', reply_markup=markup)


#Удаление из корзины определенное количество товара (уровень 3)
async def remove_from_cart(call: types.CallbackQuery, user_id, item_id, count, **kwargs):
    await delete_from_cart(user_id=user_id, item_id=item_id, count=count)
    await call.message.edit_text('Товар убран из корзины')


#Навигация по меню инлайн кнопок
@dp.callback_query_handler(delete_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    user_id = callback_data.get('user_id')
    item_id = callback_data.get("item_id")
    count = callback_data.get('count')
    print(user_id)

    #Список уровней и соответствующих им функций
    levels = {
        "0": show_cart,
        "1": choice_item_to_delete_from_cart,
        "2": get_count_to_delete,
        "3": remove_from_cart
    }

    current_level_func = levels[current_level]

    await current_level_func(
        call,
        user_id=int(user_id),
        item_id=int(item_id),
        count=int(count)
    )
