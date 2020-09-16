# Installing Voicemail Express
This document will walk you through the steps required to deploy the Voicemail Express solution to your AWS account. This solution was specifically designed to operate in a Service Cloud Voice created AWS account, but will work the same in a standarad Salesforce + Amazon Connect CTI Adapter configuration.

In order to deploy this template, you must first complete the [installation prerequisites](docs/vmx_prerequistes.md). Once those are complete, you can continue with the process below.

**Note:** You will need to save information to a notepad during the entire setup process. 

## Gather Required Information
The Voicemail Express solutions Uses AWS CloudFormation to deploy most of the solution. In order to launch the template, you will need the following information:
- ARN for the SCV Common Layers - Node layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the SCV Common Layers - Python layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the Amazon Kiesis data stream used for streaming your CTRs from the [Amazon Kinesis Data streams console](https://console.aws.amazon.com/kinesis/home)
- ARN for the Salesforce Access Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- The full domain for your Salesforce org, including the https://
- Your current Salesforce API version
- The field names for the two fields that you created in the prerequisites

Once you have the required information, you are ready to continue with installation. 

## Delploy the Cloudformation Template
1. Download the cloudformation template
1. Log into the [AWS console](https://console.aws.amazon.com/console/home)
1. Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
1. 
