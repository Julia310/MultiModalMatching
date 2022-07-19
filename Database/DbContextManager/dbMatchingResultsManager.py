from Database.dbContext import mysql_db
from Database.Models.matchingResultModel import Matches


class DbMatchesContextManager:

    def __init__(self):
        self.connection = mysql_db
        self.matches = Matches

    def save_match(self, article_ids):
        matches_dict = {
            'zal_id': article_ids[0],
            'th_gw_id': article_ids[1]
        }
        self.matches.insert([matches_dict]).execute()

    def recreate_table(self):
        if self.matches.table_exists():
            self.matches.drop_table()
        self.matches.create_table()
