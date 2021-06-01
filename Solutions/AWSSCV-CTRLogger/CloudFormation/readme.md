# AWS CloudFormation Template
The **awsscv_ctr_logger.yaml** cloudformation template deploys the following resources:

Resource Name | Type | Description
------------ | ------------- | -------------
awsscv_ctr_logger_s3_access | IAM Policy | IAM policy that adds the permissions to access the generated S3 bucket
awsscv_ctr_logger_%INSTANCENAME% | Lambda Function | Called by Kinesis data stream
