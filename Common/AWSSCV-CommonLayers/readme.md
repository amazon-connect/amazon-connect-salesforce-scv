# AWSSCV Common Layers

AWSSCV Common layers for AWS Lambda provides dependency modules used by the solutions included in this repository. It is a likely prerequisite for any of the projects the incorporate AWS Lambda functions. For new implementations, there is an AWS CloudFormation template that completes the initial deployment for you. Once deployed, you can update your layers using the Easy Upgrade process below. 

## Project Components
- CloudFormation template that builds:
  - NodeJS Lambda Layer
  - Python Lambda Layer
    
## Project Requirements
- Amazon Web Services account

## Deployment Steps
1. Right-click/control-click to download the [CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Common/AWSSCV-CommonLayers/CloudFormation/awsscv_common_layers.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3.	Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/home)
5.	Select Create Stack, and choose With new resources (standard)
6.	In the Specify Template section, choose Upload a template file
7.	Select Choose file
8.	Navigate to the folder where you saved awsscv_common_layers.yaml
9.	Select Next
10.	In the Stack Name field, enter `AWSSCV-CommonLambdaLayers`
11.	The template will ask for one parameter:
   - AWSRegion - This is the region code for the region to which you are deploying.
12.	Select Next
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select Next
15.	Scroll to the bottom and select Create Stack
16.	After a minute or two, the stack should complete.
17. The ARN's for the two (2) layers will be available in the Cloudformation stack outputs

## Examples
Python code examples are available in the [Examples folder](Docs/Examples)
## Layer Last Updated
- Node.js: 2020-09-30
- Python: 2020-09-30

