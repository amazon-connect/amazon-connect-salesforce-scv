# Version: 2022.02.20
"""
**********************************************************************************************************************
 *  Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved                                            *
 *                                                                                                                    *
 *  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated      *
 *  documentation files (the "Software"), to deal in the Software without restriction, including without limitation   *
 *  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and  *
 *  to permit persons to whom the Software is furnished to do so.                                                     *
 *                                                                                                                    *
 *  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO  *
 *  THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
 *  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF         *
 *  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS *
 *  IN THE SOFTWARE.                                                                                                  *
 **********************************************************************************************************************
"""
import sys
from pip._internal import main

main(['install', 'requests', '--target', '/tmp/'])
sys.path.insert(0,'/tmp/')


import json
import boto3
import os
import logging
import requests
import urllib3
http = urllib3.PoolManager()


logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'DEBUG')))

SUCCESS = "SUCCESS"
FAILED = "FAILED"

print('Loading function')
s3_client = boto3.resource('s3')

def lambda_handler(event, context):

    logger.debug(event)

    # Create response container
    response = {'result':'success'}

    # Create the notification data container
    notification = {}

    # Deal with deletes
    if event['RequestType'] == 'Delete':
        try:
            bucket_name = event['ResourceProperties']['bucket_name']
            delete_notification(bucket_name)
            cf_send(event, context, 'SUCCESS', {})
            response.update({'event':'CF Delete'})
            return response


        except:
            raise Exception
            cf_send(event, context, 'FAILED', {})

    # Setup the notification data
    try:
        # Grab ARNs from CF Template
        notification.update({'bucket_name':event['ResourceProperties']['bucket_name']})
        notification.update({'lambda_arn':event['ResourceProperties']['lambda_arn']})
        notification.update({'object_suffix':event['ResourceProperties']['object_suffix']})

    except Exception as e:
        logger.error(e)
        logger.debug('failed to extract parameters')
        cf_send(event, context, 'FAILED', {})
        response.update({'template_setup':'failed'})
        response.update({'result':'fail'})
        return response

    # Process the CloudFormation Request
    try:
        add_notification(notification)
        cf_send(event, context, 'SUCCESS', {})
        response.update({'notification_build':'complete'})

    except Exception as e:
        logger.error(e)
        logger.debug('failed to create contact flow')
        cf_send(event, context, 'FAILED', {})
        response.update({'flow_build':'failed'})
        response.update({'result':'fail'})
        return response

    return response

def add_notification(notification):
    bucket_notification = s3_client.BucketNotification(notification['bucket_name'])
    response = bucket_notification.put(
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': notification['lambda_arn'],
                    'Events': [
                        's3:ObjectCreated:*'
                    ],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'suffix',
                                    'Value': notification['object_suffix']
                                },
                            ]
                        }
                    }
                }
            ]
        }
    )

def delete_notification(bucket_name):
    bucket_notification = s3_client.BucketNotification(bucket_name)
    response = bucket_notification.put(
        NotificationConfiguration={}
    )
    print("Delete request completed....")

def cf_send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    logger.debug(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    logger.debug("Response body:\n{}".format(json_responseBody))

    headers = {
        'content-type' : '',
        'content-length' : str(len(json_responseBody))
    }

    try:

        response = http.request('PUT',responseUrl,body=json_responseBody.encode('utf-8'),headers=headers)
        logger.debug("Status code: {0}".format(response.reason))

    except Exception as e:
        logger.error(e)
        logger.debug("send(..) failed executing requests.put(..): {}".format(str(e)))
