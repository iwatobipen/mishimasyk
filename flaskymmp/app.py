from flask import Flask, render_template, request, url_for, jsonify
from flask_bootstrap import Bootstrap
from moduleset import chemistry
import pandas as pd
import numpy as np
import json
import pymongo
from pymongo import MongoClient
import urllib

db = MongoClient().test
collection = db.molcollection
app = Flask( __name__ )
Bootstrap(app)
dataset = collection.find()
dataset = [ data for data in dataset]

@app.route("/")
def top():
    return render_template("top.html", data=dataset)



@app.route("/_draw/<pairid>")
#@app.route("/_draw")
def drawmol(pairid):
    pairid = urllib.parse.unquote(pairid)

    res = collection.find_one({ "pairid" : pairid })
    moll = res['moll']
    molr = res['molr']
    trans = res['transform']
    core = res["context"]
    trans = trans.replace("[*:1]","[*]")
    trans = trans.replace("[*:2]","[*]")
    trans = trans.replace("[*:3]","[*]")


    transl, transr = trans.split(">>")

    svgl = chemistry.depictmol( moll, transl )
    svgr = chemistry.depictmol( molr, transr )

    return jsonify( ml=svgl, mr=svgr )

"""
@app.route('/')
def root():
    return "helloworld"
"""

if __name__ == '__main__':
    app.run( debug = True )
