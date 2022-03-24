## NOTE: Common Layers has been deprecated ##
New implementations either depend on the Salesforce config (which incorporates the layers), or reference the layer source directly. There is no need to deploy this any longer.

# AWSSCV Common Layers

AWSSCV Common layers for AWS Lambda provides dependency modules used by the solutions included in this repository. It is a likely prerequisite for any of the projects the incorporate AWS Lambda functions. For new implementations, there is an AWS CloudFormation template that completes the initial deployment for you. Once deployed, you can update your layers using the Easy Upgrade process below.

## Project Components
- CloudFormation template that builds:
  - NodeJS Lambda Layer
  - Python Lambda Layer

## Project Requirements
- Amazon Web Services account

## Deployment Steps
**Solution should not be deployed**
