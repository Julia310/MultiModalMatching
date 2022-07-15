from DatabaseManager.peeweeModels import mysql_db, ZalandoEmbeddings, TommyHGerryWEmbeddings, \
    SimilaritiesTrain, SimilaritiesTest
from tqdm import tqdm
import pickle


class MySQLManager:

    def __init__(self):
        self.connection = mysql_db
        self.table_dict = {'zal': ZalandoEmbeddings, 'th_gw': TommyHGerryWEmbeddings}
        self.similarity_table = {1: SimilaritiesTrain, 0: SimilaritiesTest}
        self.batch_size = 8000

    def save_many(self, values, data_source):
        with self.connection.atomic():
            for idx in range(0, len(values), self.batch_size):
                idx_max = len(values)
                if idx + self.batch_size < idx_max:
                    idx_max = idx + self.batch_size
                val_to_table = values[idx:idx_max]
                query = self.table_dict[data_source].insert_many(val_to_table)
                query.execute()
                print(str(idx_max) + ' rows inserted')

    def update_image_by_article_id(self, batch, data_source):
        for data_dict in tqdm(batch, desc='save image embeddings       '):
            query = self.table_dict[data_source].update(
                image=data_dict['image'],
            ). \
                where(self.table_dict[data_source].articleId == data_dict['articleId'])
            query.execute()

    def select_by_article_id(self, articleId, data_source):
        product = self.table_dict[data_source].select(). \
            where(articleId == self.table_dict[data_source].articleId).get()
        embeddings = {
            'name': pickle.loads(product.name),
            'variant': pickle.loads(product.variant),
            'price': product.price,
            'image': pickle.loads(product.image)
        }
        return embeddings

    def recreate_tables(self):
        self.connection.drop_tables([ZalandoEmbeddings, TommyHGerryWEmbeddings])
        self.connection.create_tables([ZalandoEmbeddings, TommyHGerryWEmbeddings])

    def recreate_similarities_tables(self):
        self.connection.drop_tables([SimilaritiesTest, SimilaritiesTrain])
        self.connection.create_tables([SimilaritiesTest, SimilaritiesTrain])

    def save_similarities(self, values, training = 1):
        with self.connection.atomic():
            query = self.similarity_table[training].insert_many(values)
            query.execute()

    def select_similarities(self, training):
        similarities = self.similarity_table[training].select()#.where(training == self.similarity_table.training_data)

        X = []
        y = []

        for sim in similarities:
            X.append([sim.name, sim.variant, sim.price, sim.image])
            y.append(sim.y_true)
        return X, y
