import pandas as pd
from Preprocessing.textCleaning import clean_columns
import os


def adjustBrand(inputString):
    if 'gerry weber' in inputString:
        return 'gerry weber'
    if 'tommy' in inputString:
        return 'tommy hilfiger'
    return inputString


def zalando_preprocessing():
    if not os.path.exists(os.path.abspath('./Datasets/clean_Zalando.csv')):
        df = pd.read_csv(os.path.abspath('./Datasets/Zalando.csv'), error_bad_lines=False)
        df = df[["ArticleId", "ProductName", "Color", "Price", "Brand"]]
        df.rename(columns = {'ArticleId':'id', 'ProductName':'name', 'Color':'variant', 'Price':'price', 'Brand': 'brand'}, inplace = True)

        df["name"] = df["name"].apply(lambda x: x.split(';')[0].split(' - ')[-2])

        df = clean_columns(df, ['name', 'variant'])

        df["brand"] = df["brand"].apply(lambda x: x.lower())
        df["brand"] = df["brand"].apply(lambda x: adjustBrand(x))

        with pd.option_context('display.max_columns', None,):
            print(df)

        df.to_csv(os.path.abspath('./Datasets/clean_Zalando.csv'), index=False)


def tommyh_preprocessing():
    if not os.path.exists(os.path.abspath('./Datasets/clean_TommyHilfiger.csv')):
        df = pd.read_csv(os.path.abspath('./Datasets/TommyHilfiger.csv'))
        df = df[['MPN', 'name', 'variant', 'price']]
        df.rename(columns = {'MPN':'id'}, inplace = True)


        df = clean_columns(df, ['name', 'variant'])

        df = df.assign(brand="tommy hilfiger")

        with pd.option_context('display.max_columns', None,):
            print(df)

        df.to_csv(os.path.abspath('./Datasets/clean_TommyHilfiger.csv'), index=False)


def gerryw_preprocessing():
    if not os.path.exists(os.path.abspath('./Datasets/clean_GerryWeber.csv')):
        df = pd.read_csv(os.path.abspath('./Datasets/GerryWeber.csv'))
        df = df[['MPN', 'name', 'variant', 'price']]
        df.rename(columns = {'MPN':'id'}, inplace = True)

        df = clean_columns(df, ['name', 'variant'])

        df = df.assign(brand="gerry weber")

        with pd.option_context('display.max_columns', None,):
            print(df)

        df.to_csv(os.path.abspath('./Datasets/clean_GerryWeber.csv'), index=False)


def preprocess_text_data():
    tommyh_preprocessing()
    gerryw_preprocessing()
    zalando_preprocessing()

    clean_datasets = [
        os.path.abspath('./Datasets/clean_GerryWeber.csv'),
        os.path.abspath('./Datasets/clean_TommyHilfiger.csv'),
        os.path.abspath('./Datasets/clean_Zalando.csv')
    ]

    return clean_datasets


