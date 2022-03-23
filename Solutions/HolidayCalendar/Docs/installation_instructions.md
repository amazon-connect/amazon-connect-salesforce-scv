# Installing the Salesforce Holiday Calendar
This document will walk you through the steps required to deploy the Salesforce Holiday Calendar solution to your AWS account. This solution was specifically designed to operate in a Service Cloud Voice created AWS account, but will work the same in a standard Amazon Connect implementation using Salesforce as the Holiday source.

In order to deploy this template, you must first complete the [first two steps in the main readme](../readme.md). Once those are complete, you can continue with the process below.

## Gather Required Information
The Salesforce Holiday Calendar solution is deployed via AWS CloudFormation. In order to launch the template, you will need the following information:
- ARN for the AWSSCV Common Layers - Python layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the Salesforce Config Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- Amazon Connect Instance ARN from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)

Once you have the required information, you are ready to continue with installation.

## Deploy the CloudFormation Template
The next step is to deploy the CloudFormation template. This template builds and configures all of the AWS resources required to make the Salesforce Holiday Calendar integration work.


**Salesforce Holiday Calendar configuration is complete!**
