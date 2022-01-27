import requests
import random

# The questions from website Trivia Game by using "json" command

parameters = {
    "amount": 10,
    "type": "multiple",
    "difficulty": "medium",
    "category": "11"
}

response = requests.get("https://opentdb.com/api.php", params=parameters)

data = response.json()
json_data = data["results"]

question_list = []
correct_answer = []
ls_answer = []

for question in json_data:
    question_test = question["question"]
    answer_test = question['correct_answer']
    question_list.append((question_test,answer_test))


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

print(protocol_answer)
