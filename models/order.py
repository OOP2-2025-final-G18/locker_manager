from peewee import DateTimeField, ForeignKeyField, Model

from .db import db
from .product import Product
from .user import User


class Order(Model):
    id: int
    user = ForeignKeyField(User, backref="orders")
    product = ForeignKeyField(Product, backref="orders")
    order_date = DateTimeField()

    class Meta:
        database = db
