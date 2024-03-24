# Pull base image
FROM python:3.12

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

# # Copy Pipfile and Pipfile.lock to /code/
# COPY Pipfile Pipfile.lock /code/

# Copy requirements.txt to /code/
COPY requirements.txt /code/


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# # Install dependencies using pipenv
# RUN pipenv install --deploy --ignore-pipfile

# Copy the current directory contents into the container at /code/
COPY . /code/

# Expose port 8000 to allow external access to the application
EXPOSE 8000

