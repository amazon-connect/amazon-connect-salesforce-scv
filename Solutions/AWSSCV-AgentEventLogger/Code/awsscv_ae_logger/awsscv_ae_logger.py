import os
import json
import boto3
import logging
import base64

format = os.getenv('format', 'true')

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    for record in event['Records']:
        payload = json.loads(base64.b64decode(record['kinesis']['data']))

        if (payload['EventType'] != 'HEART_BEAT'):
            log_to_console(payload)

def log_to_console(record):
    logger.info(json.dumps(record, skipkeys = True, indent = 2) if format == 'true' else json.dumps(record))
