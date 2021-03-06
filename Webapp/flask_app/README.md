# Webapp
Webapp for visualisation of data. Contains Maps, Graphs.

## Setup
- Make sure you have python-3 installed on your system
- Install Docker-engine on your system.<br/> For Ubuntu run command <br/>```apt install docker.io```
- You will need internet access to pull a base image from docher hub
- To run locally, comment out proxy environment variables from dockerfile.
- To run locally change the ip in ip.txt file to couchdb's ip.

## Execution
- To run without Docker
  - Run ```pip install -r requirements.txt``` to install dependencies.
  - Run ```gunicorn -w 3 -b :5000 -t 360 --reload wsgi:app``` for development from inside this directory.
  - Run ```gunicorn -w 3 -b :5000 -t 360 wsgi:app``` for deployment from inside this directory.
- To run via docker
  - Run ```docker build -t webapp:1.0``` to build docker image.
  - Run ```docker run -p 5000:5000 webapp:1.0``` to run in container.
