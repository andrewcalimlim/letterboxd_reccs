from flask import Flask, render_template, request
from parser import *

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html')

@app.route('/output',methods = ['POST', 'GET'])
def output():
   if request.method == 'POST':
        you = request.form['you']
        usernames = request.form['usernames']
        usernames = usernames.split()
        usernames.append(you)

        raw_scores, who, films = getMatrices(usernames)
        print("approximating..")
        scores = rank1Approximate(raw_scores)

        reccs = recommendation(raw_scores, scores, who, films, you)

        return render_template('output.html', name = you, film1=reccs[0], 
        film2=reccs[1], film3=reccs[2], film4=reccs[3], film5=reccs[4])

if __name__ == '__main__':
    app.run(debug=True)