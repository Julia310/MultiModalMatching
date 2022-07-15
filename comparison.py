from math import *
from DatabaseManager.databaseConnection import MySQLManager


def square_rooted(x):
    return round(sqrt(sum([a * a for a in x])), 5)


def cosine_similarity(x, y):
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 3)


def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


class Comparison:
    def __init__(self):
        self.db_manager = MySQLManager()

    def get_similarity_vector(self, articleIds):
        sim_vec = []
        zalando_embeddings = self.db_manager.select_by_article_id(articleIds[0], 'zal')
        th_gw_embeddings = self.db_manager.select_by_article_id(articleIds[1], 'th_gw')

        # name similarity
        zal_name = zalando_embeddings['name']
        th_gw_name = th_gw_embeddings['name']
        sim_vec.append(cosine_similarity(zal_name, th_gw_name))

        # variant similarity
        zal_variant = zalando_embeddings['variant']
        th_gw_variant = th_gw_embeddings['variant']
        sim_vec.append(cosine_similarity(zal_variant, th_gw_variant))

        # price similarity
        zal_price = zalando_embeddings['price']
        th_gw_price = th_gw_embeddings['price']
        price_similarity = min(float(zal_price), float(th_gw_price)) / max(float(zal_price), float(th_gw_price))
        sim_vec.append(price_similarity)

        # image similarity
        zal_image = zalando_embeddings['image']
        th_gw_image = th_gw_embeddings['image']
        sim_vec.append(cosine_similarity(zal_image, th_gw_image))
        return sim_vec
