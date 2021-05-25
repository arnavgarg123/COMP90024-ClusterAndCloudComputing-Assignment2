# Webapp

Webapp for visualisation of data. Contains Maps, Graphs. <br/>Gunicorn layer used as wsgi layer and for load balancing <br/>Nginx container used as webserver and also as load balancer.

## Running on localhost
- System uses an ip.txt file to read in the ip of master couch db instance.
- Create an ip.txt file with appropriate ip inside flask_app directory.
- Comment out proxy environment variables from dockerfile of nginx and flask_app.

## Setup
- Make sure you have python-3 installed on your system
Install Docker-engine and Docker-compose on your system.<br/> For Ubuntu run command <br/>```apt install docker.io```<br/>```apt install docker-compose```
- You will need internet access to pull a base image from docher hub

## Execution
- Run ```docker-compose up``` from inside this directory.
