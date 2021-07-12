from typing import Union

from aiogram import types

from keyboards.inline.menu_kb import categories_kb, subcategories_kb, item_kb, menu_cd, to_cart_cd, item_cd, count_kb

from loader import dp
from aiogram.dispatcher.filters import Command, Text

from utils.db_api.db_commands import get_item, add_item_in_cart, get_items


#Отправка меню с категориями
@dp.message_handler(Command("menu"))
async def menu(message: types.Message):
    await list_categories(message)


#ФОрмирование сообщения меню
async def list_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await categories_kb()

    if isinstance(message, types.Message):
        await message.answer("Категории товаров", reply_markup=markup)

    elif isinstance(message, types.CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


#Формирование сообщения подкатегорий
async def list_subcategories(callback: types.CallbackQuery, category, **kwargs):
    markup = await subcategories_kb(category)
    await callback.message.edit_reply_markup(markup)


#Добавление товара в коризну в определенном крличестве
@dp.callback_query_handler(to_cart_cd.filter())
async def add_to_cart(call: types.CallbackQuery, callback_data: dict):
    item_id = callback_data.get('item_id')
    count = callback_data.get('count')
    await add_item_in_cart(user_id=int(call.from_user.id), item_id=int(item_id), count=int(count))
    await call.message.edit_text("Товар успешно добавлен в корзину!\n"
                                 "Для того чтобы просмтортеть корзину отправьте /cart")


#Навигация по меню инлайн кнопок
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")
    item_id = callback_data.get("item_id")

    # Список уровней и соответствующих им функций
    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": show_item
    }

    current_level_func = levels[current_level]

    await current_level_func(
        call,
        category=category,
        subcategory=subcategory,
        item_id=int(item_id)
    )


#Отправка информации по товару
@dp.message_handler(Command('show_product'))
async def show_item(message: types.Message):
    item_id = int(message.text.split(' ')[1])
    markup = item_kb(item_id)

    item = await get_item(item_id)
    text = f"Добавить <b>{item.name}</b> за {item.price}руб в корзину ?"
    await message.answer(text, reply_markup=markup)


#Получение аколичества товара через инлайн кнопки
@dp.callback_query_handler(item_cd.filter())
async def count_item(call: types.CallbackQuery, callback_data: dict):
    item_id = callback_data.get("item_id")
    markup = count_kb(item_id=item_id)
    await call.message.edit_text(text="Выберите количество товара", reply_markup=markup)


#Отображение каталога в инлайн моде по категории и подкатегории
@dp.inline_handler(Text(contains="/catalog"))
async def show_catalog(query: types.InlineQuery):
    text = query.query.split(", ")
    await query.answer(
        results=await catalog(category_code=text[1], subcategory_code=text[2]),
        cache_time=5
    )


#Формирование каталога для инлайн мода
async def catalog(category_code, subcategory_code):
    items = await get_items(category_code=category_code, subcategory_code=subcategory_code)
    items_list = []
    for item in items:
        items_list.append({
            "item_name": item.name,
            "price": item.price,
            "id": item.id
        })

    results = []
    for i in items_list:
        results.append(
            types.InlineQueryResultArticle(
                id=i['id'],
                title=i['item_name'],
                description=f"Цена: {i['price']}руб",
                input_message_content=types.InputTextMessageContent(message_text=f"/show_product {i['id']}")
            )
        )
    return results


