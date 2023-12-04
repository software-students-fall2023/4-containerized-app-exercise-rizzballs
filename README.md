# Interview Review WebApp
![WebApp Subsystems build test](https://github.com/software-students-fall2023/4-containerized-app-exercise-rizzballs/actions/workflows/lint.yml/badge.svg)
![WebApp MLC test](https://github.com/software-students-fall2023/4-containerized-app-exercise-rizzballs/actions/workflows/ml-test.yml/badge.svg)
![WebApp WebApp test](https://github.com/software-students-fall2023/4-containerized-app-exercise-rizzballs/actions/workflows/app-test.yml/badge.svg)

## What is our WebApp?

Our WebApp is designed to help users practice and improve their interview skills. When prompted, users will speak into the microphhone and answer a generic interview question. Utilizing [SpeechRecogntion](https://pypi.org/project/SpeechRecognition/), the app will record the interview and breakdown the answer given, giving a rating based on specified critera and words used. Then, it is compared to other user attempts to give a comparison and return statistics of the prompted user.

## Installation and Usage

### Prerequisites
1. ensure you have python 3.11 or higher installed 
2. ensure you have have Docker installed and running on your computer.
3. optionally have docker Desktop 
### Github Repository Cloning Option
1. Clone the directory through Git Bash with the command:

```
git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-rizzballs.git
```

2. Open Docker Desktop or a new terminal 

3. In your command prompt/terminal, access the directory where you cloned the repository:
```
cd "path_to_directory"
```

4. From here, run the commands:
```
docker-compose build
docker-compose up
```
5. Now, access the http://127.0.0.1:5000/ in your browser of choice.

6. to end the session 
```
docker-compose stop
```
or 
```
docker-compose down
```

### Website Access Option

With deployment to Digital Ocean, you can access our webapp directly by typing in your url: 165.227.220.8:5000

#### Note for MacOS Users:
1. After doing docker-compose build and then running docker-compose up leads you to this error: 
```
Error response from daemon: Ports are not available: listen tcp 0.0.0.0:5000: bind: address already in use.

```
2. To trouble shoot this in your terminal, run:
```
lsof -i tcp:5000
```
3. and kill that process by doing: 
```
kill -9 <ProcessID>
```
4. If however, two processes appear when you run the above command then "Airplay" should be turned off
5. To do so go to system settings -> search up air drop and click on "AirDrop and Handoff" -> from there turn off "AirPlay receiver".
6. Then try docker-compose up again. 

#### Special Instructions for Chrome Users
If you are using Google Chrome, the application may not work due to microphone access problems. You can bypass security restrictions due to the site being hosted on a bare IP address by:

1. **Open Chrome Flags**:
   - Type `chrome://flags/#unsafely-treat-insecure-origin-as-secure` in your Chrome address bar and press `Enter`.

2. **Enable Insecure Origins**:
   - In the "Insecure origins treated as secure" section, add `http://165.227.220.8:5000`.
   - Change the dropdown from 'Disabled' to 'Enabled'.

3. **Relaunch Chrome**:
   - Click the 'Relaunch' button to apply the changes.

Warning: This is only a workaround and should be used cautiously as it can introduce security risks. It's recommended only for testing or non-sensitive use.


### Install ffmpeg (Windows)
1. Go to the official ffmpeg website, hover over the windows icon, and click Windows builds from gyan.dev
2. Download ffmpeg-git-full.7z under "latest git master branch build
3. Extract the files to desired location
4. Open your System Environment Variables on your windows control panel. Under User Variables, click on "Path" under "User Variables" and click edit. Add the directory to the bin of the extracted ffmpeg. It should look something like "[Folder Location]\ffmpeg-2023-11-28-git-47e214245b-full_build\bin". Press Ok until you're exited completely out of System Properties. 

This should allow you to use ffmpeg while using our program. Make sure to use a clean shell to make sure it is up to date

### Install ffmpeg (Windows)
1. in your terminal type in 
```
brew install ffmpeg 
```
This should allow you to use ffmpeg while using our program

## Test Coverage

You can view our most recent coverage results on your Github actions.

This is our test coverage as of December 4th, 2023 for the machine learning client:

```
---------- coverage: platform linux, python 3.11.6-final-0 -----------
Name                                                                                                                                                 Stmts   Miss  Cover
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/home/runner/work/4-containerized-app-exercise-rizzballs/4-containerized-app-exercise-rizzballs/machine-learning-client/machine_learning_client.py     129     10    92%
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                                                                                  129     10    92%

======================== 7 passed, 2 warnings in 41.67s ========================
```

This is our test coverage as of December 4th, 2023 for the web app:

```
test_app.py ....                                                         [100%]

---------- coverage: platform linux, python 3.11.6-final-0 -----------
Name                                                                                                             Stmts   Miss  Cover
------------------------------------------------------------------------------------------------------------------------------------
/home/runner/work/4-containerized-app-exercise-rizzballs/4-containerized-app-exercise-rizzballs/web-app/app.py      38      8    79%
------------------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                                               38      8    79%


============================== 4 passed in 0.43s ===============================
```

## Contributors

- [Andrew Huang](https://github.com/andrew0022)
- [Kei Oshima](https://github.com/KeiOshima)
- [Richard Qu](https://github.com/kingslayerrq)
- [Ryan Horng](https://github.com/Ryan-Horng)