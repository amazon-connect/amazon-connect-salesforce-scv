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

# Import the necessary moduels for this flow to work
import json
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

def lambda_handler(event, context):
    # Establish response container
    response = {}

    # Check for processing flag
    try:
        current_state = event['Details']['ContactData']['Attributes']['current_state']
    except:
        response.update({'result':'fail'})
        response.update({'result_reason':'missing state'})

    # Is this a first pass?
    if current_state == 'start':
        current_state = 'processing'
        response.update({'current_state':current_state})
        current_target_list = event['Details']['ContactData']['Attributes']['agent_targets'].split(',')
        remaining_targets = len(current_target_list)

    else:
        current_target_list = json.loads(event['Details']['ContactData']['Attributes']['remaining_target_list'])

    # Grab next target & update the response
    next_target = current_target_list.pop(0)
    response.update({'next_target':next_target})

    remaining_targets = len(current_target_list)

    # Format the list if there are more targets to process
    if remaining_targets != 0:
        remaining_target_list = json.dumps(current_target_list)
        response.update({'remaining_target_list':remaining_target_list})

    else:
        response.update({'current_state':'complete'})

    response.update({'remaining_targets':remaining_targets})

    logger.debug(next_target)
    logger.debug(remaining_targets)

    return response
