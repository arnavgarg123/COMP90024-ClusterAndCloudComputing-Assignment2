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
RUN mkdir Harvestor
COPY . ./Harvestor/
RUN pip install -r ./Harvestor/requirements.txt
WORKDIR ./Harvestor/
CMD python app.py Twitter.txt
