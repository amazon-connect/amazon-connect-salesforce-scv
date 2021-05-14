# Salesforce Config
Establishes a Self-Signed SSL Certificate, Salesforce Connected App, a Salesforce User, and information about the Salesforce org. Saves the information to the AWS account using AWS Secrets Manager for secure storage and retrieval of the credentials and configuration info as needed. Also creates an IAM Policy and Role common to the deployents from this repository.

# Setup
Follow the following steps to prepare your Salesforce Org before running the CloudFormation template. As you proceed through these instructions, it is recommended that you use a text editor to save important information along the way. Each item you need to save will be specifically called out. Much of this process is based on the [Create Your Connected App](https://trailhead.salesforce.com/en/content/learn/modules/sfdx_travis_ci/sfdx_travis_ci_connected_app) Trailhead, but the instructions here should be used in place of those from the Trailhead.

## Prerequisites
1. Complete the [AWSSCV Common Layers](../../Common/AWSSCV-CommonLayers/readme.md) Setup
2. You will need OpenSSL to generate certificates. An easy way to check if you already have OpenSSL is to open a command line/terminal window and type `which ssl`. You should see a response similar to `/usr/bin/openssl`. If you do not, you will need to install OpenSSL before continuing.

## Create a self-signed SSL certificate and private key
1. Create a certificates folder on your computer to store the files that will be created.
2. Open a command line/terminal window and navigate to your newly created folder
3. Generate an RSA private key by entering `openssl genrsa -des3 -passout pass:SomePassword -out server.pass.key 2048`
 - NOTE: Make sure to replace **SomePassword** with a password of your choosing
4. Now use the private key to generate a key file by entering `openssl rsa -passin pass:SomePassword -in server.pass.key -out server.key`
 - NOTE: Make sure to replace **SomePassword** with the password that you provided above
5. Delete the server.pass.key file by entering `rm server.pass.key`
6. Next, you will request the certificate. Once you enter the following command, you will be asked to provide additional information. Please keep track of what you have provided. To request the certificate, enter `openssl req -new -key server.key -out server.csr`
7. Now, you need to generate the SSL certificate. Enter `openssl x509 -req -sha256 -days 365 -in server.csr -signkey server.key -out server.crt`
8. Fianlly, you need to encode the private key for storage by entering `base64 server.key > encoded_key.txt`
8. Your folder should now have four files: 
 - server.crt <- This is your certificate
 - server.csr <- This is the certificate request
 - server.key <- This is the private key
 - encoded_key.txt <- This is the base64 encoded private key

## Collect additional Salesforce Org details
1. Log in into your Salesforce org and go to Setup 
2.	In the Quick Find field, enter `apex`, then select **Apex Classes** from the results 
3.	Select New
4.	Select the Version Settings tab
5.	**Note the Salesforce.com API version in your notepad**
6. In the Quick Find field, enter `My Domain`, then select **My Domain** from the results
7. In the My Domain Step 4 box, note the domain name. Add it to your notes, prefixing it with **https://**, for example:
 - https://example.my.salesforce.com
8. In the Quick Find field, enter `Company`, then select **Company Information** from the results
9. **Note the Salesforce.com Organization ID value in your notepad**

## Create a New Connected App
1.	Log in into your Salesforce org and go to Setup 
2.	In the Quick Find field, type `app manager`, then select App Manager from the results 
3.	In the upper right corner, select New Connected App
4.	On the New Connected App form, enter `AWS_Utility` as the name for the Connected App. This will populate the API Name automatically. Then provide a contact email address
5.	Select the checkbox to Enable OAuth Settings 
6.	Set the Callback URL to `http://localhost:1717/OauthRedirect`
7.  Select **Use digital signatures**
8.  Select Choose File, and upload the server.crt file you created earlier
9.	In the Selected OAuth Scopes section, select the following and add them to the Selected OAuth Scopes:
  * Access and manage your data (api)
  * Perform requests on your behalf at any time (refresh_token, offline_access)
  * Provide access to your data via the Web (web)
10.	Select Save at the bottom of the screen.
11.	Select Continue on the New Connected App page
12.	You should now be at the new app’s page
13.	**Copy the value for Consumer Key to your notepad**
14.	At the top of the detail page, select Manage
15.	On the Connected App Detail page, select the Edit Policies button
16.	Set Permitted Users to Admin approved users are pre-authorized and choose OK on the pop-up dialog
17.	Select Save

## Create a new user
1. In the Quick Find field, type `users` then select Users from the results 
2. Select New User
3. Set the required fields as:
 a. Last Name: awsutil
 b. Alias: awsutil
 c. Email: provide a valid email address
 d. Username: awsutil@<yoursalesforcedomain>.com
 e. Nickname: awsutil
4. On the right-hand side, set **User License** to **Salesforce**
5. Set the **Profile** to **System Administrator**
6. Choose Save
7. **Copy the username to your notepad**

## Create a new Permission Set
1. From Setup, enter Permission in the Quick Find box, then select Permission Sets
2. Select New
3. For the Label, enter: `AWS_Utility`, then press tab
4. Select Save
5. From the **Permission Sets** list, select **AWS_Utility**
6. Select **Manage Assignments**
7. Select **Add Assignments**
8. Select the checkbox next to the **awsutil** user
9. Select **Assign**, then select **Done**
10. Enter `App Manager` in the Quick Find box, then select App Manager
11. To the right of **AWS_Utility**, select the list item drop-down arrow and choose **Manage**
12. In the Permission Sets section, select **Manage Permission Sets**
13. Select the checkbox next to **AWS_Utility**, then choose **Save**

## Store Salesforce Settings in AWS Secrets Manager
To ensure that your Salesforce credentials are secure, the Lambdas require that the credentials are stored in AWS Secrets Manager. AWS Secrets Manager is a highly secure service that helps you store and retrieve secrets.

1.	Right-click/control-click to download the [CloudFormation template](https://raw.githubusercontent.com/amazon-connect/amazon-connect-salesforce-scv/master/Common/AWSSCV-SalesforceConfig/CloudFormation/awsscv-ssm.yaml).
2. In a new browser tab, login to the [AWS Console](https://console.aws.amazon.com/console/home)
3.	Make sure you are in the same region as your Amazon Connect instance. You can set the region by expanding the region selector in the upper right and choosing the region
4.	Navigate to the CloudFormation console
5.	Select Create Stack, and choose With new resources (standard)
6.	In the Specify Template section, choose Upload a template file
7.	Select Choose file
8.	Navigate to the folder where you saved awsscv-ssm.yaml
9.	Select Next
10.	In the Stack Name field, enter `AWSSCV-SalesforceConfig`
11.	Enter the parameters as follows (most from your notepad):
 - AWSRegion: Select the region that you have deployed Amazon Connect in
 - ConnectInstanceName: Your connect instance name
 - AWSSalesforceCommonPythonLayer: The ARN of the Common Python Layer created by deployment of the AWSSCV-CommonLayers prerequisite stack. This value is available in the outputs of the AWSSCV-CommonLayers stack.
 - sfConsumerKey: The consumer key from your connected app
 - sfHost: The full https url to your salesforce org
 - sfOrgId: Provide your Salesforce.com Organization ID
 - sfPrivateKey: The contents of the encoded_key.txt that you generated as a part of the setup process.
 - sfUsername: Your awsutil username
 - sfMode: The type of Salesforce org (PROD, DEV, SANDBOX)
12.	Select Next
13.	In Service Cloud Voice deployments, it is normal to see a warning on the next page, Configure stack options
14.	Scroll to the bottom and select Next
15.	Scroll to the bottom and select Create Stack
16.	After a minute or two, the stack should complete.

## Post Install Validation
Once the Salesforce Config CloudFormation stack is complete, the Salesforce integration should be validated.

1. While in the Stack details, select **Resources**
2. Find the Lambda function with the Logical ID **scvsalesforcevalidator**
3. **Select the link** in the Physical ID column to open that resource in a new tab and switch to that tab.
4. Select the **Test** button
5. Provide an **Event name**
6. You may keep the default test payload
7. Select the **Create** button
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

