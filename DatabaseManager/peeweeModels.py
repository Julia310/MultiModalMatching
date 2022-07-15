from peewee import *

mysql_db = MySQLDatabase('MatchingData', user='root', password='asdfghjkl.54321', host='127.0.0.1', port=3306)


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = mysql_db


class LongTextField(TextField):
    field_type = 'LONGTEXT'


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
