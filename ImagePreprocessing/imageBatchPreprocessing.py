import logging

class ImageBatchIterator:
    def __init__(self, image_path_list):
        self.image_path_list = image_path_list
        self.batch_size = 2000
        self.idx = 0

    def next_batch(self):
        if self.idx == len(self.image_path_list):
            return None

        idx_max = len(self.image_path_list)
        if self.idx + self.batch_size < idx_max:
            idx_max = self.idx + self.batch_size

        image_path_sublist = self.image_path_list[self.idx:idx_max]

        logging.info('>>>>>>>>>>  Preprocessing images    ' + str(self.idx) + ' - ' + str(idx_max) + '  <<<<<<<<<<')
        self.idx = idx_max
        return image_path_sublist

