# Pull base image
FROM python:3.12

# # Use an Alpine-based Python image
# FROM python:3.12-alpine

# # Use a smaller base image
# FROM python:3.8-slim as builder

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Create directory for the code
RUN mkdir /code

# Set the working directory inside the container
WORKDIR /code

# # Install pipenv
# RUN pip install pipenv


# Copy requirements.txt to /code/
COPY requirements.txt /code/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Install dependencies using pipenv
# RUN pipenv install --deploy --ignore-pipfile


# Install Gunicorn
RUN pip install gunicorn


# Expose port 8000 to allow external access to the application
EXPOSE 8000

# Copy the current directory contents into the container at /code/
COPY . /code/
