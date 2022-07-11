from TextPreprocessing.textPreprocessing import preprocess_text_data
from EmbeddingCreation.createTextEmbedding import ManageTextEmbeddings
from EmbeddingCreation.createImageEmbedding import ManageImageEmbeddings
from matchingUtilities import MatchingUtilities
from time import time
from ClassifierTraining.trainingPreparation import TrainingPreparation
from ClassifierTraining.trainClassifier import TrainClassifier


def main():


    start = time()
    print('Start processing')
    datasets = preprocess_text_data()

    print('Init Matching Utilities')
    m_utilities = MatchingUtilities([datasets[-1]], datasets[:-1])
    print('data prepared for embedding creation in ' + str((time() - start) / 60.0) + ' minutes')

    print('Start preparing data for embedding creation')
    # ###### Text Embedding ######
    start = time()
    print('start creating text embeddings')
    '''text_data_df1, text_data_df2 = m_utilities.get_matching_text_data_as_df(column_names=['name', 'variant', 'price'])


    text_to_embeddings_obj = ManageTextEmbeddings(
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
        text_data_df1,
        text_data_df2,
        'zal',
        'th_gw')
    text_to_embeddings_obj.generate_embeddings()
    print('text embeddings created and saved in ' + str((time() - start) / 60.0) + ' minutes')'''

    # ###### Image Embedding ######
    print('start creating and saving image embeddings')
    start = time()
    image_list1, image_list2 = m_utilities.get_matching_image_path_list('zal', 'th_gw')
    images_to_embeddings = ManageImageEmbeddings(image_list1, image_list2, 'zal', 'th_gw')
    images_to_embeddings.generate_embeddings()
    print('image embeddings created and saved in ' + str((time() - start) / 60.0) + ' minutes')

    '''potential_matches = m_utilities.get_potential_matches()
    cls_training = TrainingPreparation(potential_matches)
    print('train classifier')
    train_classifier_obj = TrainClassifier()
    train_classifier_obj.train_classifier()'''


if __name__ == "__main__":
    main()
