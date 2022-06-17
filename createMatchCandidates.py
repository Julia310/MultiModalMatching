import itertools

def create_candidates(data_dict1, data_dict2):
    keys = list(data_dict1.keys())

    potential_matches = []

    for key in keys:
        potential_matches.append({key: list(itertools.product(data_dict2[key], data_dict1[key]))})

    return potential_matches

