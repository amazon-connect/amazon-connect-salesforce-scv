# Deploy the CloudFormation Template
To ensure that your Salesforce credentials are secure, the Lambdas require that the credentials are stored in AWS Secrets Manager. AWS Secrets Manager is a highly secure service that helps you store and retrieve secrets.

## Additional Reference
There is a [video](sf_config.mp4) of this process available for reference.

## Deploy the Template
1.	Right-click/control-click and open the [CloudFormation template](CloudFormation/awsscv_sc.yaml) in a new window/tab.
2.  Right-click/control-click the **Raw** button and save the link as awsscv_cs.yaml.
3.  In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
4.	Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
5.	Navigate to the CloudFormation console
6.	Select **Create Stack**, and choose **With new resources (standard)**
7.	In the Specify Template section, choose **Upload a template file**
8.	Select **Choose file**
9.	Navigate to the awsscv-sc.yaml you downloaded previously and choose **Open**
10.	Wait a moment for the S3 URL to update, then select **Next**
11.	In the Stack Name field, enter `AWSSCV-SalesforceConfig`
12.	**Complete the parameters** using the information that you have gathered.
13.	Once the parameters are complete, choose **Next**
    *  NOTE: In Service Cloud Voice bundle deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select **Next**
15. Scroll to the bottom, select the boxes to **acknowledge that IAM resources will be created**.
16.	Scroll to the bottom and select **Create Stack**
17.	After a minute or two, the stack should complete.

## Post Install Validation
Once the Salesforce Config CloudFormation stack is complete, the Salesforce integration should be validated.

1. While in the Stack details, select **Resources**
2. Find the Lambda function with the Logical ID **SCVSalesforceValidator**
3. **Select the link** in the Physical ID column to open that resource in a new tab and switch to that tab.
4. Select the **Test** button
5. Provide an **Event name**
6. You may keep the default test payload, and leave all other options as their defaults.
7. Select the **Save** button
8. Select the **Test** button

If the test is successful, results will be displayed indicating success.

If the test is not successful, results will be displayed indicating a failure.  You may set a logging level to further debug your configuration.
1. In the **Environment variables** section, select the **Edit** button
2. Select the **Add environment variable** button
3. Enter **lambda_logging_level** in the **Key** field
4. Enter **DEBUG** in the **Value** field
5. Select the **Save** button
6. Select the **Test** button

Additional details will be displayed in the **Log output** section of the **Execution result** panel.
