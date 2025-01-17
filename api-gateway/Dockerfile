FROM alpine:3.12

# Install the necessary packages using apk (Alpine package manager)
RUN apk update \
  && apk add --no-cache \
  build-base \
  python3 \
  python3-dev \
  py3-pip \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt

# Copy the rest of the application code
COPY . /app

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Expose port 8080 for the application
EXPOSE 8080

# Set the default command to run the server
CMD ["python3", "server.py"]
