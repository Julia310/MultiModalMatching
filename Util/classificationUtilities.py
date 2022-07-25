from tqdm import tqdm


class ClassificationUtilities:
    def __init__(self, db_context, sim_generator, m_utilities, classification):
        self.db_context = db_context
        self.sim_generator = sim_generator
        self.potential_matches = m_utilities.get_potential_matches_as_flat_list()
        self.classification = classification

    def save_similarities(self):
        for i in tqdm(range(len(self.potential_matches)), desc='save similarities of potential matches'):
            sim_vector = self.sim_generator.get_similarity_vector(self.potential_matches[i])

            sim_dict = {
                'zal_id': self.potential_matches[i][0],
                'th_gw_id': self.potential_matches[i][1],
                'name': sim_vector[0],
                'variant': sim_vector[1],
                'price': sim_vector[2],
                'image': sim_vector[3]
            }

            self.db_context.save_similarity_vector(sim_dict)
            self.classification.conduct_classification(sim_dict)

