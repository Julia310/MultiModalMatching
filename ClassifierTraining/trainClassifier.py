from sklearn.ensemble import RandomForestClassifier
import logging
from Util.similarityGenerator import SimilarityGenerator
import os
import csv
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
import time
import pickle


def plot_roc_cur(fper, tper):
    plt.plot(fper, tper, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()


def get_random_forest_grid():
    # Number of trees in random forest
    n_estimators = [100, 200, 300, 600, 1000]
    # Maximum number of levels in tree
    max_depth = [30, 60, 80, 90, 100, 110, None]
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                   'max_depth': max_depth,
                   'min_samples_split': min_samples_split,
                   'min_samples_leaf': min_samples_leaf,
                   'bootstrap': bootstrap}

    return random_grid


class TrainClassifier:
    def __init__(self, db_context_manager, db_embeddings_context_manager):
        self.classifier = RandomForestClassifier(random_state=42)
        self.comparison = SimilarityGenerator(db_embeddings_context_manager)
        self.train_file = open(os.path.join(os.path.abspath('./ClassifierTraining'), 'train.csv'))
        self.csv_reader_train = csv.reader(self.train_file)
        self.test_file = open(os.path.join(os.path.abspath('./ClassifierTraining'), 'test.csv'))
        self.csv_reader_test = csv.reader(self.test_file)
        self.batchsize = 1000
        self.db_manager = db_context_manager

    '''def train_classifier(self):
        X_train = []
        y_train = []
        rows = list(self.csv_reader_train)
        for i in tqdm(range(len(rows)), desc='calculate similarities for training'):
            y_train.append(int(rows[i][-1]))
            X_train.append(self.comparison.get_similarity_vector(rows[i]))
        self.classifier.fit(X=np.array(X_train), y=np.array(y_train))'''

    def save_similarities(self, training = 1):
        #self.db_manager.recreate_similarities_tables()
        if training == 1:
            rows = list(self.csv_reader_train)
        else:
            rows = list(self.csv_reader_test)
        similarity_dict = {}
        for i in tqdm(range(len(rows)), desc='save similarities to db'):
            similarity_dict = {}
            sim_row = self.comparison.get_similarity_vector(rows[i])
            similarity_dict['zal_id'] = rows[i][0]
            similarity_dict['th_gw_id'] = rows[i][1]
            similarity_dict['name'] = sim_row[0]
            similarity_dict['variant'] = sim_row[1]
            similarity_dict['price'] = sim_row[2]
            similarity_dict['image'] = sim_row[3]
            similarity_dict['y_true'] = int(rows[i][-1])
            if (i + 1) % 5000:
                self.db_manager.save_similarities(similarity_dict, training)
        self.db_manager.save_similarities(similarity_dict, training)

    def get_similarities(self, training = 1):
        X, y = self.db_manager.select_similarities(training)
        return X, y

    def test_classifier(self):
        X_test = []
        y_test = []
        rows = list(self.csv_reader_test)
        for i in tqdm(range(len(rows)), desc='calculate similarities for testing'):
            y_test.append(int(rows[i][-1]))
            X_test.append(self.comparison.get_similarity_vector(rows[i]))
        y_pred = self.classifier.predict(np.array(X_test))
        logging.info(confusion_matrix(np.array(y_test), np.array(y_pred)))
        #fper, tper, thresholds = roc_curve(np.array(y_test), y_pred)
        #plot_roc_cur(fper, tper)

    def train_classifier(self):
        X_train, y_train = self.get_similarities(training=1)
        #X_test, y_test = self.get_similarities(training=0)
        param_dict = get_random_forest_grid()
        np.random.seed(42)
        start = time.time()
        cv_rf = GridSearchCV(self.classifier, cv=5,
                             param_grid=param_dict,
                             n_jobs=3, scoring='f1_macro')

        cv_rf.fit(X_train, y_train)
        logging.info('Best Parameters using grid search: \n',
              cv_rf.best_params_)
        end = time.time()

        logging.info('Time taken in grid search: {0: .2f}'.format(end - start))

    def train_classifier_test(self):
        X_train, y_train = self.get_similarities(training=1)
        self.classifier.fit(X=np.array(X_train), y=np.array(y_train))
        logging.info('Dumping random forest to file')
        filename = os.path.abspath(r'./random_forest.sav')
        with open(filename, 'wb') as file:
            pickle.dump(self.classifier, file)
