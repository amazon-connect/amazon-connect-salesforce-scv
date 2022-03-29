# Version: 2022.03.23
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
connect_client = boto3.client('connect')

def lambda_handler(event, context):

    print(event)
    logger.debug(event)

    # Create response container
    response = {'result':'success'}

    # Create the association data container
    association = {}

    # Deal with deletes
    if event['RequestType'] == 'Delete':
        try:
            lambda_function = event['ResourceProperties']['lambda_arn']
            instance_id = event['ResourceProperties']['instance_id']
            disassociate_function(lambda_function, instance_id)
            cf_send(event, context, 'SUCCESS', {})
            response.update({'event':'CF Delete'})
            return response

        except Exception as e:
            logger.error(e)
            cf_send(event, context, 'FAILED', {})
            response.update({'template_setup':'failed'})
            response.update({'result':'fail'})
            return response

    # Setup the association data
    try:
        # Grab data from CF Template
        association.update({'lambda_arn':event['ResourceProperties']['lambda_arn']})
        association.update({'instance_id':event['ResourceProperties']['instance_id']})


    except Exception as e:
        logger.error(e)
        logger.debug('failed to extract parameters')
        cf_send(event, context, 'FAILED', {})
        response.update({'template_setup':'failed'})
        response.update({'result':'fail'})
        return response

    # Process the CloudFormation Request
    try:
        add_association(association)
        cf_send(event, context, 'SUCCESS', {})
        response.update({'lambda_association':'complete'})

    except Exception as e:
        logger.error(e)
        logger.debug('failed to associate function')
        cf_send(event, context, 'FAILED', {})
        response.update({'lambda_association':'failed'})
        response.update({'result':'fail'})
        return response

    return response

def add_association(association):
    response = connect_client.associate_lambda_function(
        InstanceId= association['instance_id'],
        FunctionArn = association['lambda_arn']
    )

def disassociate_function(lambda_function,instance_id):
    response = connect_client.disassociate_lambda_function(
        InstanceId= instance_id,
        FunctionArn = lambda_function
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
