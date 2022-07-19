from Database.dbContext import mysql_db
from Database.Models.trainDataModels import SimilaritiesTrain, SimilaritiesTest


class DbTrainDataContextManager:

    def __init__(self):
        self.connection = mysql_db
        self.similarity_table_train = SimilaritiesTrain
        self.similarity_table_test = SimilaritiesTest
        self.batch_size = 8000

    def recreate_similarities_tables(self):
        self.connection.drop_tables([SimilaritiesTest, SimilaritiesTrain])
        self.connection.create_tables([SimilaritiesTest, SimilaritiesTrain])

    def save_similarities(self, values, training=1):
        with self.connection.atomic():
            if training == 1:
                query = self.similarity_table_train.insert_many(values)
            else:
                query = self.similarity_table_test.insert_many(values)
            query.execute()

    def select_similarities(self, training=1):
        if training == 1:
            similarities = self.similarity_table_train.select()
        else:
            similarities = self.similarity_table_test.select()

        X = []
        y = []

        for sim in similarities:
            X.append([sim.name, sim.variant, sim.price, sim.image])
            y.append(sim.y_true)
        return X, y



