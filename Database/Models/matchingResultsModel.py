from Database.Models.baseModel import BaseModel
from peewee import *


class Matches(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()


class TrueMatches(BaseModel):
    zal_id = CharField()
    th_gw_id = CharField()
