import os
from pymongo import MongoClient
import pymongo
import datetime
import speech_recognition as sr
import sys

r = sr.recognizer()

def record_microphone():
    with sr.Microphone() as source:
        print("Please give your answer:")
        audio = r.listen(source)
    return audio

def audio_to_text(audio):
    try:
        transcription = r.recognize_google(audio)
        print(transcription)
    except sr.UnknownValueError:
        print("Sorry, we could not recognize your response.")
    except sr.RequestError as e:
        print("Sorry, there appears to be an error with Google Speech to Text")

def grade_response(transcription):
    print("working on it...")

def main():
    print("Tell me a little bit about yourself")
    audio = record_microphone()
    transcription = audio_to_text(audio)
    result = grade_response(transcription)

if __name__ == "__main__":
    main()