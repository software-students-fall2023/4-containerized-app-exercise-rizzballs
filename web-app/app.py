"""
app.py file that helps serve as the front end of our application
"""

import os
import subprocess
from flask import Flask, render_template, request, jsonify


app = Flask("project4")

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def root_page():
    """
    template to render root page
    """
    return render_template("root.html")


@app.route("/analyzeData", methods=["POST"])
def analyze_data():
    """
    Function to send genreated audio file to the machine learning client
    """
    try:
        if "audio" not in request.files:
            return jsonify({"status": "error", "message": "No audio file provided"})

        audio_file = request.files["audio"]
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], "user_audio.wav")
        audio_file.save(audio_path)

        print("Audio file saved at:", audio_path)
        result = subprocess.run(
            [
                "C:\\Users\\Andrew - User\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe",
                "E:\\4-containerized-app-exercise-rizzballs\\machine-learning-client\\machine_learning_client.py",  # pylint: disable=line-too-long
                audio_path,  # pylint: disable=line-too-long disable=trailing-whitespace
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        if result.returncode == 0:
            print("Process succeeded!")
        else:
            print("Process failed. Exit code:", result.returncode)

        return jsonify({"status": "success"})

    except FileNotFoundError as e:
        return jsonify({"status": "error", "message": f"File not found: {str(e)}"})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Subprocess failed: {str(e)}"})


if __name__ == "__main__":
    PORT = os.getenv("PORT", "5000")
    app.run(debug=True, port=PORT)
