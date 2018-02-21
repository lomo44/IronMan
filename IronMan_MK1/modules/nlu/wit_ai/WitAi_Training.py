from Trainer import Trainer
import json
import sys
import urllib.parse
import time


def generate_sample_json():
    # inten_list=["personal_info", "person", "location", "information", "experience", "preference", "opinion", "ability"]
    # question_type_list=["polar", "closed"]
    data_out = []
    with open("sample_question.txt",'r') as file_in:
        for line in file_in:
            if (line[0] != '#'):
                line = line.strip()
                sample = line.split(',')
                # if sample[1] not in inten_list:
                #     print ("Error:",sample[1],"is not a legal intent")
                #     exit()
                # if sample[2] not in question_type_list:
                #     print ("Error:", sample[2], "is not a legal question type")
                #     exit()
                new_sample = {"text": sample[0], "entities": []};
                # new_sample["entities"].append({"entity": "intent", "value": sample[1]})
                new_sample["entities"].append({"entity": "conversation_type", "value": sample[2]})
                index = 3
                while index < len(sample):
                    start = new_sample["text"].find(sample[index+2])
                    end = start + len(sample[index+2])
                    if start == -1 or end == -1:
                        print ("Error:", sample[index+2], "cannot be find in text")
                        exit()
                    new_entity = {"entity": sample[index], "start": start, "end": end, "value": sample[index+1]}
                    new_sample["entities"].append(new_entity)
                    index += 3
                data_out.append(new_sample)
                print(new_sample["text"])
    with open("training_sample.json",'w') as file_out:
        json.dump(data_out,file_out,indent=2)


def sending_message(access_token):
    client = Trainer(access_token=access_token)
    input_message_file = "sample_question.txt"
    data_out = []
    with open(input_message_file, 'r') as message_in:
        next(message_in)
        for line in message_in:
            line = line.strip()
            question = line.split(',')
            new_message = question[0]
            url = urllib.parse.quote(new_message, safe='/', encoding=None, errors=None)
            data_out.append(client.get_message(url))

    with open("message_response.json", 'w') as file_out:
        json.dump(data_out, file_out, indent=2)



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
    access_token = 'MRWCQY74ZTT244XU4DUPHCMU4RIRUDKT'
    keyword_entity_file = "keyword_entities.json"
    training_sample_file = "training_sample.json"
    client = Trainer(access_token=access_token)
    if len(sys.argv) == 1:
        client.init_entity(keyword_entity_file)
        client.init_training_sample(training_sample_file)
    elif sys.argv[1]=="-d" or sys.argv[1]=="-D" or sys.argv[1]=="delete":
        client.clean_up()
    elif sys.argv[1] == "-g" or sys.argv[1] == "-G" or sys.argv[1] == "generate_sample_json":
        generate_sample_json()
    elif sys.argv[1] == "-r" or sys.argv[1] == "-R" or sys.argv[1] == "message_response":
        sending_message(access_token)
    elif sys.argv[1]=="-h" or sys.argv[1]=="-H" or sys.argv[1]=="help":
        print ("Default setting: Initialize and training the Wit.ai")
        print ("-d/-D/delete: delete all data in the wit.ai")
        print ("-g/-G/generate_sample_json: generate training sample file in JSON")
        print ("-r/-R/message_response: send question to Wit.ai to get response")
    else:
        print ("Error Input: used -h for help")


if __name__ == "__main__":
    main()