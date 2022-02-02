import requests
import random
import html
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
just_question = []

for question in json_data:

    question_list.append(html.unescape(question["question"]))
    correct_answer.append(html.unescape(question['correct_answer']))

for answer in json_data:
    ls = []
    ls.append(answer['correct_answer'])

    for j in html.unescape(answer["incorrect_answers"]):
        ls.append(html.unescape(j))

        random.shuffle(ls)
    ls_answer.append(ls)
protocol_answer = []
for i in ls_answer:
    sign = "#".join(i)
    protocol_answer.append(sign)

