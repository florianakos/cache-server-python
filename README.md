# cache-server-python

A service written in Python using Flask that uses AWS DynamoDB as DB backend to cache API responses from VirusTotal ...

For easy development and testing on local machine, there is a local copy of DynamoDB set up, see the [instructions here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html).

To set up authorization to VirusTotal API, there is a `.env` file which loads the key into the container using **VT_API_KEY** env variable. 

Before the local copy of DynamoDB can be used, be sure to run the script `bin/setup_dynamodb_tables.sh` which creates the tables and sets their TTL.