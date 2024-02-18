# Use an official Python runtime as a parent image
FROM python:3.12.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that Django will run on
EXPOSE 8000

# Define the command to run on container start
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]