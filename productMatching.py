from DatabaseManager.peeweeModels import Matches
from TextPreprocessing.textPreprocessing import preprocess_text_data
from EmbeddingCreation.createTextEmbedding import ManageTextEmbeddings
from EmbeddingCreation.createImageEmbedding import ManageImageEmbeddings
from Util.matchingUtilities import MatchingUtilities
from time import time
from ClassifierTraining.trainClassifier import TrainClassifier
from Classification.classificationWorker import ClassificationWorker
from DatabaseManager.dbContextManager import DbContextManager
import logging
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

ZALANDO_TABLE_ALIAS = 'zal'
TOMMYH_GERRYW_TABLE_ALIAS = 'th_gw'

def create_text_embedding(m_utilities):
    # ##### Text Embedding ######
    start = time()
    logging.info('Start creating text embeddings')
    text_data_df1, text_data_df2 = m_utilities.get_matching_text_data_as_df(column_names=['name', 'variant', 'price'])
    text_to_embeddings_obj = ManageTextEmbeddings(
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        text_data_df1,
        text_data_df2,
        ZALANDO_TABLE_ALIAS,
        TOMMYH_GERRYW_TABLE_ALIAS)
    text_to_embeddings_obj.generate_embeddings()
    logging.info('Text embeddings created and saved in ' + str((time() - start) / 60.0) + ' minutes')


def create_image_embedding(m_utilities):
    # ###### Image Embedding ######
    logging.info('Start creating and saving image embeddings')
    start = time()
    image_list1, image_list2 = m_utilities.get_matching_image_path_list(ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS)
    images_to_embeddings = ManageImageEmbeddings(
        image_list1,
        image_list2,
        ZALANDO_TABLE_ALIAS,
        TOMMYH_GERRYW_TABLE_ALIAS,
    )
    images_to_embeddings.generate_embeddings()
    logging.info('Image embeddings created and saved in ' + str("{:8.2f}".format(time() - start)) + ' seconds')


def preprocess_data():
    logging.info('Start preparing data for embedding creation')
    start = time()
    logging.info('Start processing')
    datasets = preprocess_text_data()
    logging.info('Init Matching Util')
    m_utilities = MatchingUtilities([datasets[-1]], datasets[:-1])
    logging.info('Data prepared for embedding creation in ' + str("{:8.2f}".format(time() - start)) + ' seconds')
    return m_utilities


def recreate_database_tables():
    Matches.create_table()
    mysql_manager = DbContextManager()
    mysql_manager.recreate_tables()


def config_logger():
    # TODO ensure file is created for final execution
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


def train_classifier(m_utilities):
    logging.info('Training the classifier')
    train_classifier_obj = TrainClassifier()
    train_classifier_obj.train_classifier_test()




def main():
    # 0 Main utilities
    config_logger()
    # recreate_database_tables()

    # 1.1 Applying data schema
    # ##### DROP AND RECREATE TABLES #####
    m_utilities = preprocess_data()

    # ##### CREATING EMBEDDINGS #####
    # create_text_embedding(m_utilities)
    # create_image_embedding(m_utilities)
    # ##### CREATING EMBEDDINGS #####

    # ##### TRAINING THE CLASSIFIER #####
    # train_classifier(m_utilities)

    # ##### CONDUCTING CLASSIFICATION #####
    classification_worker = ClassificationWorker(m_utilities)
    classification_worker.conduct_classification()

if __name__ == "__main__":
    main()
