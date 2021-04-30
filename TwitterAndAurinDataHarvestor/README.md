# Twitter Data Harvestor

This is a basic Twitter data harvestor. Data is querried using twitter's api. 

## Pre-Setup
- You will have to get tiwtter developer account. It can be created using this [link](https://developer.twitter.com/)
- Get your OAuth 1.0a Api_Key, Api_Secret_Key, Access_Token, Access_Secret_Token
- Make sure you have python-3 installed on your system
- Install Docker-engine and Docker-compose on your system.<br/> For Ubuntu run command <br/>```apt install docker.io```<br/>```apt install docker-compose```
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
- Run ```docker-compose up``` from inside this directory.
