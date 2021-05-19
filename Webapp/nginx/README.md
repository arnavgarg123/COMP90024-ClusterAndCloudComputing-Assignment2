# Nginx webserver

Webserver container to serve our app to clients.<br/>
Load balancer of nginx is also used.

## config
- Default config file replaced with our file to serve our application.
- Flask app container is accessed using internal network created in docker compose in parent directory.

## Setup
- No need to run this seperatly. Just run the ```docker-compose``` file in parent directory.
