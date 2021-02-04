from awsscv.sf import Salesforce

def lambda_handler(event, context):
    response = {}

    # Handle EventBridge pings that keep the function warm
    if 'source' in event:
        response.update({'statusCode': 200,'response' : 'warm', 'event' : 'EventBridge ping'})
        return response
