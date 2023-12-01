"""
app.py file that helps serve as the front end of our application
"""

import os
import subprocess
from flask import Flask, render_template, request, jsonify
import sys
from pydub import AudioSegment
import pymongo
from pymongo import MongoClient



app = Flask("project4")

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

client = MongoClient("mongodb://localhost:27017/")
db = client["ml_databse"]
collection = db["transcription"]


@app.route("/")
def root_page():
    """
    template to render root page
    """
    return render_template("root.html")


@app.route("/analyzeData", methods=["POST"])
def analyze_data():
    """
    Function to send genreated audio file to the machine learning client
    """
    try:
        if "audio" not in request.files:
            return jsonify({"status": "error", "message": "No audio file provided"})

        audio_file = request.files["audio"]
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], "user_audio.wav")
        audio_file.save(audio_path)

        # Converting the audio to the correct format
        webm_audio = AudioSegment.from_file(audio_path, format="webm")
        audio_path = audio_path.replace(".wav", "_converted.wav")
        webm_audio.export(audio_path, format="wav")

        print("Audio file saved at:", audio_path)
        python_interpreter = sys.executable
        ## this is getting the file path for teh machine_learning_client hopefuly this should work with windows as well. 
        machine_learning_client_path = os.path.join(PROJECT_ROOT, "machine-learning-client", "machine_learning_client.py")
        print(machine_learning_client_path)

        # Constructing the path to the audio file based on layout hopefully this works on window 
        web_app_directory = os.path.join(PROJECT_ROOT, "web-app")
        audio_file_name = os.path.join("uploads", "user_audio_converted.wav")
        audio_path = os.path.join(web_app_directory, audio_file_name)
        print("this is audio path: ", audio_path)
        print()

        
        result = subprocess.run(
            [python_interpreter, "-u", machine_learning_client_path, audio_path],
            capture_output=True,
            text=True,
            check=True,
        )
        ## this is if nothing is getting printed it on the terminal at first from the results of the subproceess being run on the machine_learning_client.py
        ## this should print out the results of the machine_learning_client.py and show the results
        print("Standard Output:")
        print(result.stdout)

        if result.returncode == 0:
            print("Process succeeded!")
        else:
            print("Process failed. Exit code:", result.returncode)

        return jsonify({"status": "success"})

    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": f"File not found: {str(e)}"})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Subprocess failed: {str(e)}"})

@app.route("/gradeTranscription", methods=["GET"])
def grade_transcription():
    """
    Function to generate a page giving a break down and grade of an audio transcript someone had just recorded
    """
    transcripts = db['transcripts']
    my_transcript = collection.find_one(sort=[('_id', -1)])
    grade = 0
    filler_words = 0
    buzz_words = 0
    """filler_words += my_transcript.find()"""
    filler_words += my_transcript.find("uh")
    filler_words += my_transcript.find("um")
    filler_words += my_transcript.find("ah")
    filler_words += my_transcript.find("like")
    filler_words += my_transcript.find("er")
    """buzz_words += my_transcript.find()"""
    buzz_words += my_transcript.find("education")
    buzz_words += my_transcript.find("major")
    buzz_words += my_transcript.find("college")
    buzz_words += my_transcript.find("university")
    buzz_words += my_transcript.find("experience")
    buzz_words += my_transcript.find("intern")
    buzz_words += my_transcript.find("job")
    buzz_words += my_transcript.find("certificate")
    buzz_words += my_transcript.find("qualification")
    buzz_words += my_transcript.find("work")
    buzz_words += my_transcript.find("interest")
    buzz_words += my_transcript.find("develop")
    buzz_words += my_transcript.find("fulfill")
    buzz_words += my_transcript.find("refine")
    if buzz_words == 0:
        bz_breakdown = "You did not use any buzz words. When answering this question, try to talk about your education, work experiences, major, or any jobs you had."
    elif 0 < buzz_words <= 5:
        bz_breakdown = f"You used {buzz_words} buzz words. A decent answer, but you can improve. Try to find more things to say about yourself professionally."
    elif buzz_words > 5:
        bz_breakdown = f"You used {buzz_words} buzz words. The topics of your answer are acceptable. Make sure to "
    if filler_words == 0:
        fw_breakdown = "You did not use any filler words. Or there was a problem with the audio transcript. Either way, remember to talk confidently and at a good pace."
    elif 0 < filler_words <= 5:
        fw_breakdown = f"You used {filler_words} filler words. From here, you just need to practice your answer until it comes out naturally. Make sure to keep relaxed."
    elif filler_words < 5:
        fw_breakdown = f"You used {filler_words} filler words. When giving your answer, try speaking slower and more clearly. Don't confuse yourself by thinking too far ahead."
    grade = (buzz_words * 3) - filler_words
    if grade > 20:
        grade = 20
    if grade < 0:
        grade = 0
    if grade == 0:
        grade_analysis = f"Your grade is {grade}/20. You should rethink your answer to be more focused and clearly thought out."
    elif 0 < grade <= 5:
        grade_analysis = f"Your grade is {grade}/20. Refine your answer by reflecting on your education, work experience, and relevant info."
    elif 5 < grade <= 10:
        grade_analysis = f"Your grade is {grade}/20. You're answer fulfills some of the necessary buzz words. If you have any more relevant data or ways to improve your speech, do so."
    elif 10 < grade <= 15:
        grade_analysis = f"Your grade is {grade}/20. You gave a very good response. Everything beyond this is fine tuning your response to the interviewer."
    elif 15 < grade <= 20:
        grade_analysis = f"Your grade is {grade}/20. This should be your go to answer, but it all depends on the interviewer. This answer should could out naturally and be your basis."
    grade_report = {
        "filler_words": fw_breakdown,
        "buzz_words": bz_breakdown,
        "grade_analysis": grade_analysis
    }
    return render_template('grade.html',grade_report = grade_report, activePage='grade.html')




if __name__ == "__main__":
    PORT = os.getenv("PORT", "5000")
    app.run(debug=True, port=PORT)
