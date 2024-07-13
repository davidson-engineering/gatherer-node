# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install required packages
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git g++ -y

# Update pip
RUN python -m pip install --upgrade pip

# Install package using pip
COPY ./ ./app
WORKDIR /app
RUN pip install .

# # Creates a non-root user with an explicit UID and adds permission to access the /app folder
# # For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN addgroup --gid 1001 appusergroup
# RUN adduser -u 1001 --gid 1001 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser
