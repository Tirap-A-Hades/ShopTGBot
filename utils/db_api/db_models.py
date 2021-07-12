
from sqlalchemy import sql, Column, Sequence, BIGINT, Integer, ForeignKey, String

from utils.db_api.db_gino import db

#Таблица товаров
class Item(db.Model):
    __tablename__ = "items"
    query: sql.Select

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)

    #код категории(на англ)
    category_code = Column(String(40))
    category_name = Column(String(50))

    #код подкатегории(на англ)
    subcategory_code = Column(String(40))
    subcategory_name = Column(String(50))

    name = Column(String(50))
    price = Column(Integer)

    def __repr__(self):
        return f"""
        Товар №{self.id} - {self.name}
        Цена {self.price}
        """


class Cart(db.Model):
    __tablename__ = "cart"
    query: sql.Select

    #user id нужен для привязки товара к определнному пользователю
    user_id = Column(BIGINT, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    count = Column(Integer)

    def __repr__(self):
        return f"""
        id товара: {self.item_id}
        id пользователя: {self.user_id}
        """
