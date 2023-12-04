FROM python:3.11


WORKDIR /machine-learning-client

COPY requirements.txt ./
# Install ffmpeg for format conversion
RUN apt-get update && apt-get install -y ffmpeg
RUN apt-get -y install libasound-dev
RUN apt-get -y install portaudio19-dev
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /machine-learning-client

EXPOSE 5001

ENV NAME World

CMD ["python", "machine_learning_client.py"]
