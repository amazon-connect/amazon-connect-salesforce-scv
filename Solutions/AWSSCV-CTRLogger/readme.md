# CTR Logger
This example shows how you can capture CTR events from a Kinesis stream and process those events to store CTR data in S3 or log CTR data to CloudWatch.

## Deployment Resources
To enable CTR logging, we need to deploy one AWS Lambda function.

### AWS Lambda Function
For these deployments, the following AWS Lambda function is provided:
- awsscv_ctr_logger_%InstanceName% (awsscv-ctr-logger.py): Provides ability to receive CTR events from Kinesis, store those events in S3, and/or log those events to CloudWatch.

## Prerequisites for all deployments
1. [AWSSCV Salesforce Config](amazon-connect-salesforce-scv/Common/AWSSCV-SalesforceConfig) deployed
2. Access to the [AWS Console](https://console.aws.amazon.com/console/home)

## Deplyoment instructions
### Deploy the CloudFormation template
1. Right-click/control-click to download the [AWSSCV CTRLogger template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Examples/AWSSCV-CTRLogger/CloudFormation/awsscv_ctr_logger.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3.	Make sure you are in the **same region** as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the **CloudFormation console**
5.	Select **Create Stack**, and choose **With new resources (standard)**
6.	In the Specify Template section, choose **Upload a template file**
7.	Select **Choose file**
8.	Navigate to the folder where you saved a**wsscv_follow_me_routing.yaml**
9.	Select **Next**
10.	In the Stack Name field, enter `AWSSCV-CTRLogger`
11.	**Enter the parameters** as follows (most from your notepad):
- AWSRegion: Select the region that you have deployed Amazon Connect in
- AWSSCVCommonRole: ARN of the awsscv_common_role role
- ConnectInstanceName: Provide the instance name for Amazon Connect.
- CTRKinesisStream: ARN of the CTR Kinesis stream
- Format: Pretty print (true) the CTR output
- LambdaLoggingLevel: INFO or DEBUG
- WriteTo: Where to send the CTR data (s3, console, or both)
12.	Select **Next**
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select **Next**
15.	Scroll to the bottom, make sure to check the acknowledgement that AWS CloudFormation might create IAM resource, and select **Create Stack**
16.	After a minute or two, the stack should complete.
