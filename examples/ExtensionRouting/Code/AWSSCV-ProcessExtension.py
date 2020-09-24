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

import json
import os

def lambda_handler(event, context):
    # Uncomment the following line for debugging
    # print(event)

    # Establsih an empty response
    response = {}
    # Set the default result to success
    response.update({'result':'success'})

    # Handle EventBridge pings that keep the function warm
    if 'source' in event:
        response.update({'statusCode': 200,'response' : 'warm', 'event' : 'EventBridge ping'})
        return response

    # Extract the Org ID from environment variables
    try:
        org_id = os.environ['sf_org_id']

    except:
        response.update({'result':'fail'})
        response.update({'fail_message':'Invalid Lambda config - missing Salesforce org ID'})
        return response

    # Extract the passed Id attribute, if present
    try:
        Id = event['Details']['Parameters']['Id']

        # If the key exists, extract the value and build the agent id
        if Id != '':
            clean_id = Id[:- 3]
            agent_id = clean_id + '@' + org_id
            response.update({'agent_id':agent_id})

        else:
            response.update({'result':'fail'})
            response.update({'fail_message':'Id value empty'})

    except:
        response.update({'result':'fail'})
        response.update({'fail_message':'Id key not passed'})

    return response
