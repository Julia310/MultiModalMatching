from DatabaseManager.peeweeModels import mysql_db, ZalandoEmbeddings, TommyHGerryWEmbeddings
from tqdm import tqdm


class MySQLManager:

    def __init__(self):
        self.connection = mysql_db
        self.table_dict = {'zal': ZalandoEmbeddings, 'th_gw': TommyHGerryWEmbeddings}
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

    def update_image_by_articleId(self, batch, data_source):
        for data_dict in tqdm(batch, desc='save image embeddings'):
            query = self.table_dict[data_source].update(image=data_dict['image']). \
                where(self.table_dict[data_source].articleId == data_dict['articleId'])
            query.execute()
