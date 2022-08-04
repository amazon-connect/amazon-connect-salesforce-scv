# Setup
Follow the following steps to prepare your Salesforce Org before running the CloudFormation template. As you proceed through these instructions, it is recommended that you use a text editor to save important information along the way. Each item you need to save will be specifically called out. Much of this process is based on the [Create Your Connected App](https://trailhead.salesforce.com/en/content/learn/modules/sfdx_travis_ci/sfdx_travis_ci_connected_app) Trailhead, but the instructions here should be used in place of those from the Trailhead.

## Prerequisites
1. You will need OpenSSL to generate certificates. An easy way to check if you already have OpenSSL is to open a command line/terminal window and type `which ssl`. You should see a response similar to `/usr/bin/openssl`. If you do not, you will need to install OpenSSL before continuing.

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
9. Your folder should now have four files:
 - server.crt <- This is your certificate
 - server.csr <- This is the certificate request
 - server.key <- This is the private key
 - encoded_key.txt <- This is the base64 encoded private key

## Collect additional Salesforce Org details
1.  Log in into your Salesforce org and go to Setup
2.	In the Quick Find field, enter `apex`, then select **Apex Classes** from the results
3.	Select New
4.	Select the Version Settings tab
5.	**Note the Salesforce.com API version in your notepad**
6.  In the Quick Find field, enter `My Domain`, then select **My Domain** from the results
7.  In the My Domain Step 4 box, note the domain name. Add it to your notes, prefixing it with **https://**, for example:
    - https://example.my.salesforce.com
8.  In the Quick Find field, enter `Company`, then select **Company Information** from the results
9.  **Note the Salesforce.com Organization ID value in your notepad**

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
    * Manage user data via APIs (api)
    * Perform requests at any time (refresh_token, offline_access)
    * Manage user data via Web browsers (web)
10.	Select Save at the bottom of the screen.
11.	Select Continue on the New Connected App page
12.	You should now be at the new app’s page
13. Select Manage Consumer Details, this will open a new tab/window and require you to revalidate your login.
14. Once you verify your identity, you will be at the details page.
15.	**Copy the value for Consumer Key to your notepad**
16.	At the top of the detail page, select Manage
17.	On the Connected App Detail page, select the Edit Policies button
18.	Set Permitted Users to Admin approved users are pre-authorized and choose OK on the pop-up dialog
19.	Select Save

## Create a new user
1.  In the Quick Find field, type `users` then select Users from the results
2.  Select New User
3.  Set the required fields as:
    * Last Name: awsutil
    * Alias: awsutil
    * Email: provide a valid email address
    * Username: awsutil@%yoursalesforcedomain%.com
    * Nickname: awsutil
4.  On the right-hand side, set **User License** to **Salesforce**
5.  Set the **Profile** to **System Administrator**
6.  Choose Save
7.  **Copy the username to your notepad**

## Create a new Permission Set
1.  From Setup, enter Permission in the Quick Find box, then select Permission Sets
2.  Select New
3.  For the Label, enter: `AWS_Utility`, then press tab
4.  Select Save
5.  From the **Permission Sets** list, select **AWS_Utility**
6.  Select **Manage Assignments**
7.  Select **Add Assignments**
8.  Select the checkbox next to the **awsutil** user
9.  Select **Assign**, then select **Done**
10. Enter `App Manager` in the Quick Find box, then select App Manager
11. To the right of **AWS_Utility**, select the list item drop-down arrow and choose **Manage**
12. In the Permission Sets section, select **Manage Permission Sets**
13. Select the checkbox next to **AWS_Utility**, then choose **Save**

You have now completed the prerequisite configuration. Please continue with [depolying the template](installation.md).
