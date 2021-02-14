#!/bin/bash

trap ctrl_c INT

function ctrl_c() {
        echo "... caught interrupt signal (Ctrl+C), initiating shutdown"
        echo "... removing temp dynamodb files from local filesystem..."
        rm -rf dynamodb_local shared-local-instance.db
        echo "Cleanup complete! Good bye ..."
        exit
}

if [ -d "dynamodb_local" ]
then
    echo "Directory 'dynamodb_local' already exists, carry on!"
else
    echo "Fetching dynamodb JAR to run locally..."
    mkdir dynamodb_local
    wget https://s3.eu-central-1.amazonaws.com/dynamodb-local-frankfurt/dynamodb_local_latest.tar.gz -P dynamodb_local
    tar -xf dynamodb_local/dynamodb_local_latest.tar.gz -C dynamodb_local
    rm -rf dynamodb_local/dynamodb_local_latest.tar.gz
fi

echo "Running DynamoDB Locally via localhost:8000"
java -Djava.library.path=dynamodb_local/DynamoDBLocal_lib -jar dynamodb_local/DynamoDBLocal.jar -sharedDb