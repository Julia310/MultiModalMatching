import pandas as pd
from TextPreprocessing.textCleaning import clean_columns
import os


def adjust_brand(input_string):
    if 'gerry weber' in input_string:
        return 'gerry weber'
    if 'tommy' in input_string:
        return 'tommy hilfiger'
    return input_string


def get_first_image(urls, dataset):
    if dataset == 'th':
        url = urls.split(',')[0]
    elif dataset == 'z':
        url = 'https' + urls.split('https')[1]
    else:
        url = urls.split(',')[0]
    return url


def zalando_preprocessing():
    if not os.path.exists(os.path.abspath('./Datasets/clean_Zalando.csv')):
        df = pd.read_csv(os.path.abspath('./Datasets/Zalando.csv'), error_bad_lines=False)
        df = df[["ArticleId", "ProductName", "Color", "Price", 'ImageUrl', "Brand"]]
        df.rename(columns={'ArticleId': 'id', 'ProductName': 'name', 'Color': 'variant', 'Price': 'price',
                           'ImageUrl': 'image', 'Brand': 'brand'}, inplace=True)

        df["name"] = df["name"].apply(lambda x: x.split(';')[0].split(' - ')[-2])

        df = clean_columns(df, ['name'])

        df["brand"] = df["brand"].apply(lambda x: x.lower())
        df["brand"] = df["brand"].apply(lambda x: adjust_brand(x))

        df["variant"] = df["variant"].apply(lambda x: x.lower())
        df["image"] = df["image"].apply(lambda x: get_first_image(x, 'z'))

        with pd.option_context('display.max_columns', None, ):
            print(df)

        df.to_csv(os.path.abspath('./Datasets/clean_Zalando.csv'), index=False)


def tommyh_preprocessing():
    if not os.path.exists(os.path.abspath('./Datasets/clean_TommyHilfiger.csv')):
        df = pd.read_csv(os.path.abspath('./Datasets/TommyHilfiger.csv'))
        df = df[['MPN', 'name', 'variant', 'price', 'images']]
        df.rename(columns={'MPN': 'id', 'images': 'image'}, inplace=True)

        df = clean_columns(df, ['name'])
        df = df.assign(brand="tommy hilfiger")

        df["variant"] = df["variant"].apply(lambda x: x.lower())
        df["image"] = df["image"].apply(lambda x: get_first_image(x, 'th'))

        with pd.option_context('display.max_columns', None, ):
            print(df)

        df.to_csv(os.path.abspath('./Datasets/clean_TommyHilfiger.csv'), index=False)


def gerryw_preprocessing():
    if not os.path.exists(os.path.abspath('./Datasets/clean_GerryWeber.csv')):
        df = pd.read_csv(os.path.abspath('./Datasets/GerryWeber.csv'))
        df = df[['MPN', 'name', 'variant', 'price', 'images']]
        df.rename(columns={'MPN': 'id', 'images': 'image'}, inplace=True)

        df = clean_columns(df, ['name'])
        df = df.assign(brand="gerry weber")

        df["variant"] = df["variant"].apply(lambda x: x.lower())
        df["image"] = df["image"].apply(lambda x: get_first_image(x, 'gw'))

        with pd.option_context('display.max_columns', None, ):
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
