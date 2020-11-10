# Installing the Data-Directed Routing: Flow Routing Example

## Prerequisites
You MUST complete the prep and prerequisite installs before continuing with this installation. Please refer to the [example prep guide](prep.md) for detailed instructions.

## Salesforce Sample Package
The Flow Routing example uses custom elements in Salesforce. In order to simplify the deployment of the solution, we have prepared an unmanaged package available via the Salesforce AppExchange. By deploying the unmanaged app, you will have the ability to modify the deployed resources as you see fit. Additional resources will be deployed in your AWS account via cloudformation template. 

## Install the Sample Package from AppExchange
1. Log in into your Salesforce org and go to **Setup** 
2. Once at Setup, navigate to: https://login.salesforce.com/packaging/installPackage.apexp?p0=04t6g000008KKYC
3. Re-Login, if required
4. Enter the following password: AWSSCV2020!
 - NOTE: As stated previously, this is an **EXAMPLE**. This is not intended to be placed into production as is with no modification. We are providing this package to simplify the deployment of this example
5. Select **Install for All Users**
6. Choose **Install**
7. After a while, you may receive a message that the app is taking a while to install. You will be emailed when installation is complete, it can take ~5 minutes depending on your org setup.
8. Once you receive the email, return to **Setup**
9. In the **Quick Find** field type `flow`
10. Select **Flows** from the results
11. Select **AWSSCV Data Directed Routing Example Flow**
12. Once Flow Builder opens, select **Debug**
13. In the **Debug the flow** window, enter:
 - find_agent: `1`
 - find_queue: `1`
 - focus: `windows`
 - intent: `desktop`
 - subintent: `os`
14. Select **Run**
15. After a couple of seconds, you should receive **All done**, and the last result should be simillar to:
  - `{!output_response} = "0053t000008RyOrAAK11QQ0bb866c8_ecfd_4df2_b294_c4a3fd17ab14"`
16. Package deployment is complete

# Configure the AWS Resources
Now that the Salesforce environment is ready, you will need to configure the AWS resources that are used in this example. They consist of:
 - Two AWS Lambda functions. One invokes the flow and collects the response. The other processes destinations in the response. 
 - A sample Amazon Connect contact flow to provide the customer experience and perform the routing
 To make deployment easier, we will configure these resources using CloudFormation.
 
## Deploy the Cloudformation Template
1. Right-click/control-click to download the [Data-Directed Routing: Flow Routing CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Examples/AWSSCV-DataDirectedRouting-FlowRouting/CloudFormation/awsscv_ddr_flow.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3. Make sure you are in the **same region** as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4. Navigate to the **CloudFormation console**
5. Select **Create Stack**, and choose **With new resources (standard)**
6. In the Specify Template section, choose **Upload a template file**
7. Select **Choose file**
8. Navigate to the folder where you saved **awsscv_extension_routing_scv.yaml**
9. Select **Next**
10. In the Stack Name field, enter `AWSSCV-DDR-Flow`
11. **Enter the parameters** as follows (most from your notepad):
 - AWSRegion: Select the region that you have deployed Amazon Connect in
 - ConnectInstanceName: Your connect instance name
 - AWSSCVCommonRole: The ARN of the awsscv_common_role role
 - AWSSCVCommonLambdaPythonLayer: ARN of the common python layer
 - sfConfig: ARN for your Salesforce config in AWS Secrets Manager
 - sfOrgId: Provide the ID for your Salesforce Org
 - sfQueuePrefix: The prefix used for Salesforce Queues. The default is QQ.
12.	Select **Next**
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select **Next**
15.	Scroll to the bottom and select **Create Stack**
16.	After a minute or two, the stack should complete.

## Create Test Cases and Validate Lambda
1. Login to the [AWS Console](https://console.aws.amazon.com/console/home)
2. Make sure you are in the **same region** as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
3. Navigate to the **Lambda console**
4. Choose the Lambda function that begins with **awsscv_ddr_flow_**
5. In the Function code section, open the **flow_request_event.json** file
6. Copy the entire contents of the file, and close it
7. Drop down the **Select a test event** selection box (just to the left ot the **Test** button), and choose **Configure test events**
8. For the Event name, enter `invokeFlow`
9. Replace the existing json contents with the data that you copied
10. Select **Create**
11. Once the save completes, select **Test**
12. You should receive a response similar to:
`{
  "agent_targets": "0053t000008RyOr@00D3t000003d8t5,0053t0000086HG2@00D3t000003d8t5",
  "queue_target": "arn:aws:connect:us-west-2:123456789012:instance/9308c2a1-9bc6-4cea-8290-6c0b4a6d38fa/queue/0bb866c8-ecfd-4df2-b294-c4a3fd17ab14",
  "has_queue": "1",
  "has_agents": "1",
  "status": "success"
}`
13. Select **Functions** in the navigation breaddcrumbs to go back to the list of functions
14. Choose the Lambda function that begins with **awsscv_ddr_flow_target_processor_**
15. In the Function code section, open the **target_start_event.json** file
16. Copy the entire contents of the file, and close it
17. Drop down the **Select a test event** selection box (just to the left ot the **Test** button), and choose **Configure test events**
18. For the Event name, enter `startList`
19. Replace the existing json contents with the data that you copied
20. Select **Create**
21. In the Function code section, open the **target_processing_event.json** file
22. Copy the entire contents of the file, and close it
23. Drop down the **Select a test event** selection box (just to the left ot the **Test** button), and choose **Configure test events**
24. Slect **Creat new test event**
25. For the Event name, enter `processList`
26. Replace the existing json contents with the data that you copied
27. Select **Create**
28. Once the save completes, drop down the **Select a test event** selection box and choose **startList**
29. Now select **Test**
30. You should receive a response similar to:
'{
  "current_state": "processing",
  "next_target": "0053t000008RyOr@00D3t000003d8t5",
  "remaining_target_list": "[\"0053t0000086HG2@00D3t000003d8t5\"]",
  "remaining_targets": 1
}'
31. Now, drop down the **Select a test event** selection box and choose **processList**
32. Now select **Test**
33. You should receive a response similar to:
'{
  "next_target": "0053t0000086HG2@00D3t000003d8t5",
  "current_state": "complete",
  "remaining_targets": 0
}'
34. Lambda validation complete
35. While you are in the Lambda console, copy the ARNs for the following Lambda functions (the following are partial function name matches) and paste them to a textpad:
 - InvokeTelephonyIntegrationApiFunction
 - awsscv_ddr_flow_target_processor
 - awsscv_ddr_flow_scv

