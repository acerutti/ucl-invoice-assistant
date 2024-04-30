# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.9

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install -r requirements.txt

# Install tesseract
RUN apt-get update -qqy && apt-get install -qqy \
        tesseract-ocr \
        libtesseract-dev

# Install pdf2image, pytesseract, and Pillow
RUN pip install pdf2image
RUN pip install pytesseract
RUN pip install Pillow

RUN go build -o uploader cmd/uploader/uploader.go
EXPOSE 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
ENV GOPATH=/app
CMD ["/app/uploader", ":8080"]
