from sklearn.ensemble import RandomForestClassifier
from comparison import cosine_similarity
from DatabaseManager.databaseConnection import MySQLManager
import os
import csv


class TrainClassifier:
    def __init__(self):
        self.forest = RandomForestClassifier(criterion='gini',
                                             n_estimators=5,
                                             random_state=1,
                                             n_jobs=2)
        self.db_manager = MySQLManager()
        self.file = open(os.path.join(os.path.abspath('./ClassifierTraining'), 'train.csv'))
        self.csv_reader = csv.reader(self.file)
        self.batchsize = 1000

    def get_batch_for_training(self):
        idx = 0
        batch = []
        for rec in self.csv_reader:
            print(rec)
            batch.append(rec)
            idx += 1
            if idx == 1000:
                break
        return batch

    def train_classifier(self):
        X_train = []
        batch = self.get_batch_for_training()
        while len(batch) > 0:
            for i in range(len(batch)):
                sim_vector = self.get_similaritiy_vector(batch[i])
            batch = self.get_batch_for_training()

    def get_similaritiy_vector(self, articleIds):
        sim_vec = []
        zalando_embeddings = self.db_manager.select_by_articleId(articleIds[0], 'zal')
        th_gw_embeddings = self.db_manager.select_by_articleId(articleIds[1], 'th_gw')
        for i in range(len(zalando_embeddings)):
            print(i)
        return sim_vec