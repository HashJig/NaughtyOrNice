from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('questions.html')

@app.route('/submit', methods=['POST'])
def submit():
    naughty = []
    good = []

    good_responses = 0
    bad_responses = 0

    def addGoodBad(response, goodResponse):
        nonlocal good_responses, bad_responses
        if response == goodResponse:
            good_responses += 1
        else:
            bad_responses += 1

    name = request.form.get('name')
    believe_in_santa = request.form.get('believe_in_santa')
    lost_temper = request.form.get('lost_temper')
    say_please_thank_you = request.form.get('say_please_thank_you')
    whine = request.form.get('whine')
    nicest_thing = request.form.get('nicest_thing')

    addGoodBad(believe_in_santa, "yes")
    addGoodBad(lost_temper, "no")
    addGoodBad(say_please_thank_you, "yes")
    addGoodBad(whine, "no")

    response_user = ""
    if good_responses == 4:
        response_user = "You are on the good list"
        good.append(name)
    elif good_responses == 3:
        response_user = "You are on the brink of being on the naughty list"
        good.append(name)    
    elif good_responses == 2:
        response_user = "You are now on the naughty list"
        naughty.append(name)
    else:
        response_user = "You have been really naughty"
        naughty.append(name)


    return render_template('results.html', 
                           response_user=response_user)

if __name__ == '__main__':
    app.run(debug=True)
