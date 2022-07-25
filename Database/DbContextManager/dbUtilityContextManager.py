from Database.dbContext import mysql_db
from Database.Models.utilityModels import TrueMatches, Similarities
import logging


class DbUtilityContextManager:

    def __init__(self):
        self.connection = mysql_db
        self.true_matches = TrueMatches
        self.similarities = Similarities
        self.batch_size = 1000

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

    def save_similarity_vector(self, similarity_dict):
        self.similarities.insert([similarity_dict]).execute()

    def recreate_tables(self):
        if self.similarities.table_exists() and self.true_matches.table_exists():
            self.similarities.drop_table()
            self.true_matches.drop_table()
        self.true_matches.create_table()
        self.similarities.create_table()
