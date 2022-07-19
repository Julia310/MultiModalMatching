from peewee import Model
from Database.dbContext import mysql_db


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = mysql_db
