# AWS CloudFormation Template
The **awsscv_ddr_flow.yaml** cloudformation template deploys the following reosurces:
- IAM Policy that is attached to the common user
- Lambda function that invokes the Salesforce Flow
- Lambda function that processes the target responses from Salesforce
- Lambda function that modifies and injects a contact flow into Amazon Connect