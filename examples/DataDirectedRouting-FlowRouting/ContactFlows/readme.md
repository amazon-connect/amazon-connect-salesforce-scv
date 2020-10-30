# Amazon Connect Contact Flows
The contact flows in this folder are the Amazon Connect contact flow builder experted versions. They must be manually imported into an AMazon Connect Instance. These are useful if you want to add these to an instance without running the CloudFormation template. They will require modification to function correctly in your instance. The included flows are:

Resource Name | Contact Flow Type | Description
------------ | ------------- | -------------
AWSSCV-DDR-Flow | Contact Flow | Sample flow that uses a DTMF menu to select the skillset required, then uses Lambda functions to retreive data from Salesforce via flow.
