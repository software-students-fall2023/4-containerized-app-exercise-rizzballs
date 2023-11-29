FROM python:3.11

WORKDIR /app

#COPY Pipfile Pipfile.lock ./

#RUN pip install pipenv && pipenv install --deploy --ignore-pipfile
RUN apt-get -y update
RUN apt-get -y install libasound-dev
RUN apt-get -y install portaudio19-dev
# Set up microphone access in the Dockerfile
RUN apt-get update && apt-get install -y alsa-utils

WORKDIR /usr/src/app
COPY requirements.txt ./

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "machine_learning_client.py"]
