#!/usr/bin/python
import json
import re

def writeJosn(filename,data):
    file_full_name = './'+'filename'+'.json'
    with open(file_full_name,'w') as file_out:
        json.dump(data, file_out)


with open('input_p.txt','r') as file_in:
    q_polar =[]
    q_closed = []
    q_open = []
    question_type = 'Polar'
    question = ['question','answer']
    for line in file_in:
        match_question = re.match('Question\s*(\S*).*:\s*(.*)\s',line)
        if match_question:
            question_type = match_question.group(1)
            question[0] = match_question.group(2)
            if question_type == 'Open-ended' :
                list_element = {'Question': question[0],'Answer': None}
                q_open.append(list_element)
        match_answer = re.match('Answer:\s*(.*)\s', line)
        if match_answer:
            question[1] = match_answer.group(1)
            if question_type == 'Polar':
                list_element = {'Question': question[0], 'Answer': question[1]}
                q_polar.append(list_element)
            if question_type == 'Closed':
                list_element = {'Question': question[0], 'Answer': question[1]}
                q_polar.append(list_element)
    data = {'polar':q_polar,'closed':q_closed,'open_ended':q_open}

    writeJosn('tests_questions', data)