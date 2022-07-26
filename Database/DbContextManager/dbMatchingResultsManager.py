from Database.dbContext import mysql_db
from Database.Models.matchingResultsModel import Matches, TrueMatches
import logging


class DbMatchesContextManager:

    def __init__(self):
        self.connection = mysql_db
        self.matches = Matches
        self.true_matches = TrueMatches
        self.batch_size = 1000

    def save_match(self, article_ids):
        matches_dict = {
            'zal_id': article_ids[0],
            'th_gw_id': article_ids[1]
        }
        self.matches.insert([matches_dict]).execute()

    def save_many_matches(self, matches):
        self.matches.insert_many(matches).execute()

    def save_true_matches(self, matches):
        with self.connection.atomic():
            for idx in range(0, len(matches), self.batch_size):
                idx_max = len(matches)
                if idx + self.batch_size < idx_max:
                    idx_max = idx + self.batch_size
                val_to_table = matches[idx:idx_max]
                query = self.true_matches.insert_many(val_to_table)
                query.execute()
                logging.info(str(idx_max) + ' rows inserted')

    def recreate_tables(self):
        if self.matches.table_exists() and self.true_matches.table_exists():
            self.matches.drop_table()
            self.true_matches.drop_table()
        self.true_matches.create_table()
        self.matches.create_table()

