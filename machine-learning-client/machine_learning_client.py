"""
Machine Learning python file providing conversion of audio 
to text transcription and analysis of audio transcription
"""
from enum import Enum
import sys
import pyaudio
import pymongo
from pymongo import MongoClient
import speech_recognition as sr


class ML:
    """Machine Learning class functions"""

    pa = pyaudio.PyAudio()

    def list_all_mic(self):
        """
        List all available microphone device
        """
        if len(sr.Microphone.list_microphone_names()) == 0:
            print("no device available")
            return

        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f'Microphone with name "{name}"')
            print(f" found for Microphone(device_index={index})")

    def record_microphone(self):
        """Function for recording microphone input"""
        ML.list_all_mic(self)  # Use for debug
        mc = None
        try:
            mc = sr.Microphone()
            print("Mic init successful")
        except OSError:
            mc = sr.Microphone(0)
            print("no default mic")
        with mc as source:
            print("Please give your answer:")
            r = sr.Recognizer()
            audio = r.listen(source)
        return audio
    
    def add_transcription_mongo(self, transcription):
        """
        Save transcription to MongoDB
        """
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["ml_databse"]
            collection = db["transcription"]

            data = {"transcription": transcription}
            result = collection.insert_one(data)
            print(f"Transcription saved to MongoDB with ID: {result.inserted_id}")

        except Exception as e:
            print(f"Error saving transcription to MongoDB: {e}")

    def audio_to_text(self, audio_file_string):
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
        return transcription

    class BuzzWord(Enum):
        """List of Buzzwords"""

        HELLO = "hello"
        UGH = "ugh"

    def grade_response(self, transcription):
        """
        Give out a score based on the transcribed audio


        Args:
            transcription (str): transcribed audio
        """
        print("working on it...")
        grade = "Your response had "
        for bw in ML.BuzzWord:
            bw_count = (str)(transcription.lower().count(bw.value))
            grade += bw.value + " appearing " + bw_count + " times "
        return grade


def main():
    """Main Method"""

    """
    ## this is to test if you just want to run the machine_learning_client.py by itself.
    print("Tell me a little bit about yourself")
    ml = ML()
    audio = r"/Users/keioshima/Documents/projects-fall-2023/4-containerized-app-exercise-rizzballs/web-app/uploads/user_audio.wav"
    replace: /Users/keioshima/Documents with the neccessary string so for windows it may start with C// or something
    transcription = ml.audio_to_text(audio)
    result = ml.grade_response(transcription)
    print(result)
    print("test main")
    
    """

    try:
        print("Tell me a little bit about yourself")
        ml = ML()
        # Check if command-line arguments are provided
        if len(sys.argv) != 2:
            print("Usage: python machine_learning_client.py <audio_path>")
            sys.exit(1)

        audio_path = sys.argv[1]
        print("This is audio path: ", audio_path)

        transcription = ml.audio_to_text(audio_path)
        print(transcription)
        ml.add_transcription_mongo(transcription)
        result = ml.grade_response(transcription)
        print(result)
        
    except Exception as e:
        print(f"Error in machine_learning_client.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
