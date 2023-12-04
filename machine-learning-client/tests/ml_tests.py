"""
tests for machine-learning-client
"""
import os
import machine_learning_client as ML # pylint: disable=import-error
import pytest









# Mocking dependencies and functions
@pytest.fixture
def mock_dependencies(monkeypatch):
    """Setup Mock"""
    monkeypatch.setattr(
        "machine_learning_client.audio_to_text",
        lambda *args, **kwargs: "mocked_transcription",
    )
    monkeypatch.setattr(
        "machine_learning_client.grade_transcription",
        lambda *args, **kwargs: "mocked_grade",
    )
    monkeypatch.setattr(
        "machine_learning_client.add_transcription_mongo", lambda *args, **kwargs: None
    )


# Create a fixture for the Flask application with CORS enabled
@pytest.fixture
def client():
    """Create a fixture for the Flask application with CORS enabled"""
    with ML.app.test_client() as client: # pylint: disable=redefined-outer-name
        yield client


# Test the route handler with a valid audio file
def test_analyze_audios_valid_audio(client): # pylint: disable=redefined-outer-name
    """Test the route handler with a valid audio file"""
    audio_file_path = os.path.join(os.path.dirname(__file__), "test_audio.webm")
    print(audio_file_path)
    with open(audio_file_path, "rb") as audio_file:
        response = client.post(
            "/analyzeAudio", data={"audio": (audio_file, "test_audio.webm")}
        )

    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Audio analysis completed"}


# Test the route handler without including an audio file
def test_analyze_audios_no_audio_file(client): # pylint: disable=redefined-outer-name
    """Test the route handler without including an audio file"""
    response = client.post("/analyzeAudio")

    assert response.status_code == 400
    assert response.json == {"status": "error", "message": "No audio file provided"}


# Test the route handler with an exception during audio processing
def test_analyze_audios_exception(client, monkeypatch): # pylint: disable=redefined-outer-name
    """Test the route handler with an exception during audio processing"""
    monkeypatch.setattr(
        "machine_learning_client.audio_to_text",
        lambda *args, **kwargs: Exception("Mocked exception"),
    )

    audio_file_path = os.path.join(os.path.dirname(__file__), "test_audio.webm")

    with open(audio_file_path, "rb") as audio_file:
        response = client.post(
            "/analyzeAudio", data={"audio": (audio_file, "test_audio.webm")}
        )

    assert response.status_code == 500
    assert response.json["status"] == "error"

    # Asserting that the error message starts with "An error occurred:"
    assert response.json["message"].startswith("An error occurred:")


class Tests:
    """Tests class for ml_tests.py"""

    def test_audio_text_conversion(self):
        """testing audio_to_text function in ML with valid audiofile as input"""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "richard.aiff"
        file_path = os.path.join(project_root, tests_path, file_name)
        print(file_path)
        actual = ML.audio_to_text(file_path)
        assert isinstance(
            actual, str
        ), f"Expected audio_to_text to return a string. Instead it returned a {actual}"
        assert (
            actual.lower() == "my name is richard"
        ), f"Expected the converted audio to be 'my name is richard'. Instead it returned {actual}"

    def test_grade_transcription_good(self):
        """testing grade_transcription function in ML with a recording of all filler && buzz words""" # pylint: disable=line-too-long
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "filler.aiff"
        file_path = os.path.join(project_root, tests_path, file_name)
        actual = ML.grade_transcription(ML.audio_to_text(file_path))
        assert isinstance(
            actual, dict
        ), f"Expected grade_transcription to return a dict. Instead it returned a {actual}"
        assert actual == {
            "filler_words": "You used 7 filler words. When giving your answer, try speaking slower and more clearly. Don't confuse yourself by thinking too far ahead.", # pylint: disable=line-too-long
            "buzz_words": "You used 14 buzz words. The topics of your answer are acceptable. Make sure to ", # pylint: disable=line-too-long
            "grade_analysis": "Your grade is 20/20. This should be your go to answer, but it all depends on the interviewer. This answer should could out naturally and be your basis.", # pylint: disable=line-too-long
        }, f"Expected a 20 grade report. Instead it returned {actual}"

    def test_grade_transcription_gt5(self):
        """testing grade_transcription function in ML with a recording of many filler/buzz words"""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "gt5.aiff"
        file_path = os.path.join(project_root, tests_path, file_name)
        actual = ML.grade_transcription(ML.audio_to_text(file_path))
        assert isinstance(
            actual, dict
        ), f"Expected grade_transcription to return a dict. Instead it returned a {actual}"
        assert actual == {
            "filler_words": "You did not use any filler words. Or there was a problem with the audio transcript. Either way, remember to talk confidently and at a good pace.", # pylint: disable=line-too-long
            "buzz_words": "You did not use any buzz words. When answering this question, try to talk about your education, work experiences, major, or any jobs you had.", # pylint: disable=line-too-long
            "grade_analysis": "Your grade is 0/20. You should rethink your answer to be more focused and clearly thought out.", # pylint: disable=line-too-long
        }, f"Expected a 0 grade report. Instead it returned {actual}"

    def test_grade_transcription_5(self):
        """testing grade_transcription function in ML with a recording of 5 filler/buzz"""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "5.aiff"
        file_path = os.path.join(project_root, tests_path, file_name)
        actual = ML.grade_transcription(ML.audio_to_text(file_path))
        assert isinstance(
            actual, dict
        ), f"Expected grade_transcription to return a dict. Instead it returned a {actual}"
        assert actual == {
            "filler_words": "You used 16 filler words. When giving your answer, try speaking slower and more clearly. Don't confuse yourself by thinking too far ahead.", # pylint: disable=line-too-long
            "buzz_words": "You did not use any buzz words. When answering this question, try to talk about your education, work experiences, major, or any jobs you had.", # pylint: disable=line-too-long
            "grade_analysis": "Your grade is 0/20. You should rethink your answer to be more focused and clearly thought out.", # pylint: disable=line-too-long
        }, f"Expected a 0 grade report. Instead it returned {actual}"
