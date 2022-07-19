import boto3
from typing import TypeVar

dynamo = TypeVar("dynamo")

dynamodb = boto3.resource("dynamodb")

table: dynamo = dynamodb.Table("fax_db")
