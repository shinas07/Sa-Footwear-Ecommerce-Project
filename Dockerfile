FROM python:3.12

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures that Python output is sent straight to terminal (e.g., logs)
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/
# Expose port 8000 for external access
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
