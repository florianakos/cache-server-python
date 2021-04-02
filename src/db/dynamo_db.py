from decimal import Decimal
import boto3
import json
import os
from botocore.config import Config

AWS_CONF = Config(region_name='eu-west-1', retries={'max_attempts': 3, 'mode': 'standard'})


class DynamoDB:

    def __init__(self):
        if self._in_docker_compose():
            self.dynamodb = boto3.resource('dynamodb', endpoint_url=self._localstack_endpoint(), config=AWS_CONF)
        else:
            self.dynamodb = boto3.resource('dynamodb')

    def save(self, table_name, data):
        parsed = json.loads(json.dumps(data), parse_float=Decimal)
        self.dynamodb.Table(table_name).put_item(Item=parsed)

    def load(self, table_name, query_value):
        return self.dynamodb.Table(table_name).get_item(Key={"query_value": query_value})

    @staticmethod
    def _in_docker_compose() -> bool:
        if os.getenv("DOCKER_COMPOSE") and os.getenv("DOCKER_COMPOSE") == "true":
            return True
        return False

    @staticmethod
    def _localstack_endpoint() -> str:
        return f"http://{os.getenv('DYNAMODB_HOST')}:{os.getenv('DYNAMODB_PORT')}"
