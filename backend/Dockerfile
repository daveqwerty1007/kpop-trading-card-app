# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the image
COPY . /app

# Set the environment variables
ENV FLASK_APP=app/main.py
ENV FLASK_ENV=development

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
