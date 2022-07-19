from peewee import MySQLDatabase
from abc import ABC
from playhouse.shortcuts import ReconnectMixin
from playhouse.mysql_ext import MariaDBConnectorDatabase


# mysql_db = MySQLDatabase('MatchingData', user='root', password='asdfghjkl.54321', host='127.0.0.1', port=3306)


class ReconnectMySQLDatabase(ReconnectMixin, MySQLDatabase, ABC):
    pass



mysql_db = MariaDBConnectorDatabase('dbprak_09', user='dbprak_09', password='hDVNlxpQHZGQRbv',
                                  host='wdi13.informatik.uni-leipzig.de', port=3406)


def before_execute_any_query():
    mysql_db.connect()


# after execute all queries and complete the action
def after_execute_query():
    mysql_db.close()
