# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements/local.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to the location of manage.py
WORKDIR /app/Envios

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the migrations and start the development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
