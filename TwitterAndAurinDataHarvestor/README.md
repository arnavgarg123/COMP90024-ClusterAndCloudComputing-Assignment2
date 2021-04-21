# Twitter Data Harvestor

This is a basic Twitter data harvestor. Data is querried using twitter's api. 

## Pre-Setup
- You will have to get tiwtter developer account. It can be created using this [link](https://developer.twitter.com/)
- Get your OAuth 1.0a Api_Key, Api_Secret_Key, Access_Token, Access_Secret_Token
- Make sure you have python-3 installed on your system
- Install Docker-engine on your system. For Ubuntu run command ```apt install docker.io```
- You will need internet access to pull a base image from docher hub

## Setup
- Paste your Api_Key, Api_Secret_Key, Access_Token, Access_Secret_Token to the Twitter.txt file <br />
Example -<br />
  ```
  Api_Key: xrfctgyuhnjkm
  Api_Secret_Key: gfhcgvjbhnkj
  Access_Token: cfvghnmkiuyhgb
  Access_Secret_Token: cfghbhjnbhjkadcefc
  ```
## Execution
- Run ```docker build -t twitter-harvestor:1.0 .``` form inside this directory.
- Now that you have the container built. You can simply run ```docker run twitter-harvestor:1.0``` to run the python script.
