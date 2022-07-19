from Database.Models.baseModel import BaseModel
from peewee import *


class ZalandoEmbeddings(BaseModel):
    articleId = CharField(unique=True)
    name = BlobField()
    variant = BlobField()
    price = CharField()
    image = BlobField()


class TommyHGerryWEmbeddings(BaseModel):
    articleId = CharField(unique=True)
    name = BlobField()
    variant = BlobField()
    price = CharField()
    image = BlobField()
