"""
tests for machine-learning-client
"""
import machine_learning_client as ML
import os
import pytest
from flask import Flask
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask.testing import FlaskClient
from flask_cors import CORS
from pytest_flask import fixtures
from machine_learning_client import audio_to_text, grade_transcription, add_transcription_mongo
# Mocking dependencies and functions
@pytest.fixture
def mock_dependencies(monkeypatch):
    monkeypatch.setattr("machine_learning_client.audio_to_text", lambda *args, **kwargs: "mocked_transcription")
    monkeypatch.setattr("machine_learning_client.grade_transcription", lambda *args, **kwargs: "mocked_grade")
    monkeypatch.setattr("machine_learning_client.add_transcription_mongo", lambda *args, **kwargs: None)

# Create a fixture for the Flask application with CORS enabled
@pytest.fixture
def client():
    with ML.app.test_client() as client:
        yield client

# Test the route handler with a valid audio file
def test_analyze_audios_valid_audio(client):
    audio_file_path = os.path.join(os.path.dirname(__file__), "test_audio.webm")
    print(audio_file_path)
    with open(audio_file_path, "rb") as audio_file:
        response = client.post("/analyzeAudio", data={"audio": (audio_file, "test_audio.webm")})

    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Audio analysis completed"}

# Test the route handler without including an audio file
def test_analyze_audios_no_audio_file(client):
    response = client.post("/analyzeAudio")

    assert response.status_code == 400
    assert response.json == {"status": "error", "message": "No audio file provided"}

# Test the route handler with an exception during audio processing
def test_analyze_audios_exception(client, monkeypatch):
    monkeypatch.setattr("machine_learning_client.audio_to_text", lambda *args, **kwargs: Exception("Mocked exception"))

    audio_file_path = os.path.join(os.path.dirname(__file__), "test_audio.webm")

    with open(audio_file_path, "rb") as audio_file:
        response = client.post("/analyzeAudio", data={"audio": (audio_file, "test_audio.webm")})

    assert response.status_code == 500
    assert response.json["status"] == "error"

    # Asserting that the error message starts with "An error occurred:"
    assert response.json["message"].startswith("An error occurred:")

class Tests:
    """Tests class for ml_tests.py"""
    def test_audio_text_conversion(self):
        """testing audio_to_text function in ML with valid audiofile as input"""
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "richard.aiff"
        file_path = os.path.join(PROJECT_ROOT, tests_path, file_name)
        print(file_path)
        actual = ML.audio_to_text(file_path)
        assert isinstance(
            actual, str
        ), f"Expected audio_to_text to return a string. Instead it returned a {actual}"
        assert (
            actual.lower() == "my name is richard"
        ), f"Expected the converted audio to be 'my name is richard'. Instead it returned {actual}"
    
    
            

    def test_grade_transcription_good(self):
        """testing grade_transcription function in ML with a recording of all filler && buzz words"""
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "filler.aiff"
        file_path = os.path.join(PROJECT_ROOT, tests_path, file_name)
        actual = ML.grade_transcription(ML.audio_to_text(file_path))
        assert isinstance(actual, dict), f"Expected grade_transcription to return a dict. Instead it returned a {actual}"
        assert (actual == {"filler_words": "You used 7 filler words. When giving your answer, try speaking slower and more clearly. Don't confuse yourself by thinking too far ahead.",
        "buzz_words": "You used 14 buzz words. The topics of your answer are acceptable. Make sure to ",
        "grade_analysis": "Your grade is 20/20. This should be your go to answer, but it all depends on the interviewer. This answer should could out naturally and be your basis."}
                ), f"Expected a 20 grade report. Instead it returned {actual}"
    
    def test_grade_transcription_gt5(self):
        """testing grade_transcription function in ML with a recording of many filler/buzz words"""
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "gt5.aiff"
        file_path = os.path.join(PROJECT_ROOT, tests_path, file_name)
        actual = ML.grade_transcription(ML.audio_to_text(file_path))
        assert isinstance(actual, dict), f"Expected grade_transcription to return a dict. Instead it returned a {actual}"
        assert (actual == {"filler_words": "You did not use any filler words. Or there was a problem with the audio transcript. Either way, remember to talk confidently and at a good pace.",
        "buzz_words": "You did not use any buzz words. When answering this question, try to talk about your education, work experiences, major, or any jobs you had.",
        "grade_analysis": "Your grade is 0/20. You should rethink your answer to be more focused and clearly thought out."}
                ), f"Expected a 0 grade report. Instead it returned {actual}"
    
    def test_grade_transcription_5(self):
        """testing grade_transcription function in ML with a recording of 5 filler/buzz"""
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "5.aiff"
        file_path = os.path.join(PROJECT_ROOT, tests_path, file_name)
        actual = ML.grade_transcription(ML.audio_to_text(file_path))
        assert isinstance(actual, dict), f"Expected grade_transcription to return a dict. Instead it returned a {actual}"
        assert (actual == {"filler_words": "You used 16 filler words. When giving your answer, try speaking slower and more clearly. Don't confuse yourself by thinking too far ahead.",
        "buzz_words": "You did not use any buzz words. When answering this question, try to talk about your education, work experiences, major, or any jobs you had.",
        "grade_analysis": "Your grade is 0/20. You should rethink your answer to be more focused and clearly thought out."}
                ), f"Expected a 0 grade report. Instead it returned {actual}"