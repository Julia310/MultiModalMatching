

def blocking(data_dict):
    blocking_dict = {}
    #blocking_key = data_dict[key]

    ids = list(data_dict.keys())

    for id in ids:
        blocking_key = data_dict[id][-1]
        if not (blocking_key in blocking_dict):
            blocking_dict[blocking_key] = []
        blocking_dict[blocking_key].append(id)

    return blocking_dict





