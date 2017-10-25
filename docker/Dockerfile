FROM python:3.6.3-slim-stretch

# Create app directory
ADD . /webapp
WORKDIR /webapp

# Install required OS dependencies.
RUN apt-get update
RUN apt-get install -y libssl-dev libcurl4-openssl-dev gcc

# Install app and testing requirements.
RUN pip install -r requirements.txt

# Install app package.
RUN pip install .

# Set the default directory for our environment
ENV HOME /webapp

# Set environment variable used by "flask run" command.
ENV FLASK_APP myob_ops_technical_test

# Expose port 5000 
EXPOSE 5000
 
ENTRYPOINT ["flask", "run", "-h", "0.0.0.0" ]
