import pandas as pd
import numpy as np

def hasnumbers(inputString):
    if any(char.isdigit() for char in inputString):
        print(inputString)
        return True
    return False

def cutGerry(inputString):
    if 'gerry weber' in inputString:
        return 'gerry weber'
    return inputString

def cutTommy(inputString):
    if 'tommy' in inputString:
        return 'tommy hilfiger'
    return inputString

#df["ProductName"].apply(lambda x: hasnumbers(x))


df = pd.read_csv('/Users/svenjaschmiedl/Documents/Studium/Leipzig_Master/2. Semester/BD_Pr/Daten/zalando.csv', error_bad_lines=False)
df = df[["ProductName", "ArticleId", "Color", "Brand", "Price"]]

df["ProductName"] = df["ProductName"].apply(lambda x: x.split(';')[0].split(' - ')[-2])
df["ProductName"] = df["ProductName"].apply(lambda x: x.lower())
df["ProductName"] = df["ProductName"].apply(lambda x: x.replace('ä', 'ae'))
df["ProductName"] = df["ProductName"].apply(lambda x: x.replace('ö', 'oe'))
df["ProductName"] = df["ProductName"].apply(lambda x: x.replace('ü', 'ue'))
df["ProductName"] = df["ProductName"].apply(lambda x: x.replace('ß', 'ss'))
df["ProductName"] = df["ProductName"].apply(lambda x: x.replace('-', ' '))
df["ProductName"] = df["ProductName"].apply(lambda x: x.replace('3/4', 'dreiviertel'))

df["Color"] = df["Color"].apply(lambda x: x.lower())
df["Color"] = df["Color"].apply(lambda x: ' '.join(set(x.split('/'))))

df["Brand"] = df["Brand"].apply(lambda x: x.lower())

df["Brand"].apply(lambda x: cutGerry(x))
df["Brand"].apply(lambda x: cutTommy(x))

with pd.option_context('display.max_columns', None,):
    print(df)

#print(df.describe()) #basic stats
#print(df.isnull().any()) #check null values
#print(df.dtypes)
