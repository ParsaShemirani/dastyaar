# Dockerfile
FROM python:latest

# create & switch to app dir
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# at runtime we'll mount the code, so no COPY for code here

# default command
CMD ["python", "main.py"]
