# COMP90024-ClusterAndCloudComputing-Assignment2
Analysed tweets from across Australia to study life in different cities.<br/>
Studied correlation between true data and extracted data from tweets in various scenarios.<br/>
Map view to get some general statistics on location enabled tweets.

## Motivation
Project was created to understand the corelation between Twitter and AURIN data. Twitter is a very rich source for raw data. We thought of processing this data to understand different aspects of life in Australian cities. We wanted to build a system which could compare some aspects of life between different cities. Hence, we created 3 scenarios and focused on which aspects of these can we extract from twitter and compare with AURIN data.

## Resources Used
- Melbourne Research Cloud
- AURIN
- Twitter

## Technologies Used
- Ansible
- Docker
- Couchdb
- Python Flask
- Tensorflow
- Neural network
- GeoJson

## Why Twitter???
Social media platform generates huge amount of data daily. When cleaned properly this data can be used to perform various type of analysis. Most social media platform also collect location data which can be used to track users. Most of the companies do not give access to this data to the public. However Twitter has a developer account which provides a subset of this data for free. As the freely data is only 1% of the total data it can not be effectively used to track users but still there are many interesting analysis that can be performed when this data is combined with some of the other freely available data.

## Architecture
- System is made up of multi-layer architecture where each layer has certain responsibilities: 
  - Data Gathering 
  - Data Storage 
  - Data Analytics 
  - Data Visualization
- Deployed on a total of four computing instances
  - Harvestor, couchdb and preprocessing
    - 3 instances
    - 2 vCPU, 9 GB RAM, 40+30 GB HDD
    - couchdb in cluster with 3 nodes
  - webapp 
    - 1 vCPU, 4.5 GB RAM, 30 GB HDD
- Diagram
![Architecture Diagram](https://github.com/arnavgarg123/COMP90024-ClusterAndCloudComputing-Assignment2/blob/main/Docs/Architecture.png)

## Data
- Twitter Harvestor
  - Tweets
  - Location
  - Date/Time
  - User ID
  - Tweet ID
- AURIN (Australian Urban Research Infrastructure Network)
  - City wise population data
  - City wise cost of living data
  - Unemployment data
- Collected from 19 cities

## Analysis
- Sentiment Analysis
  - NLP Model
    - Removed stop words and used word Tockenizer
    - Uses Multi dimentional (50) embedings
    - Bidirectional LSTM layer to make sense of each word in the sentence based on previous words
    - Convolution 1d layer
- Map
  - General Statistics
  - Location of tweets
  - Density of number of tweets from a locality
- Graphs
  - Scenario 1 (Life in different cities)
    - 
  - Scenario 2 (Covid-19)
    - 
  - Scenario 3 (Effects of unemployment on people)

## Deployment
### Setup
- Python-3 needs to be installed locally
- You need to have Ansible installed locally
- You will have to get your own Openstackrc file along with a openstack api password

### Steps for Deployment:
- Create your own key pair and  upload it to MRC.
- In the inventory.ini file, replace the value of “ansible_ssh_private_key_file” to the path of the key on your system.
- Also in var.yaml (found in the variable directory) replace the value of “instance_key_name” to the name that you gave your key.
- Clone Github directory. We need the AnsiblePlaybook directory locally.
  - ```git clone “https://github.com/arnavgarg123/COMP90024-ClusterAndCloudComputing-Assignment2.git”```
- Make sure you are connected to VPN if you are accessing MRC from outside the university.
- Now go into Ansible directory and run 
  - ```. ./unimelb-comp90024-2021-grp-48-openrc.sh; ansible-playbook -i inventory/inventory.ini mrc.yaml```
- Enter your password and wait for it to execute. (Takes around 15 min)

Once the system has been deployed you can access the webapp using the url of the webapp instance. 


## Future work
- Data from other social media sites can be gathered and used along with this data to increase precision of our analysis.
- Data from paid twitter account can be taken to understand the life of people in more detail.
- Data from paid twitter account can also be used to track them and create a blueprint of their daily movement pattern.
- More nodes can be added to enable scaling of the system and also to collect data from more cities.
- This system can be applied to analyse any country. (With enough resources possibly the entire earth)
