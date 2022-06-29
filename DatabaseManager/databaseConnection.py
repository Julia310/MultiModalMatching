from DatabaseManager.peeweeModels import mysql_db, ZalandoEmbeddings, TommyHGerryWEmbeddings


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
        products = []
        for data_dict in batch:
            product = self.table_dict[data_source].select().\
                where(self.table_dict[data_source].articleId == data_dict['articleId'])

            product[0].image = data_dict['image']
            products.append(product[0])
        self.table_dict[data_source].bulk_update([products], fields=self.table_dict[data_source].image)
