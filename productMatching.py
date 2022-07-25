import os
import sys
conf_path = os.getcwd()
print(conf_path)
sys.path.append(conf_path)
from TextPreprocessing.textPreprocessing import preprocess_text_data
from EmbeddingCreation.createTextEmbedding import ManageTextEmbeddings
from EmbeddingCreation.createImageEmbedding import ManageImageEmbeddings
from Util.matchingUtilities import MatchingUtilities
from time import time
from ClassifierTraining.trainClassifier import TrainClassifier
from Classification.classificationWorker import ClassificationWorker
from Database.DbContextManager.dbEmbeddingContextManager import DbEmbeddingContextManager
from Database.DbContextManager.dbTrainDataContextManager import DbTrainDataContextManager
from Database.DbContextManager.dbMatchingResultsManager import DbMatchesContextManager
from Database.DbContextManager.dbUtilityContextManager import DbUtilityContextManager
from Util.similarityGenerator import SimilarityGenerator
from dataAlias import ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS
from Util.evaluationUtilities import EvaluationUtilites
from Util.classificationUtilities import ClassificationUtilities
from Classification.classification import Classification
import logging


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def create_text_embedding(m_utilities, db_embedding_manager):
    # ##### Text Embedding ######
    start = time()
    logging.info('Start creating text embeddings')
    text_data_df1, text_data_df2 = m_utilities.get_matching_text_data_as_df(column_names=['name', 'variant', 'price'])
    text_to_embeddings_obj = ManageTextEmbeddings(
        #'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        'sentence-transformers/distiluse-base-multilingual-cased-v1',
        text_data_df1,
        text_data_df2,
        ZALANDO_TABLE_ALIAS,
        TOMMYH_GERRYW_TABLE_ALIAS,
        db_embedding_manager)
    text_to_embeddings_obj.manage_embeddings()
    logging.info('Text embeddings created and saved in ' + str((time() - start) / 60.0) + ' minutes')


def create_image_embedding(m_utilities, db_embedding_manager):
    # ###### Image Embedding ######
    logging.info('Start creating and saving image embeddings')
    start = time()
    image_list1, image_list2 = m_utilities.get_matching_image_path_list(ZALANDO_TABLE_ALIAS, TOMMYH_GERRYW_TABLE_ALIAS)
    images_to_embeddings = ManageImageEmbeddings(
        image_list1,
        image_list2,
        ZALANDO_TABLE_ALIAS,
        TOMMYH_GERRYW_TABLE_ALIAS,
        db_embedding_manager
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


def recreate_database_tables(db_embedding_manager, db_matches_manager, db_utility_manager):
    db_embedding_manager.recreate_tables()
    db_matches_manager.recreate_tables()
    db_utility_manager.recreate_tables()


def config_logger():
    # TODO ensure file is created for final execution
    logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)


def train_classifier(m_utilities, db_train_data_manager, db_embedding_manager):
    logging.info('Training the classifier')
    train_classifier_obj = TrainClassifier(db_train_data_manager, db_embedding_manager)
    train_classifier_obj.train_classifier_test()


def main():
    # 0 Main utilities
    config_logger()
    m_utilities = preprocess_data()

    db_embedding_manager = DbEmbeddingContextManager()
    db_matches_manager = DbMatchesContextManager()
    db_utility_manager = DbUtilityContextManager()

    # 1.1 Applying data schema
    # ##### DROP AND RECREATE TABLES #####
    recreate_database_tables(db_embedding_manager, db_matches_manager, db_utility_manager)


    # ##### CREATING EMBEDDINGS #####
    create_text_embedding(m_utilities, db_embedding_manager)
    create_image_embedding(m_utilities, db_embedding_manager)
    # ##### CREATING EMBEDDINGS #####

    sim_generator = SimilarityGenerator(db_embedding_manager)
    classification = Classification(db_matches_manager)
    classification_utilities = ClassificationUtilities(db_utility_manager, sim_generator, m_utilities, classification)
    classification_utilities.save_similarities()
    #evaluation_utilities = EvaluationUtilites(db_utility_manager)
    #evaluation_utilities.save_matches_to_db()

    # ##### TRAINING THE CLASSIFIER #####
    #db_train_data_manager = DbTrainDataContextManager()
    #train_classifier(m_utilities, db_train_data_manager, db_embedding_manager)

    # ##### CONDUCTING CLASSIFICATION #####
    # recreate_database_tables(db_matches_manager)
    #classification_worker = ClassificationWorker(m_utilities, db_matches_manager, db_embedding_manager)
    #classification_worker.conduct_classification()


if __name__ == "__main__":
    main()
