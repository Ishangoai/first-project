FROM python:latest

# Set the working directory for the app
# WORKDIR /

# Copy the app from the current folder to the working directory
COPY . .

# Install the required libraries and the module itself (necessary
# to be able to run the tests with pytes)
#RUN pip install -r ./requirements.txt
#RUN pip install -e .

# Run the App
