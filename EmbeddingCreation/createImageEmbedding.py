import keras.models
from keras.applications.resnet import ResNet50
from ImagePreprocessing.imageBatchPreprocessing import ImageBatchIterator
from multiprocessing.pool import ThreadPool
from ImagePreprocessing.imagePreprocessing import get_and_preprocess_image
from DatabaseManager.dbContextManager import DbContextManager
import os
import numpy as np
from tqdm import tqdm
import pickle


class ImageEmbeddingGenerator:

    def __init__(self):
        self.image_size = [224, 224, 3]
        self.model = self.instantiate_model()
        self.image_split_count = 5

    def instantiate_model(self):
        if not os.path.exists(os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet50.h5')):
            model = ResNet50(input_shape=self.image_size, weights='imagenet', include_top=False)
            model.save(os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet50.h5'), save_format='h5')
        else:
            model = keras.models.load_model(os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet50.h5'), compile=False)
        return model

    def get_image_embedding(self, img_dict):
        image = img_dict['image']
        embedding = self.model.predict(image, verbose=0)[0]
        embedding = np.mean(embedding, axis=0)
        vector = np.mean(embedding, axis=0)
        img_byte_dict = {'articleId': img_dict['articleId'], 'image': pickle.dumps(vector)}
        return img_byte_dict

    def split_image_for_persisting(self, vector):
        split_dict = np.array_split(vector, self.image_split_count)
        return split_dict


class ManageImageEmbeddings:
    def __init__(self, image_list1, image_list2, data_source1, data_source2):
        self.image_batch_iterator1 = ImageBatchIterator(image_list1)
        self.image_batch_iterator2 = ImageBatchIterator(image_list2)
        self.data_source1 = data_source1
        self.data_source2 = data_source2
        self.processes = 10
        self.pool = ThreadPool(self.processes)
        self.image_embedding_generator = ImageEmbeddingGenerator()
        self.db_manager = DbContextManager()

    def process_image_batches(self, image_batch_iterator, data_source, multi=False):
        batch = image_batch_iterator.next_batch()
        while batch is not None:
            embeddings = []

            if multi:
                img_batch = self.pool.map(get_and_preprocess_image, batch)
            else:
                img_batch = self.preprocess_image_batch(batch)

            for img_data in tqdm(img_batch, desc='Create embeddings from batch'):
                embeddings.append(self.image_embedding_generator.get_image_embedding(img_data))

            self.db_manager.update_image_by_article_id(embeddings, data_source)
            batch = image_batch_iterator.next_batch()

    def preprocess_image_batch(self, batch):
        image_list = []
        for i in tqdm(range(len(batch)), f'Preprocess image batch      '):
            image = batch[i]
            if get_and_preprocess_image(image):
                image_list.append(get_and_preprocess_image(image))
        return image_list

    def generate_embeddings(self):
        #FIXME
        #self.process_image_batches(self.image_batch_iterator1, self.data_source1)
        self.process_image_batches(self.image_batch_iterator2, self.data_source2)
