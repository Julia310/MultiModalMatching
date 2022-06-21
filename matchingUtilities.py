import csv

def load_data_to_dict(filename):

    file = open(filename)
    csv_reader = csv.reader(file)

    next(csv_reader)

    data_dict = {}

    for rec in csv_reader:
        data_dict[rec[0]] = rec[1:]


    return data_dict