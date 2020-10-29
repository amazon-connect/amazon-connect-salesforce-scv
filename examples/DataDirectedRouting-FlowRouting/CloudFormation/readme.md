# AWS CloudFormation Template
The **awsscv_ddr_flow.yaml** cloudformation template deploys the following reosurces:
- IAM Policy that is attached to the common user
- Lambda function that invokes the Salesforce Flow
- Lambda function that processes the target responses from Salesforce
- Lambda function that modifies and injects a contact flow into Amazon Connect
- Amazon Connect contact flow that provides invokes the functions and performs the route

Resource Name | Type | Description
------------ | ------------- | -------------
AWSSCV_contact_flow_build | IAM Policy | IAM policy that adds the permissions to create contact flows
awsscv_ddr_flow_%INSTANCENAME% | Lambda Function | Called by contact flow. Invokes a Salesforce flow
awsscv_ddr_flow_target_processor_%INSTANCENAME% | Lambda Function | Called by contact flow. Processes agent targets from the previous Lambda Function
awsscv_contact_flow_builder_%INSTANCENAME% | Lambda Function | Called during cloudformation deployment. Creates the sample contact flow.