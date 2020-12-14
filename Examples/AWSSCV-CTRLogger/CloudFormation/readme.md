# AWS CloudFormation Template
The **awsscv_ctr_logger.yaml** cloudformation template deploys the following resources:

Resource Name | Type | Description
------------ | ------------- | -------------
AWSSCV_contact_flow_build | IAM Policy | IAM policy that adds the permissions to create contact flows
awsscv_ctr_logger_%INSTANCENAME% | Lambda Function | Called by contact flow. Invokes a Salesforce flow
