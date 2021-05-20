# COMP90024-ClusterAndCloudComputing-Assignment2

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
- GeoJson

## Architecture
- System is made up of multi-layer architecture where each layer has certain responsibilities: 
  - Data Gathering 
  - Data Storage 
  - Data Analytics 
  - Data Visualization
- Deployed on a total of four computing instances
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
  - Scenario 3 ()
    - 
