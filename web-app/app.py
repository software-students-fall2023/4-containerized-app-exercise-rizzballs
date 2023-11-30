<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import os
import subprocess
=======
"""Module designed to supplement front end webpage"""
import os
import datetime
import sys
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)
from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
>>>>>>> 5a0af371e4dbfe2fdc0328cf9e5f1e13a84def20

app = Flask("project4")

<<<<<<< HEAD
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def RootPage():
    return render_template('root.html')

@app.route('/analyzeData', methods=['POST'])
def analyzeData():
    try:
        if 'audio' not in request.files:
            return jsonify({"status": "error", "message": "No audio file provided"})

        audio_file = request.files['audio']
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_audio.wav')
        audio_file.save(audio_path)


        print("Audio file saved at:", audio_path)  
        result = subprocess.run(["C:\\Users\\Andrew - User\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe", "E:\\4-containerized-app-exercise-rizzballs\\machine-learning-client\\machine_learning_client.py", audio_path], capture_output=True, text=True)


        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
=======

@app.route("/")
def root_page():
    """Root page route"""
    return render_template("root.html")


@app.route("/analyze_data", methods=["POST"])
def anaylze_data():
    """Analyze data by sending it to the ml client"""
    return
>>>>>>> 5a0af371e4dbfe2fdc0328cf9e5f1e13a84def20


if __name__ == "__main__":
<<<<<<< HEAD
    PORT = os.getenv('PORT', 5000) 
=======
    PORT = os.getenv("PORT", 5000)
>>>>>>> 5a0af371e4dbfe2fdc0328cf9e5f1e13a84def20
    app.run(debug=True, port=PORT)
