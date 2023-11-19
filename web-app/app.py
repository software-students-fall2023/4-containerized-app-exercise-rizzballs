from flask import Flask, render_template, request, redirect, url_for, make_response, session
import os
from pymongo import MongoClient
import pymongo
import datetime
from bson.objectid import ObjectId
import sys

app = Flask('project4')

@app.route('/')
def RootPage():
    return render_template('root.html')

if __name__ == "__main__":
    PORT = os.getenv('PORT', 5000) 
    app.run(debug=True,port=PORT)
