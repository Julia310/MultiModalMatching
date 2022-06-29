from keras.applications.resnet import ResNet50
from keras.layers import Flatten
from keras.models import Model
from ImagePreprocessing.imageBatchPreprocessing import ImageBatchIterator
from multiprocessing.pool import ThreadPool
from ImagePreprocessing.imagePreprocessing import get_and_preprocess_image
from DatabaseManager.databaseConnection import MySQLManager


class ImageEmbeddingGenerator:
    def __init__(self):
        self.image_size = [224, 224, 3]
        self.model = self.instantiate_model()

    def instantiate_model(self):
        resnet = ResNet50(input_shape=self.image_size, weights='imagenet', include_top=False)
        output = Flatten()(resnet.output)
        model = Model(inputs=resnet.input, outputs=output)
        return model

    def get_image_embedding(self, img_dict):
        image = img_dict['image']
        vector = self.model.predict(image)[0].dumps()
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

    def process_image_batches(self, image_batch_iterator, data_source):
        batch = image_batch_iterator.next_batch()
        while not batch is None:

            img_batch = self.pool.map(get_and_preprocess_image, batch)

            embeddings = []

            for img_data in img_batch:
                embeddings.append(self.image_embedding_generator.get_image_embedding(img_data))

            self.db_manager.update_image_by_articleId(embeddings, data_source)
            batch = image_batch_iterator.next_batch()

    def generate_and_save_embeddings(self):
        self.process_image_batches(self.image_batch_iterator1, self.data_source1)
        self.process_image_batches(self.image_batch_iterator2, self.data_source2)
