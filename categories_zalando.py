import pandas as pd
import os

df = pd.read_csv(os.path.abspath('./Zalando.csv'), error_bad_lines=False)
df = df[["ArticleId", "ProductName", "Color", "Price", "Brand"]]
df.rename(columns = {'ArticleId':'id', 'ProductName':'name', 'Color':'variant', 'Price':'price', 'Brand': 'brand'}, inplace = True)
df["name"] = df["name"].apply(lambda x: x.split(';')[0].split(' - ')[-2])
#print(df.name.unique())
df_pullover = df['name'][df['name'].str.contains('pullover')]
#print(df_pullover.unique())
df_shirt = df['name'][df['name'].str.contains('shirt')]
#print(df_shirt.unique())
df_hose = df['name'][df['name'].str.contains('hose')]
#print(df_hose.unique())
df_roecke = df['name'][df['name'].str.contains('rock')]
#print(df_roecke.unique())
df_jacke = df['name'][df['name'].str.contains('jacke')]
#print(df_jacke.unique())
df_kleid = df['name'][df['name'].str.contains('kleid')]
#print(df_kleid.unique())
df_schuhe = df['name'][df['name'].str.contains('schuhe')]
#print(df_schuhe.unique())


for value in df['name'].iteritems():
    if 'jeans' in value[1] or 'Jeans' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Jeans'
    elif 'pullover' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Pullover'
    elif 'Jacke' in value[1] or 'jacke' in value[1] or 'Sakko' in value[1] or 'sakko' in value[1] or 'Blazer' in value[1] or 'Mantel' in value[1] or 'mantel' in value[1] or 'Weste' in value[1] or 'weste' in value[1] or 'Windbreaker' in value[1] or 'Parka' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Jacken'
    elif 'Kleid' in value[1] or 'kleid' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Kleider'
    elif 'Rock' in value[1] or 'rock' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Röcke'
    elif 'Shirt' in value[1] or 'shirt' in value[1] or 'Top' in value[1] or 'Hemd' in value[1] or 'hemd' in value[1] or 'Bluse' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Oberteile'
    elif 'Hose' in value[1] or 'hose' in value[1] or 'Shorts' in value[1] or 'shorts' in value[1] or 'Chino' in value[1] or 'Tights' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Hosen'
    elif 'Schuh' in value[1] or 'schuh' in value[1] or 'Sneaker' in value[1] or 'Sandale' in value[1] or 'sandale' in value[1] or 'Sandalette' in value[1] or 'sandalette' in value[1] or 'Zehentrenner' in value[1] or 'Ballerina' in value[1] or 'ballerina' in value[1] or 'Overknees' in value[1] or 'pumps' in value[1] or 'Pumps' in value[1] or 'stiefel' in value [1] or 'Stiefel' in value[1] or 'High Heel' in value[1] or 'Pantolette' in value[1] or 'Mokassin' in value[1] or 'Boot' in value[1] or 'Espadrille' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Schuhe'
    elif 'Slip' in value[1] or 'slip' in value[1] or 'String' in value[1] or 'Tanga' in value[1] or 'Panties' in value[1] or 'BH' in value[1] or 'Bustier' in value[1] or 'Socken' in value[1] or 'socken' in value[1] or 'Strümpfe' in value[1] or 'Füßlinge' in value[1] or 'Bralette' in value[1] or '':
        row = value[0]
        df.loc[row, 'category'] = 'Unterwäsche'

df.fillna('Sonstiges', inplace=True)

zalando_categories = df["category"]

pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

#filtered_df = df[df['category'].isnull()]
#print(filtered_df)
#print(df)
df_gerryweber = df.loc[df['brand'] == 'Gerry Weber']
#print(df_gerryweber)
print(df_gerryweber.groupby(['category']).count())

df_tommyhilfiger = df.loc[df['brand'] == 'Tommy Hilfiger']
#print(df_tommyhilfiger)
print(df_tommyhilfiger.groupby(['category']).count())