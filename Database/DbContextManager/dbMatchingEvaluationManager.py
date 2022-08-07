from Database.dbContext import mysql_db
from Database.Models.matchingEvaluationModels import Matches, TrueMatches, TommyHilfigerIds, GerryWeberIds
import logging
from peewee import JOIN


class DbMatchesContextManager:
    """
        Persists classified and true classified_matches to database and enables methods to access these.
        Emables to receive data for the evaluation of threshold_classification of the whole matching process.
    """

    def __init__(self):
        self.connection = mysql_db
        self.classified_matches = Matches
        self.true_matches = TrueMatches
        self.batch_size = 1000

    def save_match(self, article_ids):
        matches_dict = {
            'zal_id': article_ids[0],
            'th_gw_id': article_ids[1]
        }
        self.classified_matches.insert([matches_dict]).execute()

    def save_many_matches(self, matches):
        self.classified_matches.insert_many(matches).execute()

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
        if self.classified_matches.table_exists():
            self.classified_matches.drop_table()
        if self.true_matches.table_exists():
            self.true_matches.drop_table()
        self.true_matches.create_table()
        self.classified_matches.create_table()

    def get_classification_evaluation_data(self, total_potential_matches):
        # number of true matches from database
        query = self.true_matches.select()
        total_true_matches = len(query)
        # number of classified matches
        query = self.classified_matches.select()
        classified_matches = len(query)
        # Join true matches and classified matches to get the number of true positives
        join_cond = (
                (Matches.zal_id == TrueMatches.zal_id) &
                (Matches.th_gw_id == TrueMatches.th_gw_id))
        query = (self.true_matches.select().join(self.classified_matches, JOIN.INNER, on=join_cond))
        true_positives = len(query)
        false_negatives = total_true_matches - true_positives
        false_positives = classified_matches - true_positives
        true_negatives = total_potential_matches - true_positives - false_negatives - false_positives

        return true_positives, false_positives, false_negatives, true_negatives

