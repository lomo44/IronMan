import json


def main():
    data_out = []
    with open("sample_question.txt",'r') as file_in:
        next(file_in)
        for line in file_in:
            line = line.strip()
            sample = line.split(',')
            new_sample = {"text": sample[0], "entities": [{"entity": "intent", "value": sample[1]}]}
            index = 2
            while index < len(sample):
                start = new_sample["text"].find(sample[index+2])
                end = start + len(sample[index+2])
                new_entity = {"entity": sample[index], "start": start, "end": end, "value": sample[index+1]}
                new_sample["entities"].append(new_entity)
                index += 3
            data_out.append(new_sample)
            print(new_sample["text"])
    with open("training_sample.json",'w') as file_out:
        json.dump(data_out,file_out,indent=2)


if __name__ == "__main__":
    main()
