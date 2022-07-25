import csv
import os
import logging
import sys

MATCHES_ZAL_GW = os.path.join(os.path.abspath('./Datasets'), 'matches_zalando_gerryweber.csv')
MATCHES_ZAL_TH = os.path.join(os.path.abspath('./Datasets'), 'matches_zalando_tommyhilfiger.csv')
if 'linux' in sys.platform:
    MATCHES_ZAL_GW = os.path.join(os.path.abspath('./MultiModalMatching/Datasets'), 'matches_zalando_gerryweber.csv')
    MATCHES_ZAL_TH = os.path.join(os.path.abspath('./MultiModalMatching/Datasets'), 'matches_zalando_tommyhilfiger.csv')


class EvaluationUtilites:
    def __init__(self, db_context):
        self.zal_gw_reader = csv.reader(open(MATCHES_ZAL_GW))
        self.zal_th_reader = csv.reader(open(MATCHES_ZAL_TH))
        self.db_context = db_context

    def save_matches_to_db(self):
        attributes = ['zal_id', 'th_gw_id']
        zal_th_matches = list(self.zal_th_reader)[1:]
        zal_th_matches_dict = [dict(zip(attributes, l)) for l in zal_th_matches]
        self.db_context.save_true_matches(zal_th_matches_dict)
        logging.info('true Zalando - TommyHilfiger matches persisted to db')

        zal_gw_matches = list(self.zal_gw_reader)[1:]
        zal_gw_matches_dict = [dict(zip(attributes, l)) for l in zal_gw_matches]
        self.db_context.save_true_matches(zal_gw_matches_dict)
        logging.info('true Zalando - GerryWeber matches persisted to db')



