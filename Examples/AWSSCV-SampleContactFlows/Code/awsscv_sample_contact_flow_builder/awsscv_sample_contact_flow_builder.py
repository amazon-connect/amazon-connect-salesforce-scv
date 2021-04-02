import sys
from pip._internal import main

main(['install', 'requests', '--target', '/tmp/'])
sys.path.insert(0, '/tmp/')

import os, json, logging, boto3, requests, urllib3
from awsscv.cfb import ContactFlowBuilder

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

http = urllib3.PoolManager()

def lambda_handler(event, context):
    logger.debug(event)

    task_root = os.environ['LAMBDA_TASK_ROOT']

    cfb = ContactFlowBuilder()

    config_source = open(task_root + '/config.json').read()
    config_content = json.loads(config_source)

    try:
        for (k, v) in config_content.items():
            file_source = open(task_root + '/' + v['Source']).read()
            flow_content = json.loads(file_source)['ContactFlow']['Content']

            sub_map = v['SubMap']

            sub_map['%%CONNECT_BASIC_QUEUE_ARN%%'] = os.getenv('connect_basic_queue_arn')
            sub_map['%%INVOKE_TELEPHONY_FUNCTION_ARM%%'] = os.getenv('invoke_telephony_function_arn')

            result = cfb.create_contact_flow(
                os.getenv('connect_instance_id'),
                v['Name'],
                v['Type'],
                v['Description'],
                flow_content,
                sub_map
            )

            cf_send(event, context, 'SUCCESS', {})
            return result;

    except Exception as e:
        logger.error(e)
        cf_send(event, context, 'FAILED', {})
        raise e


def cf_send(event, context, status, data, physical_resource_id=None, no_echo=False):
    response_url = event['ResponseURL']

    logger.debug(response_url)

    response = {
        'Status': status,
        'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': physical_resource_id or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'NoEcho': no_echo,
        'Data': data
    }

    json_response = json.dumps(response)

    logger.debug("Response body:\n{}".format(json_response))

    headers = {
        'content-type': '',
        'content-length': str(len(json_response))
    }

    try:

        response = http.request('PUT', response_url, body=json_response.encode('utf-8'), headers=headers)
        logger.debug("Status code: {0}".format(response.reason))

    except Exception as e:
        logger.error(e)
        logger.debug("send(..) failed executing requests.put(..): {}".format(str(e)))
