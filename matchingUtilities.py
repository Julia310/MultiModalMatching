import csv
import itertools
import pandas as pd


def create_data_dict(data_path_list):
    data_dict = dict()
    data_dict_list = []
    for path in data_path_list:
        data_dict_list.append(load_data_to_dict(path))
    if distinct_dict_keys_check(data_dict_list):
        for data_dict2 in data_dict_list:
            data_dict = {**data_dict, **data_dict2}
    else:
        raise Exception('Dictionaries contain same keys. Please make sure keys are distinct to merge dictionaries.')
    return data_dict


def load_data_to_dict(filename):
    file = open(filename)
    csv_reader = csv.reader(file)
    next(csv_reader)

    data_dict = {}

    for rec in csv_reader:
        data_dict[rec[0]] = rec[1:]

    return data_dict


def distinct_dict_keys_check(data_dict_list):
    for i in range(len(data_dict_list)):
        for j in range(i + 1, len(data_dict_list)):
            for key in data_dict_list[i]:
                if key in data_dict_list[j]:
                    return False
    return True


def blocking(data_dict):
    blocking_dict = {}
    ids = list(data_dict.keys())

    for id in ids:
        blocking_key = data_dict[id][-1] + ' ' + data_dict[id][-2]
        if not (blocking_key in blocking_dict):
            blocking_dict[blocking_key] = []
        blocking_dict[blocking_key].append(id)

    return blocking_dict


def rename_df(df, column_names):
    if len(df.columns) > len(column_names):
        df.drop(df.columns[len(df.columns) - (len(df.columns) - len(column_names)):], axis=1, inplace=True)

    column_names_dict = {}
    for i in range(len(df.columns)):
        column_names_dict[i] = column_names[i]

    df.rename(columns=column_names_dict, inplace=True)
    return df


class MatchingUtilities:

    def __init__(self, data_path_list1, data_path_list2):
        self.data_dict1 = create_data_dict(data_path_list1)
        self.data_dict2 = create_data_dict(data_path_list2)
        self.block_dict1 = blocking(self.data_dict1)
        self.block_dict2 = blocking(self.data_dict2)
        self.potential_matches = self.create_candidates()
        self.remove_irrelevant_data_from_dict()

    def create_candidates(self):
        keys = list(self.block_dict2.keys())

        potential_matches = {}

        cnt = 0
        for key in keys:
            if key in self.block_dict1:
                potential_matches[key] = list(itertools.product(self.block_dict1[key], self.block_dict2[key]))
                cnt += len(potential_matches[key])

        print('number of potential matches: ' + str(cnt))

        return potential_matches

    def remove_irrelevant_data_from_dict(self):
        potential_matches_keys = list(self.potential_matches.keys())

        for data_dict in [self.data_dict1, self.data_dict2]:
            for key in list(data_dict.keys()):
                if not data_dict[key][-1] in potential_matches_keys:
                    del data_dict[key]

    def get_potential_matches(self):
        return self.potential_matches

    def get_matching_text_data_as_df(self, column_names):
        df1 = pd.DataFrame.from_dict(self.data_dict1, orient='index')
        df1 = rename_df(df1, column_names)

        df2 = pd.DataFrame.from_dict(self.data_dict2, orient='index')
        df2 = rename_df(df2, column_names)

        return df1, df2

    def get_matching_image_path_list(self):
        image_list1 = list({'articleId': key, 'path': self.data_dict1[key][-2]}
                           for key in list(self.data_dict1.keys()))

        image_list2 = list({'articleId': key, 'path': self.data_dict2[key][-2]}
                           for key in list(self.data_dict2.keys()))
        return image_list1, image_list2
