from peewee import CharField, IntegerField, Model

from .db import db


class User(Model):
    id: int
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db
