from DataPreprocessing.preprocessing import *
from loadDataset import load_data_to_dict
from blocking import blocking
from createMatchCandidates import create_candidates
import csv
import os


def main():
    #tommyh_preprocessing()
    #gerryw_preprocessing()
    #zalando_preprocessing()

    data_dict_gerryw = load_data_to_dict(os.path.abspath('./Datasets/clean_GerryWeber.csv'))
    data_dict_tommyh = load_data_to_dict(os.path.abspath('./Datasets/clean_TommyHilfiger.csv'))
    data_dict_zalando = load_data_to_dict(os.path.abspath('./Datasets/clean_Zalando.csv'))


    gerryw_blocking_dict = blocking(data_dict_gerryw)
    tommyh_blocking_dict = blocking(data_dict_tommyh)
    zalando_blocking_dict = blocking(data_dict_zalando)

    #gw_th_blocking_dict = {**gerryw_blocking_dict, **tommyh_blocking_dict}

    potential_matches_gw_zalando = create_candidates(gerryw_blocking_dict, zalando_blocking_dict)
    potential_matches_th_zalando = create_candidates(tommyh_blocking_dict, zalando_blocking_dict)

    print('')



if __name__ == "__main__":
    main()