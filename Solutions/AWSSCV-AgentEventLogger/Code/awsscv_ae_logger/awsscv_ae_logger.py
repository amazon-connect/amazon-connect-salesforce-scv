import os, json, boto3, logging, base64

detailed_logging = os.getenv('detailed_logging', 'false')
format = os.getenv('format', 'true')

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    for record in event['Records']:
        payload = json.loads(base64.b64decode(record['kinesis']['data']))
        event_type = payload['EventType']

        try:
            previousAgentStatusARN = payload['PreviousAgentSnapshot']['AgentStatus']['ARN']
        except Error as e:
            previousAgentStatusARN = '0'

        try:
            currentAgentStatusARN = payload['CurrentAgentSnapshot']['AgentStatus']['ARN']
        except Error as e:
            currentAgentStatusARNM = '1'

        if (detailed_logging == 'true'):
            log_to_console(payload)
        else:
            if ((event_type == 'STATE_CHANGE' and currentAgentStatusARN != previousAgentStatusARN) or (event_type == 'LOGIN' or event_type == 'LOGOUT')):
                log_to_console(payload)

def log_to_console(record):
    logger.info(json.dumps(record, skipkeys = True, indent = 2) if format == 'true' else json.dumps(record))
