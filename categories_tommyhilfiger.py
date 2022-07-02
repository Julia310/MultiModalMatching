import pandas as pd
import os

df = pd.read_csv(os.path.abspath('./TommyHilfiger.csv'))
df = df[['MPN', 'name', 'variant', 'price']]
df.rename(columns = {'MPN':'id'}, inplace = True)

#print(df['name'].unique())
df_pullover = df['name'][df['name'].str.contains('pullover')]
#print(df_pullover)
df_shirt = df['name'][df['name'].str.contains('shirt')]
#print(df_shirt)

for value in df['name'].iteritems():
    if 'jeans' in value[1] or 'Jeans' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Jeans'
    elif 'Pullover' in value[1] or 'pullover' in value[1] or 'Hoodie' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Pullover'
    elif 'Jacke' in value[1] or 'jacke' in value[1] or 'Blazer' in value[1] or 'Parka' in value[1] or 'Sakko' in value[1] or 'sakko' in value[1] or 'coat' in value[1] or 'Mantel' in value[1] or 'mantel' in value[1] or 'Cardigan' in value[1] or 'Weste' in value[1] or 'weste' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Jacken'
    elif 'Kleid' in value[1] or 'kleid' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Kleider'
    elif 'Rock' in value[1] or 'rock' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Röcke'
    elif 'Shirt' in value[1] or 'shirt' in value[1] or 'Top' in value[1] or 'top' in value[1] or 'Hemd' in value[1] or 'hemd' in value[1] or 'Bluse' in value[1] or 'bluse' in value[1] or 'Longsleeve' in value[1] or 'Oberteil' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Oberteile'
    elif 'Slip' in value[1] or 'slip' in value[1] or 'String' in value[1] or 'Tanga' in value[1] or 'BH' in value[1] or 'Socken' in value[1] or 'socken' in value[1] or 'Füßlinge' in value[1] or 'Bralette' in value[1] or '':
        row = value[0]
        df.loc[row, 'category'] = 'Unterwäsche'
    elif 'Hose' in value[1] or 'hose' in value[1] or 'Pants' in value[1] or 'pants' in value[1] or 'Shorts' in value[1] or 'shorts' in value[1] or 'Chino' in value[1] or 'Leggings' in value[1] or 'Jeggings' in value[1] or 'Bermuda' in value[1] or 'Culotte' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Hosen'
    elif 'Schuh' in value[1] or 'schuh' in value[1] or 'Sneaker' in value[1] or 'sneaker' in value[1] or 'Sandale' in value[1] or 'sandale' in value[1] or 'Sandals' in value[1] or 'Stiefel' in value[1] or 'stiefel' in value[1] or 'Zehentrenner' in value[1] or 'Pantolette' in value[1] or 'Pump' in value[1] or 'Ballerina' in value[1] or 'Espadrille' in value[1] or 'Mokassin' in value[1] or 'Loafer' in value[1]:
        row = value[0]
        df.loc[row, 'category'] = 'Schuhe'

df.fillna('Sonstiges', inplace=True)

tommyhilfiger_categories = df["category"]

pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)

filtered_df = df[df['category'].isnull()]
#print(filtered_df)
#print(df)
print(df.groupby(['category']).count())