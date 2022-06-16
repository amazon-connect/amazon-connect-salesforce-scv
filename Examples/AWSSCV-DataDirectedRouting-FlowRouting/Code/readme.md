# Data-Directed Routing: Flow Routing Code Descriptions
The Data-Directed Routing: Flow Routing example uses 1 AWS Lambda function for deployment and 2 AWS Lambda functions for operation. There are other supporting files as well. Each is described below.
File | Type | Parent Function | Description
------------ | ------------- | ------------- | -------------
awsscv_contact_flow_builder.py | Python 3.8 | awsscv_contact_flow_builder | Uses the .json contact flow template to insert a new contact flow into the Amazon Connect instance using the provided parameters
awsscv_ddr_flow_cf.json | JSON | awsscv_contact_flow_builder | JSON file that contains the exxported contact flow template
awsscv_ddr_flow.py | Python 3.8 | awsscv_ddr_flow | Invocation function that uses the passed parameters in the contact flow to invoke a Salesforce flow and get the response.
flow_request_event.json | JSON | awsscv_ddr_flow | Sample contact flow event that allows you to test the function
awsscv_ddr_flow_target_processor.py | Python 3.8 | awsscv_ddr_flow_target_processor | Processes the list of agent targets returned from the Salesforce flow execution and returns the next agent to try, the remaining agent list, and the current processing status
target_start_event.json | JSON | awsscv_ddr_flow_target_processor | Sample contact flow event to simulate the start of an agent list process
target_processing_event.json | JSON | awsscv_ddr_flow_target_processor | Sample contact flow event to simulate the continued processing of an agent list
