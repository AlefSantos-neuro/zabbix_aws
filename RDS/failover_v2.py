#!/usr/bin/python
#import datetime
#import sys
import boto3
import json
from json import dumps
#from httplib2 import Http
#from optparse import OptionParser

client = boto3.client('rds',
                        aws_access_key_id='*********************', 
                        aws_secret_access_key='*********************',
                        region_name='us-east-1')


response = client.describe_events(
    Duration=5,
    SourceIdentifier='DNS DO RDS',
    SourceType='db-cluster',
)

for i in response['Events']:
    if 'failover' in i ['Message']:
        status = {
            "status": 1
    }
else:
    status = {
        "status": 0
    }
    print(json.dumps(status))
