import logging
import pickle


class Classifier:

    def __init__(self):
        self.classifier = self.load_classifier()

    def load_classifier(self):
        with open(r'./random_forest.sav', 'rb') as file:
            pickle_model = pickle.load(file)
        return pickle_model

    def get_classifier(self):
        return self.classifier

    def predict_single(self, sim_vector):
        return self.classifier.predict([sim_vector])

    def predict_batch(self, sim_vector_batch):
        return self.classifier.predict(sim_vector_batch)

    ###TODO: evaluate if further information would be useful
    def get_prediction_probability(self, sim_vector):
        return self.classifier.predict_proba(sim_vector)
