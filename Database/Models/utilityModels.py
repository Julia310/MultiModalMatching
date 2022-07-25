from Database.Models.baseModel import BaseModel
from peewee import *


class TrueMatches(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()


class Similarities(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()
    name = FloatField()
    variant = FloatField()
    price = FloatField()
    image = FloatField()