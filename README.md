# Interview Review WebApp
![WebApp Machine Learning build test](https://github.com/software-students-fall2023/4-containerized-app-exercise-rizzballs/actions/workflows/event-logger.yml/badge.svg)
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
### Method 1: Cloning the Github Repository
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

### Note for MacOS Users:
1. after doing docker-compose build and then running docker-compose up leads you to this error: 
```
Error response from daemon: Ports are not available: listen tcp 0.0.0.0:5000: bind: address already in use.

```
2. to trouble shoot thisin your terminal run:
```
lsof -i tcp:5000
```
3. and kill that process by doing 
```
kill -9 <ProcessID>
```
4. if however, two processes appear when you run the above command then "Airplay" should be turned off
5. to do so go to system settings -> search up air drop and click on "AirDrop and Handoff" -> from there turn off "AirPlay receiver".
6. and then try docker-compose up again. 


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

## Contributors

- [Andrew Huang](https://github.com/andrew0022)
- [Kei Oshima](https://github.com/KeiOshima)
- [Richard Qu](https://github.com/kingslayerrq)
- [Ryan Horng](https://github.com/Ryan-Horng)