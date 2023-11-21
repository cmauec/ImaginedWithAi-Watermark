FROM python:3.10-slim

ENV APP_HOME /app
ENV PORT 8080

WORKDIR $APP_HOME
# Copy local code to the container image.
COPY . .

RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn -t 900 --bind :$PORT --workers 1 --threads 8 app:app