FROM python:3.11
WORKDIR /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

# Define an environment variable... this will be available to programs running inside the container
ENV NAME World
# Run app.py when the container launches
CMD ["python", "app.py"]