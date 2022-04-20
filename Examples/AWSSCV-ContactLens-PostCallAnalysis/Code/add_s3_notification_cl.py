# Version: 2022.04.19

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
import urllib3
import os
import logging
import boto3
import json
import sys
from pip._internal import main

main(['install', 'requests', '--target', '/tmp/'])
sys.path.insert(0, '/tmp/')


http = urllib3.PoolManager()

SUCCESS = "SUCCESS"
FAILED = "FAILED"

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(
    os.getenv('lambda_logging_level', 'DEBUG')))

print('Loading function')
s3 = boto3.resource('s3')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    responseData = {}
    # Create response container
    response = {'result': 'success'}
    try:
        if event['RequestType'] == 'Delete':
            print("Request Type:", event['RequestType'])
            Bucket = event['ResourceProperties']['Bucket']
            delete_notification(Bucket)
            print("Sending response to custom resource after Delete")
        elif event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
            print("Request Type:", event['RequestType'])
            LambdaArn = event['ResourceProperties']['LambdaArn']
            Bucket = event['ResourceProperties']['Bucket']
            add_notification(LambdaArn, Bucket)
            responseData = {'Bucket': Bucket}
            print("Sending response to custom resource")
        responseStatus = 'SUCCESS'
    except Exception as e:
        print('Failed to process:', e)
        responseStatus = 'FAILED'
        responseData = {'Failure': 'error occured'}
    cf_send(event, context, responseStatus, {})


def add_notification(LambdaArn, Bucket):
    bucket_notification = s3.BucketNotification(Bucket)
    response = bucket_notification.put(
        NotificationConfiguration={
            'LambdaFunctionConfigurations': [
                {
                    'LambdaFunctionArn': LambdaArn,
                    'Events': [
                        's3:ObjectCreated:Put'
                    ],
                    'Filter': {
                        'Key': {
                            'FilterRules': [
                                {
                                    'Name': 'prefix',
                                    'Value': 'Analysis/Voice'
                                },
                                {
                                    'Name': 'suffix',
                                    'Value': '.json'
                                }
                            ]
                        }
                    }
                },
            ]
        }
    )
    print("Put request completed....")


def delete_notification(Bucket):
    bucket_notification = s3.BucketNotification(Bucket)
    response = bucket_notification.put(
        NotificationConfiguration={}
    )
    print("Delete request completed....")


def cf_send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']

    logger.debug(responseUrl)

    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: ' + \
        context.log_stream_name
    responseBody['PhysicalResourceId'] = physicalResourceId or context.log_stream_name
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['NoEcho'] = noEcho
    responseBody['Data'] = responseData

    json_responseBody = json.dumps(responseBody)

    logger.debug("Response body:\n{}".format(json_responseBody))

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:

        response = http.request(
            'PUT', responseUrl, body=json_responseBody.encode('utf-8'), headers=headers)
        logger.debug("Status code: {0}".format(response.reason))

    except Exception as e:
        logger.error(e)
        logger.debug(
            "send(..) failed executing requests.put(..): {}".format(str(e)))
