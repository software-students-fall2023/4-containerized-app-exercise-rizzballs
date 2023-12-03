import sys
import os
import tempfile
import pytest
from flask import jsonify 
from flask import Flask
from flask import render_template
from app import app, collection


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_root_page(client):
    client.application.testing = True  # Set testing mode for the app

    response = client.get("/")
    assert response.status_code == 200
    assert b"template to render root page" in response.data

def test_display_results(client):
    response = client.get("/results")
    assert response.status_code == 200
    assert b"Function to render the results page" in response.data


def test_analyze_data(client, monkeypatch):
    # Mock the requests.post method
    def mock_post(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def json():
                return {"mocked": "response"}

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # Mock the request.files method
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        response = client.post("/analyzeData", data={"audio": (temp_file, "test.wav")})
        assert response.status_code == 200
        assert b"mocked" in response.data


def test_analyze_data_no_audio(client):
    response = client.post("/analyzeData")
    assert response.status_code == 200
    assert b"No audio file provided" in response.data


def test_analyze_data_failed_request(client, monkeypatch):
    # Mock the requests.post method to simulate a failed request
    def mock_post(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def json():
                return {"error": "Mocked error"}

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    # Mock the request.files method
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        response = client.post("/analyzeData", data={"audio": (temp_file, "test.wav")})
        assert response.status_code == 500
        assert b"Failed to send and process audio" in response.data


# Add more tests as needed

if __name__ == "__main__":
    pytest.main(["-v", "test_app.py", "--cov=web-app"])
