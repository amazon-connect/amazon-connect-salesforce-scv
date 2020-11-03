# Data-Directed Routing: Flow Routing - Preparing for the Installation
To make this example work, you will need to add some configuration to Salesforce and Amazon Connect. In this example, we will demonstrate routing down to three tiers of skillset. In Amazon Connect, the final skillset becomes the queue, so we will need to structure everything appropriately in both platforms. 

## Add Queues to Amazon Connect
In this example, we will route to three tiers of skillset. In the event that an agent is not available, we will route the callt o a relevant queue. To make this example easy, we're going to use a simple help desk example. In our setup, our helpdesk has the following configuration:
- Desktop Support
    - OS
        - MacOS
        - Windows
    - Hardware
- Server Support

With this setup, we're going to provision the following queues in Amazon Connect:
- desktop_os_macos
- desktop_os_windows
- desktop_hardware
- server

## Perform the following steps to pre-configure Amazon Connect:
1. Log in into your Salesforce org and go to **Setup** 
2. In the **Quick Find** field type `Contact`
3. Select **Contact Centers** from the results
4. Next to your Contact Center, select **Connect Settings** to login to Aazon Connect Admin
5. In the left navigation menu, choose **Routing** and then select **Queues**
6. Select **Add new queue**
7. Complete the Add new queue configuration as follows:
 - **Name:** Enter the name as indicated above, for example `desktop_os_macos`
 - **Hours of operation:** Choose an appropriate operating schedule
 - **Outbound caller ID number:** select a phone number from your instance
 - Leave all other fields blank, or complete as desired
8. Select **Add new queue**
9. Repeat steps 6-8 for all four queues
10. In the left navigation menu, choose **Users** and then select **Routing profiles**
11. Select **Add new profile**
12. Set the **Name** to `ddr_routing_example`
13. Set the **Description** to `Sample profile for data-directed routing`
14. Select the checkbox fo **Voice**
15. Add the four queues above to the routing profile. Set priority if desired
16. Choose a queue for the **Default outbound queue**
17. Select **Add new profile**
18. In the left navigation menu, choose **Users** and then select **User Management**
19. Choose an existing user, and select **Edit**
20. Set the user's **Routing Profile** to the new profile you just created
21. Select **Save**
22. In the left navigation menu, choose **Routing** and then select **Queues**
23. Select one of the newly created queues
24. In the Edit queue page, select **Show additional information**
25. Copy the queue ID, which is the final string of characters in the ARN after the last `/`. For example, if the ARN is `arn:aws:connect:us-west-2:123456789012:instance/xxxx75x7-69xx-4613-x3xx-6x500094182x/queue/f80081bf-b055-4ecb-8eea-a52157a801be` the queue ID is `f80081bf-b055-4ecb-8eea-a52157a801be`
26. Paste this to your notepad, making sure to note which queue this is for
27. Choose **Save**
28. **Repeat** steps 23-27 for each newly created queue

## Prep the Queue IDs
In Salesforce, we are going to create queues to match those just created in Amazon Connect. In order to link them, we will set the Queue Name in Salesforce to match the Queue ID from Connect. Unfortunately, Salesforce does not allow `-` in the Queue Name and all must begin with a letter, which may not be the case for all Amazon Connect Queue IDs. The Lambda function we use will account for this and correct the the Queue Name in transit, provided you use a standard substitution pattern. You can use the reccomended patterns provided below, or use whatever you like, just be consistent.
1. In your text editor, prefix each queue id with a consistent set of **UPPERCASE** characters, for example `QQ`. Connect Queue IDs will never contain uppercase characters. For example, `f80081bf-b055-4ecb-8eea-a52157a801be` becomes `QQf80081bf-b055-4ecb-8eea-a52157a801be`
2. Next, Salesforce Queue Names cannot contain hyphens, so replace the hyphens with underscores. For example, `QQf80081bf-b055-4ecb-8eea-a52157a801be` becomes `QQf80081bf_b055_4ecb_8eea_a52157a801be`.
3. Repeat steps 1 & 2 for each of the 4 queue IDs.
4. Make sure to note what your Queue ID prefix is, you will need it later

## Create the Queues in Salesforce
1. Log in into your Salesforce org and go to **Setup** 
2. In the **Quick Find** field type `Queues`
3. Select **Queues** from the results
4. Select **New**
5. For the **Label**, enter the Queue name from Amazon Connect, for example `desktop_hardware`
6. For the **Queue Name**, enter the appropriately formatted Queue ID for the queue, for example `QQf80081bf_b055_4ecb_8eea_a52157a801be`
7. In the **Supported Objects** section, select **Case** and add it to the **Selected Objects**
8. Select Save
9. Repeat steps 4-8 for each of the four queues

## Create Skills in Salesforce
Once you have queues created, the second part of the configuration is to allow for skills routing to a specific agent. To do this, we need to create some skills and assign them to users. 
1. Log in into your Salesforce org and go to **Setup** 
2. In the **Quick Find** field type `Skills`
3. Select **Skills** from the results under **Omni-Channel**
4. Select **New** to add a new skill
5. Set the **Name** to `desktop` and tab out to populate the Developer Name as well
6. Select Save
7. Repeat steps 3-6 to create the following skills:
 - server
 - os
 - hardware
 - macos
 - windows
 
## Create Service Resources and Assign Skills
1. Log in into your Salesforce org and go to **Setup** 
2. Select **App Launcher** from the upper left
3. In the Search field type `Service Resources`
4. Select **Service Resources** from the results
5. Select **New**
6. In the **Name** field, enter an agent name. The agent should already exist as a user in Salesforce (and Service Cloud Voice)
7. Select the **Active** checkbox
8. In the **User** field, enter the user information to find the user, and select the appropriate user from the result
9. For **Resource Type**, select **Agent**
10. Select **Save**
11. Once the Service Resource saves, select the **Assign Skills** button. 
12. Add each of the previously created skills. If you are going to configure multiple users, you can vary the skillset to demonstrate matching certain skillsets.
13. Once you have added the appropriate skills, choose **Next**
14. For **each** skill, configure the following:
 - **Skill level:** any number from 1-9, it is irrelevant for this example
 - **Start date:** set it to the previous day, at any time
15. Select **Save**

## Prerequisite Installations
This installation has multiple prerequisites. Please complete the prerequisistes before moving to installation of this example.
1. Complete the [Salesforce Access Secrets](/Common/AWSSCV-SalesforceConfig) setup
2. Complete the [AWSSCV Common Layers](/Common/AWSSCV-CommonLayers) Setup

You have now completed all of the prerequisites. The next step is to perform the installation of the [Data-Directed Routing: Flow Routing](install.md) example.
