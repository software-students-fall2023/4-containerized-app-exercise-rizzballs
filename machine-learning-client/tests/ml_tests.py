"""
tests for machine-learning-client
"""
from machine_learning_client import ML
import os

class Tests:
    """Tests class for ml_tests.py"""
    def test_audio_text_conversion(self):
        """testing audio_to_text function in ML with valid audiofile as input"""
        PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        tests_path = "tests"
        file_name = "richard.aiff"
        file_path = os.path.join(PROJECT_ROOT, tests_path, file_name)
        print(file_path)
        actual = ML.audio_to_text(
            self, file_path
        )
        assert isinstance(
            actual, str
        ), f"Expected audio_to_text to return a string. Instead it returned a {actual}"
        assert (
            actual.lower() == "my name is richard"
        ), f"Expected the converted audio to be 'my name is richard'. Instead it returned {actual}"

    def test_grade_response(self):
        """testing grade_response function in ML with a transcription with 5 hellos"""
        actual = ML.grade_response(self, "hello hello hello hello hello")
        assert isinstance(
            actual, str
        ), f"Expected grade_response to return a string. Instead it returned a {actual}"
        assert (
            actual.lower()
            == "your response had hello appearing 5 times ugh appearing 0 times "
        ), f"Expected the result to be 'your response had hello appearing 5 times \
            ugh appearing 0 times '. Instead it returned {actual}"
