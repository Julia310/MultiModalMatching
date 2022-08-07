
def threshold_prediction(sim_dict):
    """
        sim_dict: dictionary containing similarity values for name, variant, price image belonging to a pair of products
        returns 1 (match) if all values are greater than the minimum thresholds, 0 (no match) otherwise
    """
    if sim_dict['price'] > 0.75 and sim_dict['image'] > 0.5 \
            and sim_dict['variant'] > 0.35 and sim_dict['name'] > 0.15:
        return 1
    else:
        return 0