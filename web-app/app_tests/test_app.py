
import sys
import os
import tempfile
import pytest
from flask import jsonify 
from flask import Flask
from flask import render_template
from app import app, collection

client = app.test_client()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_root_page(client):
    response = client.get("/test_render_template")
    print("Response status code:", response.status_code)
    print("Response data:", response.data)
    assert b'Recording audio...' in response.data


def test_analyze_data(client, monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def json():
                return {"mocked": "response"}

            @property
            def status_code(self):
                return 200

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        response = client.post("/analyzeData", data={"audio": (temp_file, "test.wav")})
        assert response.status_code == 200
        assert b"mocked" in response.data

def test_analyze_data_no_audio(client):
    response = client.post("/analyzeData")
    assert response.status_code == 200
    assert b"No audio file provided" in response.data


def test_analyze_data_failed_request(client, monkeypatch):
    def mock_post(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def json():
                return {"error": "Mocked error"}

            @property
            def status_code(self):
                return 500

        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)

    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_file:
        response = client.post("/analyzeData", data={"audio": (temp_file, "test.wav")})
        assert response.status_code == 500
        assert b"Failed to send and process audio" in response.data

if __name__ == "__main__":
    pytest.main(["-v", "test_app.py", "--cov=web-app"])
