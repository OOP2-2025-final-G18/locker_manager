from peewee import CharField, DecimalField, Model

from .db import db


class Product(Model):
    id: int
    name = CharField()
    price = DecimalField()

    class Meta:
        database = db
