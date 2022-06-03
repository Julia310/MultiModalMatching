import pandas as pd
import numpy as np
import re

def hasnumbers(inputString):
    if any(char.isdigit() for char in inputString):
        print(inputString)
        return True
    return False

def hasspaces(inputString):
    if '  ' in inputString or inputString.startswith(' '):
        print(inputString)
        return True
    return False

def removespaces(inputString):
    if inputString.startswith(' '):
        inputString = inputString.lstrip(' ')
        print(inputString)
    return inputString

#df["name"].apply(lambda x: hasnumbers(x))

df = pd.read_csv('/Users/svenjaschmiedl/Documents/Studium/Leipzig_Master/2. Semester/BD_Pr/Daten/TommyHilfiger.csv')
df = df[['name', 'variant', 'price', 'MPN']]

df["name"] = df["name"].apply(lambda x: x.lower())
df["name"] = df["name"].apply(lambda x: x.replace('ä', 'ae'))
df["name"] = df["name"].apply(lambda x: x.replace('ö', 'oe'))
df["name"] = df["name"].apply(lambda x: x.replace('ü', 'ue'))
df["name"] = df["name"].apply(lambda x: x.replace('ß', 'ss'))
df["name"] = df["name"].apply(lambda x: x.replace('-', ' '))
df["name"] = df["name"].apply(lambda x: x.replace('1er', 'einer'))
df["name"] = df["name"].apply(lambda x: x.replace('2er', 'zweier'))
df["name"] = df["name"].apply(lambda x: x.replace('3er', 'dreier'))
df["name"] = df["name"].apply(lambda x: x.replace('4er', 'vierer'))
df["name"] = df["name"].apply(lambda x: x.replace('5er', 'fünfer'))
df["name"] = df["name"].apply(lambda x: x.replace('6er', 'sechser'))
df["name"] = df["name"].apply(lambda x: x.replace('7/8', 'siebenachtel'))
df["name"] = df["name"].apply(lambda x: re.sub('[0-9]+','', x))
df["name"] = df["name"].apply(lambda x: x.replace('  ', ' '))

df = df.assign(Marke="tommy hilfiger")

df["name"].apply(lambda x: removespaces(x))
df["name"].apply(lambda x: hasspaces(x))

#with pd.option_context('display.max_columns', None,):
    #print(df)

#print(df.describe()) #basic stats
#print(df.isnull().any()) #check null values
#print(df.dtypes)
