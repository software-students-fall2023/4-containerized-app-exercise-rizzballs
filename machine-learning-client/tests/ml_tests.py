from machine_learning_client import ML
import speech_recognition as sr
import pytest

class Tests:
    def test_audio_text_conversion(self):
        actual = ML.audio_to_text(r"C:\Users\Administrator\Desktop\NYU_Undergrad\SoftwareEngineering\4-containerized-app-exercise-rizzballs\machine-learning-client\tests\richard.aiff")
        assert isinstance(actual, str), f"Expected audio_to_text to return a string. Instead it returned a {actual}"
        assert actual.lower() == "my name is richard", f"Expected the converted audio to be 'my name is richard'. Instead it returned {actual}"
    
    def test_grade_response(self):
        actual = ML.grade_response("hello hello hello hello hello")
        assert isinstance(actual, str), f"Expected grade_response to return a string. Instead it returned a {actual}"
        assert actual.lower() == "your response had hello appearing 5 times ugh appearing 0 times ", f"Expected the result to be 'your response had hello appearing 5 times ugh appearing 0 times '. Instead it returned {actual}"