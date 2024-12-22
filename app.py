from flask import Flask, render_template, request

import requests
import json

app = Flask(__name__)

naughty = []
good = []

@app.route('/')
def home():
    return render_template('questions.html')

@app.route('/submit', methods=['POST'])
def submit():
    good_responses = 0
    bad_responses = 0

    def aiCheckNicestThing(nicest_thing):
        url = "https://api.arliai.com/v1/chat/completions"
        payload = json.dumps({
        "model": "Mistral-Nemo-12B-Instruct-2407",
        "messages": [
            {"role": "system", "content": "You are to look at the nicest thing someone has done this year and rank it out of 10, if you rank it higher than 6 then respond with yes, otherwise respond with no. Respond in lowercase."},
            {"role": "user", "content": "{nicest_thing}"},
        ],
        "repetition_penalty": 1.1,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": False
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer a816df82-3350-4f23-900c-92321129e702"
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return json.loads(response.text)['choices'][0]['message']['content']

    name = request.form.get('name')
    if request.form.get('believe_in_santa') == "yes":
        good_responses += 1
    if request.form.get('lost_temper') == "no":
        good_responses += 1
    if request.form.get('say_please_thank_you') == "yes": 
        good_responses += 1
    if request.form.get('whine') == "no":
        good_responses += 1
    if aiCheckNicestThing(request.form.get('nicest_thing')) == "yes":
        good_responses += 1

    response_user = ""
    if good_responses == 5:
        response_user = "has been really nice"
        good.append(name)
    elif good_responses == 4:
        response_user = "has been nice"
        good.append(name)
    elif good_responses == 3:
        response_user = "has been too bad to be on the nice list"
        naughty.append(name)    
    elif good_responses == 2:
        response_user = "has been a bit naughty"
        naughty.append(name)
    else:
        response_user = "has been really naughty"
        naughty.append(name)


    return render_template('results.html', 
                           response_user=response_user,
                           name=name,
                           naughty=naughty,
                           good=good
                           )

if __name__ == '__main__':
    app.run(debug=True)
