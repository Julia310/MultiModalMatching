from tqdm import tqdm
from Util.similarityGenerator import SimilarityGenerator as SimGen
from DatabaseManager.dbContextManager import DbContextManager
from Classification.classifier import Classifier
import logging


class ClassificationWorker:

    def __init__(self, matching_utils):
        self.matching_utils = matching_utils
        self.potential_matches_flat = self.matching_utils.get_potential_matches_as_flat_list()
        self.classified_matches = list()
        self.classifier = Classifier()
        self.context = DbContextManager()
        self.similarity_generator = SimGen()

    def get_zalando_id_from_matches(self, index):
        return self.potential_matches_flat[index][0]

    def get_th_gw_id_from_matches(self, index):
        return self.potential_matches_flat[index][1]

    def conduct_classification(self):
        logging.info('Starting classification')
        save_counter = 0
        for i in tqdm(range(len(self.potential_matches_flat)), 'Classification Progress    '):
            matches_tuple = [self.get_zalando_id_from_matches(i),
                             self.get_th_gw_id_from_matches(i)]
            sim_vector = self.similarity_generator.get_similarity_vector(matches_tuple)
            prediction_vector = self.classifier.predict_single(sim_vector)[0]

            if prediction_vector == 1:
                self.context.save_match(matches_tuple)
                save_counter += 1

        logging.info(f'Saved {save_counter} out of {len(self.potential_matches_flat)} matches')


