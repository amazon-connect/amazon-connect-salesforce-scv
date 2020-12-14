import os
import json
import boto3
import logging
import base64

write_to = os.getenv('writeTo', 'console')
s3_bucket = os.getenv('s3Bucket')
format = os.getenv('format', 'true')

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
     for record in event['Records']:
        payload = json.loads(base64.b64decode(record['kinesis']['data']))

        if (write_to == 'console' or write_to == 'both'):
            log_to_console(payload)

        if (write_to == 's3' or write_to == 'both'):
            log_to_s3(payload)

def log_to_console(record):
    logger.info(json.dumps(record, skipkeys = True, indent = 2) if format == 'true' else json.dumps(record))

def log_to_s3(record):
    s3_client = boto3.client('s3')
    contactId = record['ContactId']
    s3_client.put_object(Body=json.dumps(record, skipkeys = True, indent = 2), Bucket=s3_bucket, Key=contactId + '.json')