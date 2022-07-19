from Database.Models.baseModel import BaseModel
from peewee import *


class SimilaritiesTrain(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()
    name = FloatField()
    variant = FloatField()
    price = FloatField()
    image = FloatField()
    y_true = IntegerField()


class SimilaritiesTest(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()
    name = FloatField()
    variant = FloatField()
    price = FloatField()
    image = FloatField()
    y_true = IntegerField()
