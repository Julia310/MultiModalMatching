from Classification.thresholdPrediction import threshold_prediction
from tqdm import tqdm


class SequentialClassification:
    """
        Conducts a classification for every pair of potential matches sequentially
    """
    def __init__(self, db_context, sim_generator, m_utilities):
        self.db_context = db_context
        self.sim_generator = sim_generator
        self.potential_matches = m_utilities.get_potential_matches_as_flat_list()

    def conduct_classification(self):
        """
            First the similarity vector is calculated for every match by applying the procedure
            sim_generetor.get_similarity_vector. Subsequently, the match is inserted in the database if classified as
            match by threshold_prediction()
        """
        for i in tqdm(range(len(self.potential_matches)), desc='save similarities of potential classified_matches'):
            sim_dict = self.sim_generator.get_similarity_vector(self.potential_matches[i])
            if threshold_prediction(sim_dict) == 1:
                self.db_context.save_classified_match((sim_dict['zal_id'], sim_dict['th_gw_id']))
