# Agent Event Logger
This example shows how you can capture agent events from a Kinesis stream and process those events to store agent event data in S3 or log CTR data to CloudWatch.

## Deployment Resources
To enable agent event logging, we need to deploy one AWS Lambda function.

### AWS Lambda Function
For these deployments, the following AWS Lambda function is provided:
- awsscv_ae_logger_%InstanceName% (awsscv-ae-logger.py): Provides ability to receive agent events from Kinesis, store those events in S3, and/or log those events to CloudWatch.

## Prerequisites for all deployments
1. [AWSSCV Common Layers](../../Common/AWSSCV-CommonLayers) deployed
2. [AWSSCV Salesforce Config](../../Common/AWSSCV-SalesforceConfig) deployed
3. Access to the [AWS Console](https://console.aws.amazon.com/console/home)

## Deplyoment instructions
### Deploy the CloudFormation template
1. Right-click/control-click to download the [AWSSCV AgentEventLogger template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Solutions/AWSSCV-AgentEventLogger/CloudFormation/awsscv_ae_logger.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3.	Make sure you are in the **same region** as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the **CloudFormation console**
5.	Select **Create Stack**, and choose **With new resources (standard)**
6.	In the Specify Template section, choose **Upload a template file**
7.	Select **Choose file**
8.	Navigate to the folder where you saved **awsscv_ae_logger.yaml**
9.	Select **Next**
10.	In the Stack Name field, enter `AWSSCV-AgentEventLogger`
11.	**Enter the parameters** as follows (most from your notepad):
- AWSRegion: Select the region that you have deployed Amazon Connect in
- AWSSCVCommonRole: ARN of the awsscv_common_role role
- ConnectInstanceName: Provide the instance name for Amazon Connect.
- AgentEventKinesisStream: ARN of the agent event Kinesis stream
- DetailedLogging: Log all agent events (true) rather than just state changes.
- Format: Pretty print the agent event output (true)
- LambdaLoggingLevel: INFO or DEBUG
12.	Select **Next**
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select **Next**
15.	Scroll to the bottom, make sure to check the acknowledgement that AWS CloudFormation might create IAM resource, and select **Create Stack**
16.	After a minute or two, the stack should complete.
