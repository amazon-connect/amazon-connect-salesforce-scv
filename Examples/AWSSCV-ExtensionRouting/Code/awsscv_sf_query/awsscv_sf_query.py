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
from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    logger.debug(event)

    # Establish an empty response
    response = {}
    # Set the default result to success
    response.update({'result':'success'})

    # Handle EventBridge pings that keep the function warm
    if 'source' in event:
        response.update({'statusCode': 200,'response' : 'warm', 'event' : 'EventBridge ping'})
        return response

    # Extract passed params and build query
    try:
        sf_sso_object = event['Details']['Parameters']['sf_sso_object']
        sf_extension = event['Details']['Parameters']['sf_extension']
        sf_query = "SELECT Id, " + sf_sso_object + " FROM User WHERE IsActive = TRUE AND Extension ='" + sf_extension + "'"

        # Login to Salesforce
        try:
            sf = Salesforce()

            # Do the Query
            try:
                query_result = sf.query(query=sf_query)

                # Prep the response
                response.update({'Username' : query_result[0][sf_sso_object]})

            except Exception as e:
                logger.error(e)
                response.update({'result':'fail', 'code' : 'SF Query Fail'})

        except Exception as e:
            logger.error(e)
            response.update({'result':'fail', 'code' : 'SF Login Fail'})

    except Exception as e:
        logger.error(e)
        response.update({'result':'fail', 'code' : 'Query failed to build'})

    return response
