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

import logging
import os
import json
from salesforce import Salesforce

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

    # Extract pushed parameters from the contact flow
    try:
        sf_query = event['Details']['Parameters']['sf_query']

        # Login to Salesforce
        try:
            sf = Salesforce()
            sf.sign_in()

            # Do the Query
            try:
                query_result = sf.query(query=sf_query)

                # Prep the response
                response.update({'Id' : query_result[0]['Id']})

            except:
                response.update({'result':'fail', 'code' : 'SF Query Fail'})

        except:
            response.update({'result':'fail', 'code' : 'SF Login Fail'})

    except:
        response.update({'result':'fail', 'code' : 'Parameters missing'})

    return response
