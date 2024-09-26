FROM python:3.12.6-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Define environment variables from the .env file
COPY .env .env

# Load environment variables
RUN export $(cat .env | xargs)

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]