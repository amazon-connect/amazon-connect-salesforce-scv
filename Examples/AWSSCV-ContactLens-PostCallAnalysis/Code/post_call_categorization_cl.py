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


# This lambda function extracts information such as matched call categories and overall (agent & customer) sentiment, post call from Connect Contact Lens.
# It also inserts the information in corresponding fields in Voice Call Object of Salesforce.
# User can easily extend this lambda function to extract and insert more information generate by Contact Lens such as call transcript, conversation characteristics etc.


import json
import boto3
import random
import os
import logging


s3 = boto3.resource('s3')
lambda_client = boto3.client('lambda')

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(
    os.getenv('lambda_logging_level', 'INFO')))


def lambda_handler(event, context):

    # This lambda function will be triggered once the Contact Lens post call analysis in available in the associated S3 bucket

    logger.debug(event)
    logger.info(event["Records"][0]["s3"]["bucket"]["name"])
    logger.info(event["Records"][0]["s3"]["object"]["key"])

    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        key = key.replace('%3A', ':')

        obj = s3.Object(bucket, key)
        clObject = json.loads(obj.get()['Body'].read().decode('utf-8'))
        logger.debug(clObject)

    except Exception as e:
        print('Failed to access contact lens s3 bucket: ', e)
        logger.error(e)
        logger.debug('Failed to access contact lens s3 bucket')
        return response['Failed to access contact lens s3 bucket']

    try:
        ContactId = clObject['CustomerMetadata']['ContactId']
        InstanceId = clObject['CustomerMetadata']['InstanceId']
        logger.info("Contact ID: " + clObject['CustomerMetadata']['ContactId'])
        logger.info(clObject['CustomerMetadata']['InstanceId'])

    # Extracting information from Contact Lens post call analysis

        Overall_Agent_Sentiment = clObject['ConversationCharacteristics']['Sentiment']['OverallSentiment']['AGENT']
        Overall_Customer_Sentiment = clObject['ConversationCharacteristics']['Sentiment']['OverallSentiment']['CUSTOMER']

        Categories = ""
        for x in range(len(clObject['Categories']['MatchedCategories'])):
            Categories = Categories + \
                clObject['Categories']['MatchedCategories'][x] + ","
        Categories = Categories[:len(Categories)-1]

    # Setting up data to insert into corresponding fields in Salesforce Voice Call Object.
    # Please ensure you have Salesforce Voice Call Object created before invoking this lambda function
    # In this example - Call_Categories, Overall_Customer, Overall_Agent_Sentiment (__c will be automatically added by Salesforce)

        cldata = {}
        cldata['Call_Categories__c'] = Categories
        cldata['Overall_Customer_Sentiment__c'] = Overall_Customer_Sentiment
        cldata['Overall_Agent_Sentiment__c'] = Overall_Agent_Sentiment
        logger.info(Categories)
        logger.info(Overall_Customer_Sentiment)
        logger.info(Overall_Agent_Sentiment)

    except Exception as e:
        print('Failed to extract inforamtion from contact lens json object: ', e)
        logger.error(e)
        logger.debug(
            'Failed to extract inforamtion from contact lens json object')
        return response['Failed to extract inforamtion from contact lens json object']

    try:
        fields = {
            "callAttributes": json.dumps(cldata)
        }
        payload = {
            "Details": {
                "Parameters": {
                    "methodName": "updateVoiceCall",
                    "fieldValues": fields,
                    "contactId": ContactId
                }
            }
        }

    # This lambda function uses "updateVoiceCall" method of TelephonyIntegrationApiFunction lambda function which comes out-of-the-box with Service Cloud Voice

        response = lambda_client.invoke(
            FunctionName=os.environ['ARN_InvokeTelephonyIntegrationApiFunction'], InvocationType='RequestResponse', Payload=json.dumps(payload))
        logger.info(json.loads(response["Payload"].read())['status'])
        return response["StatusCode"]

    except Exception as e:
        print('Failed to invoke TelephonyIntegrationApiFunction: ', e)
        logger.error(e)
        logger.debug('Failed to invoke TelephonyIntegrationApiFunction')
        return response['Failed to invoke TelephonyIntegrationApiFunction']
