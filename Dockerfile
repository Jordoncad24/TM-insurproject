# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV MONGO_URI="mongodb+srv://jordoncad24:Bionicle24.@insuranceproject.sfyyy.mongodb.net/insurance?retryWrites=true&w=majority"
# Expose the port that the Flask app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "insuranceapi:app"]
