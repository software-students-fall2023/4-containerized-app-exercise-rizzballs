import os
from pymongo import MongoClient
import pymongo
import datetime
import pyaudio
import speech_recognition as sr
import sys

r = sr.Recognizer()
pa = pyaudio.PyAudio()
def listAllMic():
    """
    List all available microphone device
    """
    if (len(sr.Microphone.list_microphone_names()) == 0):
        print("no device available")
        return
    
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

def record_microphone():
    listAllMic()                 #Use for debug
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
    try:
        transcription = r.recognize_google(audio)
        print(transcription)
        print(type(transcription))
    except sr.UnknownValueError:
        print("Sorry, we could not recognize your response.")
    except sr.RequestError as e:
        print("Sorry, there appears to be an error with Google Speech to Text")

def grade_response(transcription):
    """
    Give out a score based on the transcribed audio


    Args:
        transcription (str): transcribed audio
    """
    print("working on it...")
    

def main():
    print("Tell me a little bit about yourself")
    audio = record_microphone()
    transcription = audio_to_text(audio)
    result = grade_response(transcription)

if __name__ == "__main__":
    main()