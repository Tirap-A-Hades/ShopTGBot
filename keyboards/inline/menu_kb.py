from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_api.db_commands import get_categories, get_subcategories

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
item_cd = CallbackData("item", "item_id")
to_cart_cd = CallbackData("in_cart", "item_id", "count")


##Формирует callback data
def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(level=level,
                       category=category,
                       subcategory=subcategory,
                       item_id=item_id)


#Формирует инлайн кнопки со всеми категориями
async def categories_kb():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = await get_categories()
    for category in categories:
        button_text = f"{category.category_name}"
        cb = make_callback_data(level=CURRENT_LEVEL+1,
                                category=category.category_code)

        markup.insert(InlineKeyboardButton(text=button_text, callback_data=cb))

    return markup


#Формирует инлайн кнопки со всеми подкатегориями
async def subcategories_kb(category):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = await get_subcategories(category)
    for subcategory in subcategories:
        button_text = f"{subcategory.subcategory_name}"

        markup.insert(InlineKeyboardButton(text=button_text,
                                           switch_inline_query_current_chat=f"/catalog, {category}, {subcategory.subcategory_code}"))
    # кнопка назад, возвращает на прошлый уровень
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL-1)
        )
    )
    return markup


#Инлайн кнопка для добавления товра в коризну
def item_kb(item_id):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Добавить в корзину",
                             callback_data=item_cd.new(item_id=item_id)
                             )
    )
    return markup


#Формировнаие инлайн кнопко с количеством товара для добавления в корзину
def count_kb(item_id):
    markup = InlineKeyboardMarkup()
    i = 0
    for i in range(0, 20):
        markup.insert(
            InlineKeyboardButton(text=f"{i+1}",
                                 callback_data=to_cart_cd.new(item_id=item_id, count=str(i+1)))
        )

    return markup





