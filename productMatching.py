from DataPreprocessing.preprocessing import *
from loadDataset import load_data_to_dict
import csv
import os


def main():
    tommyh_preprocessing()
    gerryw_preprocessing()
    zalando_preprocessing()

    data_dict_gerryw = load_data_to_dict(os.path.abspath('./Datasets/clean_TommyHilfiger.csv'))
    data_dict_tommyh = load_data_to_dict(os.path.abspath('./Datasets/clean_GerryWeber.csv'))
    data_dict_zalando = load_data_to_dict(os.path.abspath('./Datasets/clean_Zalando.csv'))



if __name__ == "__main__":
    main()