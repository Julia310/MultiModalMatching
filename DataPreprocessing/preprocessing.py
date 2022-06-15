import pandas as pd
from DataPreprocessing.dataCleaning import clean_columns
import os




def zalando_preprocessing():
    df = pd.read_csv(os.path.abspath('./Datasets/clean_Zalando.csv'))



def tommyh_preprocessing():
    df = pd.read_csv(os.path.abspath('./Datasets/clean_TommyHilfiger.csv'))




def gerryw_preprocessing():
    df = pd.read_csv(os.path.abspath('./Datasets/clean_GerryWeber.csv'))




