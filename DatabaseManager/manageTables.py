from DatabaseManager.peeweeModels import mysql_db, ZalandoEmbeddings, TommyHGerryWEmbeddings


def create_tables():
    mysql_db.create_tables([ZalandoEmbeddings, TommyHGerryWEmbeddings])


def drop_tables():
    mysql_db.drop_tables([ZalandoEmbeddings, TommyHGerryWEmbeddings])


drop_tables()
create_tables()
