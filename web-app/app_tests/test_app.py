"""
Tests for the web application.
"""

import tempfile
import pytest
from app import app

app_client = app.test_client()

@pytest.fixture
def client():
    """
    Fixture to configure the app for testing and provide a test client.
    """
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client

# pylint: disable=W0621
def test_root_page(client):
    """
    Test the root page and check if "Recording audio..." is present in the response.
    """
    response = client.get("/test_render_template")
    print("Response status code:", response.status_code)
    print("Response data:", response.data)
    assert b"Recording audio..." in response.data

# pylint: disable=W0613
def test_analyze_data(client, monkeypatch):
    """
    Test the analyze_data route with a mocked response.
    """
    # pylint: disable=W0613
    def mock_post(*args, **kwargs):
        class MockResponse:
            """
    Mock function for simulating a POST request.

    This function returns a mocked response with a JSON payload.

    Returns:
        MockResponse: An object with a `json` method and a `status_code` property.
    """
            @staticmethod
            def json():
                """
                Get the JSON representation of the mocked response.

                Returns:
                    dict: A dictionary representing the mocked JSON response.
                """
                return {"mocked": "response"}

            @property
            def status_code(self):
                """
                def status code
                """
                return 200

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        response = client.post("/analyzeData", data={"audio": (temp_file, "test.wav")})
        assert response.status_code == 200
        assert b"mocked" in response.data

# pylint: disable=W0613
def test_analyze_data_no_audio(client):
    """
    Test the analyze_data route without providing an audio file.
    """
    response = client.post("/analyzeData")
    assert response.status_code == 200
    assert b"No audio file provided" in response.data

# pylint: disable=W0613
def test_analyze_data_failed_request(client, monkeypatch):
    """
    Test the analyze_data route with a mocked failed response.
    """
    def mock_post(*args, **kwargs):
        class MockResponse:
            """
            mock response class
            """
            @staticmethod
            def json():
                """
                def json
                """
                return {"error": "Mocked error"}

            @property
            def status_code(self):
                """
                def status code
                """
                return 500

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        response = client.post("/analyzeData", data={"audio": (temp_file, "test.wav")})
        assert response.status_code == 500
        assert b"Failed to send and process audio" in response.data

if __name__ == "__main__":
    pytest.main(["-v", "test_app.py", "--cov=web-app"])
