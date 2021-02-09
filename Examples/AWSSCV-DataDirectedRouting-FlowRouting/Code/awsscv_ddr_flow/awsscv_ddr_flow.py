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

# Import the necessary modules for this flow to work
import logging
import os
import json
from awsscv.sf import Salesforce

logger = logging.getLogger()
logger.setLevel(logging.getLevelName(os.getenv('lambda_logging_level', 'INFO')))

# Core function
def lambda_handler(event, context):
    # REMEMBER to comment out the line below in production to reduce PII issues
    logger.debug(event)

    # Create an empty response container
    response = {}

    # Handle EventBridge pings that keep the function warm
    if 'source' in event:
        response.update({'statusCode': 200,'response' : 'warm', 'event' : 'EventBridge ping'})
        return response

    # Extract pushed parameters from the contact flow
    try:
        parameters = dict(event['Details']['Parameters'])

    except:
        response.update({'status':'fail', 'code' : 'Parameters missing'})
        return response

    # Initialize the Salesforce Connection
    if 'sf_flow' in parameters:
        sf = Salesforce()

    else:
        response.update({'status':'fail', 'code' : 'Flow parameter missing'})
        return response

    # Try to get a routing target from Salesforce
    try:
        get_target = execute_flow(sf=sf, **parameters)

    except:
        response.update({'status':'fail', 'code' : 'invoke flow fail'})
        return response

    # Extract the result and add it to the response
    logger.debug('respnse:' + json.dumps(get_target[0]))
    response.update(get_target[0]['outputValues'])
    logger.debug(response)

    # Check for a queue target and reformat if it exists:
    if response['has_queue'] == '1':
        reformatted_queue = format_queue_target(response['queue_target'])
        response.update({'queue_target' : event['Details']['ContactData']['InstanceARN'] + '/queue/' + reformatted_queue})

    # Check for agent targets and format if necessary
    if response['has_agents'] == '1':
        agent_targets = response['agent_targets']
        split_targets = agent_targets.split(',')
        formatted_agents = ''

        for agent in split_targets:
            agent = agent[:-3]
            formatted_agents = formatted_agents + agent + '@' + os.environ['sf_org_id'] + ','

        formatted_agents = formatted_agents.rstrip(',')
        response.update({'agent_targets': formatted_agents})

    # Clean up the response
    response.pop('output_response')
    response.pop('Flow__InterviewStatus')
    response.update({'status':'success'})

    return response

# Flow execution
def execute_flow(sf, sf_flow, **kwargs):

    # Create the data array

    inputs = {}
    for k, v in kwargs.items():
        inputs.update({k: v})
    data = [inputs]

    # Invoke the flow, passing the data
    return sf.call_flow(sflow=sf_flow, data=data)

def format_queue_target(queue):
    # Clean up the Queue ID, Split the prefix off, replace the underscores with hyphens
    reformatted_queue = queue.split(os.environ['queue_prefix'])
    reformatted_queue = reformatted_queue[1]
    reformatted_queue = reformatted_queue.replace('_','-')

    # Return the formatted Queue ID
    return reformatted_queue
