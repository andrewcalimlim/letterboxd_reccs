from flask import Flask, render_template, request
#from parser import * #for local hosting test
from .parser import * #for Heroku web hosting

app = Flask(__name__)

@app.route('/')
def input():
    return render_template('input.html')

@app.route('/output',methods = ['POST', 'GET'])
def output():
    if request.method == 'POST':
        you = request.form['you']
        usernames = request.form['usernames']
        #convergence = float(request.form['converge'])

        usernames = usernames.split()
        usernames.append(you)

        raw_scores, who, films = getMatrices(usernames)
        print("approximating..")
        scores = rank1Approximate(raw_scores, 0.01)

        reccs = recommendation(raw_scores, scores, who, films, [], you)

        return render_template('output.html', name = you, film1=reccs[0], film2=reccs[1], film3=reccs[2], film4=reccs[3], film5=reccs[4])

@app.route('/about',methods = ['POST', 'GET'])
def about():
    if request.method == 'GET':
        return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)