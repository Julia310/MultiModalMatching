import os
import csv
import pandas as pd

gw = os.path.abspath('../../Datasets/clean_GerryWeber.csv')
th = os.path.abspath('../../Datasets/clean_TommyHilfiger.csv')
zal = os.path.abspath('../../Datasets/clean_Zalando.csv')

gw_zal = os.path.abspath('../../Datasets/matches_zalando_gerryweber.csv')
th_zal = os.path.abspath('../../Datasets/matches_zalando_tommyhilfiger.csv')


def test_matches(matches, df1, df2):
    file = open(matches)
    csv_reader = csv.reader(file)
    next(csv_reader)

    correct_count = 0
    wrong_count = 0

    for rec in csv_reader:
        cat1 = df1.loc[df1['id'] == rec[0]]['category'].tolist()[0]
        cat2 = df2.loc[df2['id'] == rec[1]]['category'].tolist()[0]

        print('================================================')

        print(df1.loc[df1['id'] == rec[0]]['name'])
        print(df2.loc[df2['id'] == rec[1]]['name'])

        print('================================================')

        '''if not cat1 == cat2:
            print('================================================')

            print(df1.loc[df1['id'] == rec[0]])
            print(df2.loc[df2['id'] == rec[1]])

            print('================================================')
            wrong_count += 1
        else:
            correct_count += 1'''

    print('matches found: ' + str(correct_count))
    print('not found: ' + str(wrong_count))


def main():
    df2 = pd.read_csv(gw)
    df_zal = pd.read_csv(zal)
    #test_matches(gw_zal, df_zal, df2)
    df2 = pd.read_csv(th)
    test_matches(th_zal, df_zal, df2)


if __name__ == "__main__":
    main()
