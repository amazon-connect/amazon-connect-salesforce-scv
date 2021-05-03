import sys
from pip._internal import main

main(['install', 'boto3', '--target', '/tmp/'])
sys.path.insert(0, '/tmp/')

import os, json, logging, boto3, urllib3, calendar, time, cfnresponse

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))

http = urllib3.PoolManager()

sub_map = {}
contact_flow_map = {}
results = []

def lambda_handler(event, context):
    logger.debug(event)

    try:
        if event['RequestType'] == 'Delete':
            cfnresponse.send(event, context, cfnresponse.SUCCESS, {})

            return {
                'result': 'success',
                'event': 'Delete'
            }

        task_root = os.environ['LAMBDA_TASK_ROOT']

        sub_map['%%CONNECT_BASIC_QUEUE_ARN%%'] = os.getenv('connect_basic_queue_arn')
        sub_map['%%INVOKE_TELEPHONY_FUNCTION_ARN%%'] = os.getenv('invoke_telephony_function_arn')
        sub_map['%%INVOKE_SALESFORCE_REST_API_FUNCTION_ARN%%'] = os.getenv('invoke_salesforce_rest_api_function_arn')
        sub_map['%%KVS_CONSUMER_TRIGGER_ARN%%'] = os.getenv('kvs_consumer_trigger_arn')

        ts = calendar.timegm(time.gmtime())

        # Process AWS_Sample_SCV_Agent_Transfer
        with open(os.path.join(task_root, 'AWS_Sample_SCV_Agent_Transfer.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWSSCVAgentWhisper
        with open(os.path.join(task_root, 'AWSSCVAgentWhisper.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWSSCVAgentWhisperWithStreaming
        with open(os.path.join(task_root, 'AWSSCVAgentWhisperWithStreaming.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWS_Sample_SCV_Queue_Transfer
        with open(os.path.join(task_root, 'AWS_Sample_SCV_Queue_Transfer.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWS_Sample_SCV_REST_Example
        with open(os.path.join(task_root, 'AWS_Sample_SCV_REST_Example.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWS_Sample_SCV_Inbound
        with open(os.path.join(task_root, 'AWS_Sample_SCV_Inbound.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWS_Sample_SCV_Inbound_Flow_with_Transcription
        with open(os.path.join(task_root, 'AWS_Sample_SCV_Inbound_Flow_with_Transcription.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)

        # Process AWS_Sample_SCV_Outbound_Flow_with_Transcription
        with open(os.path.join(task_root, 'AWS_Sample_SCV_Outbound_Flow_with_Transcription.json')) as f:
            json_object = json.load(f)
            result = create_contact_flow(os.getenv('connect_instance_id'), json_object, ts)
        time.sleep(2)


        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})

        return contact_flow_map

    except Exception as e:
        logger.error(e)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, {})


def create_contact_flow(connect_instance_id, json_object, ts):
    name = json_object['ContactFlow']['Name']
    type = json_object['ContactFlow']['Type']
    description = json_object['ContactFlow']['Description']
    sub_content = json_object['ContactFlow']['Content']

    for key, value in sub_map.items():
        sub_content = sub_content.replace(key, value)

    try:
        result = boto3.client('connect').create_contact_flow(
            InstanceId=connect_instance_id,
            Name=name + '-' + str(ts),
            Type=type,
            Description=description,
            Content=sub_content
        )

        sub_map['%%' + name + '%%'] = result['ContactFlowArn']

        contact_flow_map[name] = { 'ContactFlowId': result['ContactFlowId'], 'ContactFlowArn': result['ContactFlowArn'] }

        return result

    except Exception as e:
        logger.error(e)
        logger.error(sub_content)
