# Use an official Python runtime as a parent image
FROM python:3.9

# Copy the requirements.txt file into the container
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create user "app-user", and execute from it.
RUN useradd -ms /bin/bash appuser
USER appuser
RUN mkdir /home/appuser/app

# Copy everything
COPY --chown=appuser:appuser . /home/appuser/app
WORKDIR /home/appuser/app

# Set Python Path
ENV PYTHONPATH "${PYTHONPATH}:/app"
