# Assignment 2 - COMP90024 Course at The University of Melbourne
#
# Cluster and Cloud Computing - Team 48
#
# Authors:
#
#  * Arnav Garg (Student ID: 1248298)
#  * Piyush Bhandula (Student ID: 1163716)
#  * Jay Dave (Student ID: 1175625)
#  * Vishnu Priya G (Student ID: 1230719)
#  * Gurkirat Singh Chohan 1226595
#
# Location: India, Melbourne, Singapore
#
FROM python
#ENV HTTP_PROXY http://wwwproxy.unimelb.edu.au:8000/
#ENV HTTPS_PROXY http://wwwproxy.unimelb.edu.au:8000/
#ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
#ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/
#ENV no_proxy localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.o>
RUN mkdir Harvestor
COPY . ./Harvestor/
RUN pip install -r ./Harvestor/requirements.txt
WORKDIR ./Harvestor/
CMD python app.py Twitter.txt
