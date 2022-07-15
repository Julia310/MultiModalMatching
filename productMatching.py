from TextPreprocessing.textPreprocessing import preprocess_text_data
from EmbeddingCreation.createTextEmbedding import ManageTextEmbeddings
from EmbeddingCreation.createImageEmbedding import ManageImageEmbeddings
from matchingUtilities import MatchingUtilities
from DatabaseManager.databaseConnection import MySQLManager
from time import time
from ClassifierTraining.trainingPreparation import TrainingPreparation
from ClassifierTraining.trainClassifier import TrainClassifier


def create_text_embedding(m_utilities):
    # ##### Text Embedding ######
    start = time()
    print('start creating text embeddings')
    text_data_df1, text_data_df2 = m_utilities.get_matching_text_data_as_df(column_names=['name', 'variant', 'price'])
    text_to_embeddings_obj = ManageTextEmbeddings(
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        text_data_df1,
        text_data_df2,
        'zal',
        'th_gw')
    text_to_embeddings_obj.generate_embeddings()
    print('text embeddings created and saved in ' + str((time() - start) / 60.0) + ' minutes')


def create_image_embedding(m_utilities):
    # ###### Image Embedding ######
    print('start creating and saving image embeddings')
    start = time()
    image_list1, image_list2 = m_utilities.get_matching_image_path_list('zal', 'th_gw')
    images_to_embeddings = ManageImageEmbeddings(image_list1, image_list2, 'zal', 'th_gw')
    images_to_embeddings.generate_embeddings()
    print('image embeddings created and saved in ' + str((time() - start) / 60.0) + ' minutes')


def preprocess_data():
    print('Start preparing data for embedding creation')
    start = time()
    print('Start processing')
    datasets = preprocess_text_data()
    print('Init Matching Utilities')
    m_utilities = MatchingUtilities([datasets[-1]], datasets[:-1])
    print('data prepared for embedding creation in ' + str((time() - start) / 60.0) + ' minutes')
    return m_utilities


def train_classifier(m_utilities):
    potential_matches = m_utilities.get_potential_matches()
    #cls_training = TrainingPreparation(potential_matches)
    print('train classifier')
    train_classifier_obj = TrainClassifier()
    #train_classifier_obj.save_similarities(training=1)
    #train_classifier_obj.save_similarities(training=0)
    train_classifier_obj.train_classifier()
    #train_classifier_obj.train_classifier()
    #train_classifier_obj.test_classifier()


def recreate_database_tables():
    mysql_manager = MySQLManager()
    mysql_manager.recreate_tables()


def main():
    # 1.1 Applying data schema
    # ##### DROP AND RECREATE TABLES ######
    #recreate_database_tables()

    # 1.1 Applying data schema
    # ##### DROP AND RECREATE TABLES ######
    m_utilities = preprocess_data()

    # ##### CREATING EMBEDDINGS ######
    #create_text_embedding(m_utilities)
    #create_image_embedding(m_utilities)
    # ##### CREATING EMBEDDINGS ######

    # ######################>
    # ######################
    # ######################
    # ######################
    train_classifier(m_utilities)

if __name__ == "__main__":
    main()
