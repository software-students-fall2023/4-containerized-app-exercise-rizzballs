from flask import Flask, render_template, request, jsonify
import os
import subprocess

app = Flask('project4')

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def RootPage():
    return render_template('root.html')

@app.route('/analyzeData', methods=['POST'])
def analyzeData():
    try:
        if 'audio' not in request.files:
            return jsonify({"status": "error", "message": "No audio file provided"})

        audio_file = request.files['audio']
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_audio.wav')
        audio_file.save(audio_path)


        print("Audio file saved at:", audio_path)  
        result = subprocess.run(["C:\\Users\\Andrew - User\\AppData\\Local\\Microsoft\\WindowsApps\\python.exe", "E:\\4-containerized-app-exercise-rizzballs\\machine-learning-client\\machine_learning_client.py", audio_path], capture_output=True, text=True)


        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    PORT = os.getenv('PORT', 5000) 
    app.run(debug=True, port=PORT)
