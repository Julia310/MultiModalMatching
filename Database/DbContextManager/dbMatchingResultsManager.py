from Database.dbContext import mysql_db
from Database.Models.matchingResultsModel import Matches
import logging


class DbMatchesContextManager:

    def __init__(self):
        self.connection = mysql_db
        self.matches = Matches
        self.batch_size = 1000

    def save_match(self, article_ids):
        matches_dict = {
            'zal_id': article_ids[0],
            'th_gw_id': article_ids[1]
        }
        self.matches.insert([matches_dict]).execute()

    def recreate_tables(self):
        if self.matches.table_exists():
            self.matches.drop_table()
        self.matches.create_table()

