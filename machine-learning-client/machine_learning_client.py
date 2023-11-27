"""
Machine Learning python file providing conversion of audio 
to text transcription and analysis of audio transcription
"""
import os
import datetime
import sys
import pymongo
from pymongo import MongoClient
import pyaudio
import speech_recognition as sr

r = sr.Recognizer()
pa = pyaudio.PyAudio()


def list_all_mic():
    """
    List all available microphone device
    """
    if len(sr.Microphone.list_microphone_names()) == 0:
        print("no device available")
        return

    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f'Microphone with name "{name}"')
        print(f" found for `Microphone(device_index={index})`")


def record_microphone():
    """Function for recording microphone input"""
    list_all_mic()  # Use for debug
    mc = None
    try:
        mc = sr.Microphone()
        print("Mic init successful")
    except OSError:
        mc = sr.Microphone(0)
        print("no default mic")
    with mc as source:
        print("Please give your answer:")
        audio = r.listen(source)
    return audio


def audio_to_text(audio):
    """Function for converting audio file to text transcription"""
    try:
        transcription = r.recognize_google(audio)
        print(transcription)
        print(type(transcription))
    except sr.UnknownValueError:
        print("Sorry, we could not recognize your response.")
    except sr.RequestError:
        print("Sorry, there appears to be an error with Google Speech to Text")
    return transcription


def grade_response(transcription):
    """
    Give out a score based on the transcribed audio


    Args:
        transcription (str): transcribed audio
    """
    print("working on it...")
    grade = transcription
    return grade


def main():
    """Main Method"""
    print("Tell me a little bit about yourself")
    audio = record_microphone()
    transcription = audio_to_text(audio)
    result = grade_response(transcription)
    print(result)


if __name__ == "__main__":
    main()
