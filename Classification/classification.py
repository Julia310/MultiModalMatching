

class Classification:
    def __init__(self, db_context):
        self.db_context = db_context

    def threshold_prediction(self, sim_dict):
        if sim_dict['price'] > 0.6 and sim_dict['image'] > 0.35 \
                and sim_dict['variant'] > 0.2 and sim_dict['name'] > 0.1:
            return 1
        else:
            return 0

    def conduct_classification(self, sim_dict):
        save_counter = 0
        if self.threshold_prediction(sim_dict) == 1:
            self.db_context.save_match((sim_dict['zal_id'], sim_dict['th_gw_id']))
            save_counter += 1

            #if sim_dict['price'] > 0.6 and sim_dict['image'] > 0.35 \
                    #and sim_dict['variant'] > 0.2 and sim_dict['name'] > 0.1: