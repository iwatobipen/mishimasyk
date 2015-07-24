#!/usr/local/bin/python

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def toppage():
    return render_template('toppage.html')

@app.route('/plot/')
def scatterplot():
    return render_template('toppage_v2.html')

if __name__ == '__main__':
    app.run(debug = True)


