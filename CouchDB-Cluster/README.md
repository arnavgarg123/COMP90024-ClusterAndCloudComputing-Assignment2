# Docker-compose file to create couchdb containers on different instances
- To run on cloud use ansible script directly
- If trying to run this locally ensure that you have ***docker*** and ***docker-compose*** installed
- To spawn a couchdb instance locally run -> ```docker-compose up```
- To change the admin username and password of couchdb edit the fields
  - ```COUCHDB_USER```
  - ```COUCHDB_PASSWORD```
- For a more detailed understanding about the various couchdb parameters that can be controlled via docker-compose, check out the official documentation on [docker hub](https://hub.docker.com/_/couchdb)
