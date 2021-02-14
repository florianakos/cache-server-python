#!/bin/bash
set -ex

echo "Setting up Tables and their schema in local DynamoDB instance"

export AWS_ACCESS_KEY_ID=dummyKey
export AWS_SECRET_ACCESS_KEY=dummyKey

AWS="aws --endpoint-url http://localhost:8000"
ATTRIBUTE_DEF="AttributeName=query_value,AttributeType=S"
KEY_SCHEMA_DEF="AttributeName=query_value,KeyType=HASH"
THROUGHPUT_DEF="ReadCapacityUnits=5,WriteCapacityUnits=5"

TABLE_NAMES=(VTCacheIPAddresses VTCacheDomains VTCacheFiles VTCacheURLs)
for table_name in "${TABLE_NAMES[@]}"; do
  $AWS dynamodb create-table --table-name "${table_name}" --attribute-definitions "${ATTRIBUTE_DEF}" --key-schema "${KEY_SCHEMA_DEF}" --provisioned-throughput "${THROUGHPUT_DEF}"
  $AWS dynamodb update-time-to-live --table-name "${table_name}" --time-to-live-specification "Enabled=true, AttributeName=ttl"
done