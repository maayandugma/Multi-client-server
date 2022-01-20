import requests
import json
import random

# The questions from website Trivia Game by using "json" command
url = "https://opentdb.com/api.php?amount=10&category=22&difficulty=medium&type=multiple"

response = requests.get(url)
data = response.json()
json_data = data["results"]

question_list = []
question_list_shuffle = []
correct_answer = []
ls_answer = []

#Delete the keys that i don't need for the game
for i in json_data:
    del i["category"]
    del i["type"]
    del i["difficulty"]

for q in json_data:
    question_list.append(q["question"])
for i in question_list:
    question_list_shuffle.append(i)

for c_answer in json_data:
    correct_answer.append(c_answer['correct_answer'])

for answer in json_data:
    ls = []
    ls.append(answer['correct_answer'])
    for j in answer["incorrect_answers"]:
        ls.append(j)
        random.shuffle(ls)
    ls_answer.append(ls)
protocol_answer = []
for i in ls_answer:
    sign = "#".join(i)
    protocol_answer.append(sign)





