FROM nginx:latest

# Set the working directory for the app


# Copy the app from the current folder to the working directory
COPY . /usr/share/nginx/html

# Install the required libraries and the module itself (necessary
# to be able to run the tests with pytes)

# Run the App
