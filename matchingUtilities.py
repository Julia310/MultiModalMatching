import csv
import itertools

class MatchingUtilities:

    def __init__(self, data_path_list1, data_path_list2):
        self.data_dict1 = self.create_data_dict(data_path_list1)
        self.data_dict2 = self.create_data_dict(data_path_list2)
        self.block_dict1 = self.blocking(self.data_dict1)
        self.block_dict2 = self.blocking(self.data_dict2)
        self.potential_matches = self.create_candidates()


    def create_data_dict(self, data_path_list):
        data_dict = dict()
        data_dict_list = []
        for path in data_path_list:
            data_dict_list.append(self.load_data_to_dict(path))
        if self.distinct_dict_keys_check(data_dict_list):
            for data_dict2 in data_dict_list:
                data_dict = {**data_dict, **data_dict2}
        else:
            raise Exception('Dictionaries contain same keys. Please make sure keys are distinct to merge dictionaries.')
        return data_dict


    def load_data_to_dict(self, filename):

        file = open(filename)
        csv_reader = csv.reader(file)
        next(csv_reader)

        data_dict = {}

        for rec in csv_reader:
            data_dict[rec[0]] = rec[1:]

        return data_dict


    def distinct_dict_keys_check(self, data_dict_list):
        for i in range(len(data_dict_list)):
            for j in range(i + 1, len(data_dict_list)):
                for key in data_dict_list[i]:
                    if key in data_dict_list[j]:
                        return False
        return True


    def blocking(self, data_dict):
        blocking_dict = {}

        ids = list(data_dict.keys())

        for id in ids:
            blocking_key = data_dict[id][-1]
            if not (blocking_key in blocking_dict):
                blocking_dict[blocking_key] = []
            blocking_dict[blocking_key].append(id)

        return blocking_dict




    def create_candidates(self):
        keys = list(self.block_dict1.keys())

        potential_matches = []

        for key in keys:
            if key in self.block_dict2:
                potential_matches.append({key: list(itertools.product(self.block_dict1[key], self.block_dict2[key]))})

        return potential_matches