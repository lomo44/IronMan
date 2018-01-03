from Trainer import Trainer
import json
import time


def update_json(database_file,entities_file):
    # update entities_file with data in file in
    # DEPRECATED
    entities_data = []
    with open(database_file, 'r') as file_in:
        data_in = json.load(file_in)
        for entity_id in data_in:
            entity = {"id": None, "values": None}
            entity['id'] = entity_id
            entity_value = []
            for value_data in data_in[entity_id]:
                new_val = {"value": value_data, "expressions":[value_data]}
                entity_value.append(new_val)
            entity['values'] = entity_value
            entities_data.append(entity)
    with open(entities_file, 'w') as file_out:
        json.dump(entities_data, file_out, indent=4)


def init_entity(access_token, input_json_file):
    # import entities from Json file
    client = Trainer(access_token=access_token)
    client.clean_up()
    with open(input_json_file,'r') as json_in:
        init_data = json.load(json_in)
        exist_entities = client.get_all_entities()
        for new_entity in init_data:
            if new_entity['id'] not in exist_entities:
                print ("add {0}".new_entity['id'])
                client.add_entity(new_entity)
            else:
                client.update_entity(new_entity['id'], new_entity)



def main():
    access_token = '2TYQHOQY3LRZRIJFHJSMGHH26S6JLEBF'
    keyword_entity_file = "keyword_entities.json"
    training_sample_file = "training_sample.json"
    client = Trainer(access_token=access_token)
    # client.clean_up()
    client.init_entity(keyword_entity_file)
    client.init_training_sample(training_sample_file)


if __name__ == "__main__":
    main()