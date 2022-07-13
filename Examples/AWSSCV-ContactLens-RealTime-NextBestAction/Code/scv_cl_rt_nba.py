# Version: 2022.06.06
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
# This lambda function is invoked when Contact Lens real-time rule triggers mapped EventBridge event.
# It inserts Contact Lens matched category in corresponding field, Current_Call_Category in Voice Call Object of Salesforce.


import json
import boto3
import os
import logging


lambda_client = boto3.client('lambda')
connect_client = boto3.client('connect')

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(
    os.getenv('lambda_logging_level', 'INFO')))


def lambda_handler(event, context):

    logger.debug(event)
    logger.info("nba lambda invoked")

    # Setting up data to insert Contact Lens category into corresponding field, Current_Call_Category (__c will be automatically added by Salesforce)in Salesforce Voice Call Object.

    try:
        Current_Call_Category__c = event['detail']['actionName']
        contactARN = event['detail']['contactArn']
        instaceARN = event['detail']['instanceArn']
        contactId = contactARN.partition('/contact/')[2]
        instanceId = instaceARN.partition('/')[2]
        logger.debug(contactARN)
        logger.debug(contactId)
        logger.debug(instanceId)
        logger.debug(Current_Call_Category__c)
        logger.info("call category extracted from Contact Lens paylaod")

    except Exception as e:
        logger.debug("Failed to extract information from Contact Lens payload")
        logger.error(e)
        return 'failed'

    try:
        response = connect_client.get_contact_attributes(
            InstanceId=instanceId,
            InitialContactId=contactId
        )
        logger.debug(response)
        logger.info("Contact attributes recevied")

    except Exception as e:
        logger.debug("Failed to get contact attributes from Connect Contact")
        logger.error(e)
        return 'failed'

    try:
        voiceCallId = response['Attributes']['voiceCallId']
        logger.debug(voiceCallId)
        payload = {
            "Details": {
                "Parameters": {
                    "methodName": "updateRecord",
                    "objectApiName": "VoiceCall",
                    "recordId": voiceCallId,
                    "Current_Call_Category__c": Current_Call_Category__c
                }
            }
        }

        # This lambda function uses "updateRecord" method of InvokeSalesforceRestApiFunction lambda function which comes out-of-the-box with Service Cloud Voice
        response = lambda_client.invoke(
            FunctionName=os.environ['InvokeSalesforceRestApiFunctionARN'], InvocationType='RequestResponse', Payload=json.dumps(payload))
        logger.debug(response)
        logger.info("Successfully send request to update Voice Call Object")
        return 'success'

    except Exception as e:
        logger.debug("Failed to call Rest API Function")
        logger.error(e)
        return 'failed'
