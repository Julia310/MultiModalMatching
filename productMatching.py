from DataPreprocessing.preprocessing import *
from loadDataset import load_data_to_dict
from blocking import blocking
import csv
import os


def main():
    tommyh_preprocessing()
    gerryw_preprocessing()
    zalando_preprocessing()

    data_dict_gerryw = load_data_to_dict(os.path.abspath('./Datasets/clean_TommyHilfiger.csv'))
    data_dict_tommyh = load_data_to_dict(os.path.abspath('./Datasets/clean_GerryWeber.csv'))
    data_dict_zalando = load_data_to_dict(os.path.abspath('./Datasets/clean_Zalando.csv'))

    zalando_blocking_dict = blocking(data_dict_zalando)



if __name__ == "__main__":
    main()