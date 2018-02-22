from Trainer import Trainer
import json
import urllib.parse


def main():
    access_token = 'MRWCQY74ZTT244XU4DUPHCMU4RIRUDKT'
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


if __name__ == "__main__":
    main()