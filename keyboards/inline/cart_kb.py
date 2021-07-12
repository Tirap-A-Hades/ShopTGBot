from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_cart, get_item, get_count

delete_cd = CallbackData('delete', 'level', 'item_id', 'user_id', 'count')
delete_all_cd = CallbackData('delete_all', 'user_id')
buy_cd = CallbackData('buy', 'user_id', 'price')


#Формирует callback data
def make_callback_data(level: int, user_id=0, item_id=0,  count=0):
    return delete_cd.new(level=level,
                         item_id=int(item_id),
                         user_id=int(user_id),
                         count=int(count))


#Инлайн кнопки для коризны (уровень 0)
def cart_kb(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.insert(InlineKeyboardButton(text='Очистить корзину', callback_data=delete_all_cd.new(user_id)))
    markup.insert(InlineKeyboardButton(text="убрать из корзины", callback_data=make_callback_data(level=1, user_id=user_id)))
    # markup.insert(InlineKeyboardButton(text="купить"))

    return markup


#Инлайн кнопки со списком и количеством товара из корзины (уровень 1)
async def delete_kb(user_id):
    markup = InlineKeyboardMarkup(row_width=1)
    cart = await get_cart(int(user_id))
    for items in cart:
        item = await get_item(items.item_id)
        text = f"{item.name} ({items.count}шт)"
        cb = make_callback_data(level=2,
                                user_id=user_id,
                                item_id=items.item_id)

        markup.insert(InlineKeyboardButton(text, callback_data=cb))

    # кнопка назад, возвращает на прошлый уровень
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=0)
        )
    )

    return markup


#Формирование инлайн кнопок для выбора количсетва для удаления товара (уровень 2)
async def get_count_to_delete_kb(user_id, item_id):
    markup = InlineKeyboardMarkup()
    max_count = int(await get_count(int(user_id), int(item_id)))
    #Генерация инлайн кнопок с числами до максимального количества(все количество товара в корзине)
    for i in range(max_count):
        cb = delete_cd.new(level=3,
                           user_id=int(user_id),
                           item_id=int(item_id),
                           count=i+1)
        markup.insert(InlineKeyboardButton(text=f'{i+1}', callback_data=cb))

    #кнопка назад, возвращает на прошлый уровень
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=1)
        )
    )

    return markup