## Update your Amazon Connect Instance
1. Access to the [AWS Console](https://console.aws.amazon.com/console/home)
2. Navigate to the [Amazon Connect Console](https://console.aws.amazon.com/connect/home)
3. Select your **Amazon Connect instance**
4. Select **Contact Flows** from the left navigation menu
5. Go to the **AWS Lambda** section
6. In the **Function Dropdown**, choose the function that begin with **awsscv_ddr_flow_target_processor**
7. Select **+ Add Lambda Function
8. In the **Function Dropdown**, choose the function that begin with **awsscv_ddr_flow**
9. Select **+ Add Lambda Function
10. Select **Overview** from the left navigation menu
11. Select **Log in for emergency access** to open the Amazon Connect admin UI
13. Navigate to **Routing**, and select **Phone numbers**
14. Select **Claim a number**
15. Select **DID (Direct Inward Dialing)** and then **set the country** as appropriate
16. Select the desired phone number
17. In the **Description**, enter `DDR Test Line`
18. Form the ***Contact flow / IVR*** list, select **AWSSCV-DDR-Flow**
19. Select **Save**
20. After ~2 minutes, your configuration will be ready to test.

## Testing the configuration
Follow these basic steps to test the configuration
1. **Login to Salesforce**, but do not login to Omni-Channel
2. Open **Setup** in a new tab
3. In the quick find, enter `contact`, and select **Contact Centers** from the result
4. Select **Telephony Provider Settings** for your contact center
5. Once the Amazon Connect UI opens, select **Metrics and quality**, then choose **Real-time metrics**
6. Select **Queues**
7. Once the queues display opens, select the **New Table** button and choose **Agent queues**
8. Return to Salesforce and login to Omni-Channel by choosing **Phone-Available**
9. Return to Amazon Connect and validate that the Queues and Agent queues all show staffed and that your agent is online. 
10. **Dial the phone number** that you provisioned earlier
11. **Press 2** for server support. Notice that the message will state that it has found someone to assist.
12. Return to the Salesforce and **answer the incoming contact**. Once connected, return to the real-time view in Amazon Connect. Note that the call is Active in the agent personal queue. 
13. **End the call as the customer**, but DO NOT clear the call in Salesforce.
14. **Call in** again and **choose 2** once more. This time, since the agent is still in after call work and not available, you will hear "Nobody is currently available, however, I have identified a group of people that can help.". This indicates that the call will be queued to the target queue returned from Salesforce
15. Return to Salesforce, **clear the old call and accept the new call**
16. Once the call connects, **return to Amazon Connect**
17. Validate the active call in the **server queue**
18. Validation complete

