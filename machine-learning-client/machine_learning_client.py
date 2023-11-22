from flask import Flask, render_template, request, redirect, url_for, make_response, session
import os
from pymongo import MongoClient
import pymongo
import datetime
from bson.objectid import ObjectId
import sys

app = Flask('project4')

@app.route("/process_wav", methods=['GET', 'POST'])
def process_wav():
    if request.method == 'POST':
        audio_file = request.form.get("audio-recording")
        dir = 'audio/'+str(audio_file)

if __name__ == "__main__":
    PORT = os.getenv('PORT', 5000) 
    app.run(debug=True,port=PORT)
