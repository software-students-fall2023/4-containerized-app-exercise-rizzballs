FROM python:3.11
WORKDIR /app
ADD . /app

RUN apt-get -y update
RUN apt-get -y install libasound-dev
RUN apt-get -y install portaudio19-dev

COPY requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

# Define an environment variable... this will be available to programs running inside the container
ENV NAME World
# Run app.py when the container launches

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]