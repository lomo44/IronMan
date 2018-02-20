import json


def main():
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
                new_sample = {"text": sample[0], "entities": [{"entity": "intent", "value": sample[1]}]}
                # new_sample["entities"].append({"entity": "question_type", "value": sample[2]})
                index = 2
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


if __name__ == "__main__":
    main()
