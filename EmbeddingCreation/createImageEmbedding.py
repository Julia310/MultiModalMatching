import keras.models
from keras.applications.resnet import ResNet50
from keras.layers import Flatten
from keras.models import Model
from ImagePreprocessing.imageBatchPreprocessing import ImageBatchIterator
from multiprocessing.pool import ThreadPool
from ImagePreprocessing.imagePreprocessing import get_and_preprocess_image
from DatabaseManager.databaseConnection import MySQLManager
import os
from tqdm import tqdm


class ImageEmbeddingGenerator:
    def __init__(self):
        self.image_size = [224, 224, 3]
        self.model = self.instantiate_model()

    def instantiate_model(self):
        if not os.path.exists(os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet.h5')):
            resnet = ResNet50(input_shape=self.image_size, weights='imagenet', include_top=False)
            output = Flatten()(resnet.output)
            model = Model(inputs=resnet.input, outputs=output)
            model.save(os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet.h5'), save_format='h5')
        else:
            model = keras.models.load_model(os.path.join(os.path.abspath(r'EmbeddingCreation'), 'Model', 'resnet.h5'))
        return model

    def get_image_embedding(self, img_dict):
        image = img_dict['image']
        vector = self.model.predict(image, verbose=0)[0].dumps()
        return {'articleId': img_dict['articleId'], 'image': vector}


class ManageImageEmbeddings:
    def __init__(self, image_list1, image_list2, data_source1, data_source2):
        self.image_batch_iterator1 = ImageBatchIterator(image_list1)
        self.image_batch_iterator2 = ImageBatchIterator(image_list2)
        self.data_source1 = data_source1
        self.data_source2 = data_source2
        self.processes = 10
        self.pool = ThreadPool(self.processes)
        self.image_embedding_generator = ImageEmbeddingGenerator()
        self.db_manager = MySQLManager()

    def process_image_batches(self, image_batch_iterator, data_source, multi=True):
        batch = image_batch_iterator.next_batch()
        while batch is not None:
            embeddings = []

            if multi:
                img_batch = self.pool.map(get_and_preprocess_image, batch)
            else:
                img_batch = self.batch_for_system(batch)

            for img_data in tqdm(img_batch, desc='create embeddings from batch'):
                embeddings.append(self.image_embedding_generator.get_image_embedding(img_data))

            self.db_manager.update_image_by_articleId(embeddings, data_source)
            batch = image_batch_iterator.next_batch()

    def batch_for_system(self, batch):
        image_list = []
        for image in batch:
            if get_and_preprocess_image(image):
                image_list.append(get_and_preprocess_image(image))
        return image_list

    def generate_embeddings(self):
        self.process_image_batches(self.image_batch_iterator1, self.data_source1)
        self.process_image_batches(self.image_batch_iterator2, self.data_source2)
