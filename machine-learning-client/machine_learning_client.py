"""
Machine Learning python file providing conversion of audio 
to text transcription and analysis of audio transcription
"""


import os
import pyaudio


from pymongo import MongoClient
import speech_recognition as sr
from flask_cors import CORS
from flask import Flask, request, jsonify
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)

## python3 machine_learning_client.py

client = MongoClient("mongodb://mongodb:27017/")
db = client["ml_databse"]
collection = db["transcription"]


app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

pa = pyaudio.PyAudio()


def add_transcription_mongo(transcription, grade_report):
    """
    Save transcription to MongoDB
    """
    try:
        data = {"transcription": transcription, "grade_report": grade_report}
        result = collection.insert_one(data)
        print(f"Transcription saved to MongoDB with ID: {result.inserted_id}")

    except Exception as e: # pylint: disable=broad-exception-caught
        print(f"Error saving transcription to MongoDB: {e}")


def audio_to_text(audio_file_string):
    """Function for converting audio file to text transcription"""
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_string) as source:
        ad = r.listen(source)
    try:
        transcription = r.recognize_google(ad)
        print(transcription)
        print(type(transcription))
    except sr.UnknownValueError:
        print("Sorry, we could not recognize your response.")
    except sr.RequestError:
        print("Sorry, there appears to be an error with Google Speech to Text")

    print("success!! we transcribed it")
    return transcription



def grade_transcription(transcription_text): # pylint: disable=too-many-branches,too-many-statements
    """
    Function to generate a page giving a break down and grade of an audio transcript someone had just recorded # pylint: disable=line-too-long
    """

    grade = 0
    filler_words = 0
    buzz_words = 0
    filler_words += transcription_text.lower().count("uh")
    filler_words += transcription_text.lower().count("um")
    filler_words += transcription_text.lower().count("ah")
    filler_words += transcription_text.lower().count("like")
    filler_words += transcription_text.lower().count("er")
    buzz_words += transcription_text.lower().count("education")
    buzz_words += transcription_text.lower().count("major")
    buzz_words += transcription_text.lower().count("college")
    buzz_words += transcription_text.lower().count("university")
    buzz_words += transcription_text.lower().count("experience")
    buzz_words += transcription_text.lower().count("intern")
    buzz_words += transcription_text.lower().count("job")
    buzz_words += transcription_text.lower().count("certificate")
    buzz_words += transcription_text.lower().count("qualification")
    buzz_words += transcription_text.lower().count("work")
    buzz_words += transcription_text.lower().count("interest")
    buzz_words += transcription_text.lower().count("develop")
    buzz_words += transcription_text.lower().count("fulfill")
    buzz_words += transcription_text.lower().count("refine")
    print("this value of filler word: ", filler_words)
    print("this value of buzz word: ", buzz_words)
    fw_breakdown = ""
    bz_breakdown = ""
    grade_analysis = ""

    if buzz_words == 0:
        bz_breakdown = "You did not use any buzz words. When answering this question, try to talk about your education, work experiences, major, or any jobs you had." # pylint: disable=line-too-long
    elif 0 < buzz_words <= 5:
        bz_breakdown = f"You used {buzz_words} buzz words. A decent answer, but you can improve. Try to find more things to say about yourself professionally." # pylint: disable=line-too-long
    else:
        bz_breakdown = f"You used {buzz_words} buzz words. The topics of your answer are acceptable. Make sure to keep in mind your wording and topics." # pylint: disable=line-too-long
    if filler_words == 0:
        fw_breakdown = "You did not use any filler words. Or there was a problem with the audio transcript. Either way, remember to talk confidently and at a good pace." # pylint: disable=line-too-long
    elif 0 < filler_words <= 5:
        fw_breakdown = f"You used {filler_words} filler words. From here, you just need to practice your answer until it comes out naturally. Make sure to keep relaxed." # pylint: disable=line-too-long
    else:
        fw_breakdown = f"You used {filler_words} filler words. When giving your answer, try speaking slower and more clearly. Don't confuse yourself by thinking too far ahead." # pylint: disable=line-too-long
    grade = (buzz_words * 3) - filler_words
    print(grade)
    if grade > 20:
        grade = 20
    elif grade < 0:
        grade = 0
    if grade == 0:
        grade_analysis = f"Your grade is {grade}/20. You should rethink your answer to be more focused and clearly thought out." # pylint: disable=line-too-long
    elif 0 < grade <= 5:
        grade_analysis = f"Your grade is {grade}/20. Refine your answer by reflecting on your education, work experience, and relevant info." # pylint: disable=line-too-long
    elif 5 < grade <= 10:
        grade_analysis = f"Your grade is {grade}/20. You're answer fulfills some of the necessary buzz words. If you have any more relevant data or ways to improve your speech, do so." # pylint: disable=line-too-long
    elif 10 < grade <= 15:
        grade_analysis = f"Your grade is {grade}/20. You gave a very good response. Everything beyond this is fine tuning your response to the interviewer." # pylint: disable=line-too-long
    else:
        grade_analysis = f"Your grade is {grade}/20. This should be your go to answer, but it all depends on the interviewer. This answer should could out naturally and be your basis." # pylint: disable=line-too-long
    grade_report = {
        "filler_words": fw_breakdown,
        "buzz_words": bz_breakdown,
        "grade_analysis": grade_analysis,
    }
    print(fw_breakdown)
    print(bz_breakdown)
    print(grade_analysis)
    return grade_report


@app.route("/analyzeAudio", methods=["POST"])
def analyze_Audios(): # pylint: disable=invalid-name
    """
    Endpoint to receive and analyze audio file
    """
    try:
        if "audio" not in request.files:
            return (
                jsonify({"status": "error", "message": "No audio file provided"}),
                400,
            )

        audio_file = request.files["audio"]

        # Delete existing files if they exist
        existing_audio_path = os.path.join(
            app.config["UPLOAD_FOLDER"], "user_audio.wav"
        )
        if os.path.exists(existing_audio_path):
            os.remove(existing_audio_path)

        existing_converted_path = existing_audio_path.replace(".wav", "_converted.wav")
        if os.path.exists(existing_converted_path):
            os.remove(existing_converted_path)

        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], "user_audio.wav")
        audio_file.save(audio_path)

        # Convert the audio to the correct format (webm to wav)
        webm_audio = AudioSegment.from_file(audio_path, format="webm")
        converted_audio_path = audio_path.replace(".wav", "_converted.wav")
        webm_audio.export(converted_audio_path, format="wav")

        ml_directory = os.path.join(PROJECT_ROOT, "machine-learning-client")
        audio_file_name = os.path.join("uploads", "user_audio_converted.wav")
        true_audio_path = os.path.join(ml_directory, audio_file_name)
        true_audio_path_str = str(true_audio_path)
        print(true_audio_path)
        # Call your functions from ml.py to process the audio
        print("calling audio to text method")
        transcription = audio_to_text(true_audio_path_str)
        print(transcription)
        print("calling grade to text method")
        graded_transcription = grade_transcription(transcription)
        add_transcription_mongo(transcription, graded_transcription)

        print("we did it baby")
        return (
            jsonify({"status": "success", "message": "Audio analysis completed"}),
            200,
        )

    except Exception as e: # pylint: disable=broad-exception-caught
        return (
            jsonify({"status": "error", "message": f"An error occurred: {str(e)}"}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5001")), debug=True)
