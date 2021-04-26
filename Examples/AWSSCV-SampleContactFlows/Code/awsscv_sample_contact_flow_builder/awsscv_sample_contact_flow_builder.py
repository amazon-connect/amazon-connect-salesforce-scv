import sys
from pip._internal import main

main(['install', 'boto3', '--target', '/tmp/'])
sys.path.insert(0, '/tmp/')

import os, json, logging, boto3, urllib3, cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

http = urllib3.PoolManager()


def lambda_handler(event, context):
    logger.debug(event)

    if event['RequestType'] == 'Delete':
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})

        return {
            'result': 'success',
            'event': 'Delete'
        }

    task_root = os.environ['LAMBDA_TASK_ROOT']

    config_source = open(task_root + '/config.json').read()
    config_content = json.loads(config_source)

    results = []

    try:
        for (k, v) in config_content.items():
            file_source = open(task_root + '/' + v['Source']).read()
            flow_content = json.loads(file_source)['ContactFlow']['Content']

            sub_map = v['SubMap']
            sub_map['%%CONNECT_BASIC_QUEUE_ARN%%'] = os.getenv('connect_basic_queue_arn')
            sub_map['%%INVOKE_TELEPHONY_FUNCTION_ARN%%'] = os.getenv('invoke_telephony_function_arn')
            sub_map['%%INVOKE_SALESFORCE_REST_API_FUNCTION_ARN%%'] = os.getenv('invoke_salesforce_rest_api_function_arn')
            sub_map['%%KVS_CONSUMER_TRIGGER_ARN%%'] = os.getenv('kvs_consumer_trigger_arn')

            result = create_contact_flow(
                os.getenv('connect_instance_id'),
                v['Name'],
                v['Type'],
                v['Description'],
                flow_content,
                sub_map
            )

            results.append(result)

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
        return results

    except Exception as e:
        logger.error(e)
        cfnresponse.send(event, context, cfnresponse.FAILED, {})


def create_contact_flow(connect_instance_id, name, type, description, content, sub_map):
    sub_content = content

    for key, value in sub_map.items():
        sub_content = sub_content.replace(key, value)

    result = boto3.client('connect').create_contact_flow(
        InstanceId=connect_instance_id,
        Name=name,
        Type=type.upper(),
        Description=description,
        Content=sub_content
    )

    return result
