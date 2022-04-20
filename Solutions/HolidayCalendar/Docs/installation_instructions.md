# Installing the Salesforce Holiday Calendar
This document will walk you through the steps required to deploy the Salesforce Holiday Calendar solution to your AWS account. This solution was specifically designed to operate in a Service Cloud Voice created AWS account, but will work the same in a standard Amazon Connect implementation using Salesforce as the Holiday source.

In order to deploy this template, you must first complete the [first two steps in the main readme](../readme.md). Once those are complete, you can continue with the process below.

## Gather Required Information
The Salesforce Holiday Calendar solution is deployed via AWS CloudFormation. In order to launch the template, you will need the following information:
- ARN for the common_python_layer layer from the [Lambda console](https://console.aws.amazon.com/lambda/home)
- ARN for the Salesforce Config Secrets from the [AWS Secrets Manager console](https://console.aws.amazon.com/secretsmanager/home)
- Amazon Connect Instance Alias from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)
- Amazon Connect Instance ARN from the [Amazon Connect console](https://console.aws.amazon.com/connect/home)

Once you have the required information, you are ready to continue with installation.

## Deploy the CloudFormation Template
The next step is to deploy the CloudFormation template. This template builds and configures all of the AWS resources required to make the Salesforce Holiday Calendar integration work.
1.	Right-click/control-click and open the [CloudFormation template](../CloudFormation/sfhc.yaml) in a new window/tab.
2.  Right-click/control-click the **Raw** button and save the link as sfhc.yaml.
3.  Log into the [AWS console](https://console.aws.amazon.com/console/home)
4.  Navigate to the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation/home)
5.  Choose **Create stack**
6.  In the **Specify template** section, select **Upload a Template file**
7.  Select **Choose file**
7.  Navigate to the **sfhc.yaml** file that you downloaded previously and choose **Open**
8.  Wait a moment for the S3 URL to update, then select **Next**
9.  Provide a name for the stack, such as `SFHolidayCalendar`
10. **Complete the parameters** using the information that you have gathered.
11. Once the parameters are complete, choose **Next**
  - **NOTE:** In Service Cloud Voice bundle deployments, it is normal to see a warning on the next page, Configure stack options
12.	Scroll to the bottom and select **Next**
13.	Scroll to the bottom, select the boxes to **acknowledge that IAM resources will be created**
14. Select **Create Stack**
15. The deployment will take 5-10 minutes. During this time, multiple nested stacks will be deployed. Once the main stack shows **CREATE_COMPLETE**, you are ready to proceed.
**Salesforce Holiday Calendar configuration is complete!**

## Validate the Setup
Once the CloudFormation template deploys, you can validate the connectivity with Salesforce and the holiday lookup process.
1.  Log into the [AWS console](https://console.aws.amazon.com/console/home)
2.  Navigate to the [AWS Lambda console](https://console.aws.amazon.com/lambda/home)
3.  Select the newly created holiday function, which will start with `SFCalendar-`.
4.  In the environment pane, you should see a file named `test`, open that and copy the contents.
5.  Select the dropdown menu for **Test**, and choose **Configure test event**
6.  Provide a name for the Event, then paste the copied json over the existing Event JSON.
7.  Select **Save**
8.  Select **Test**
9.  You should get a response of `{"isHoliday": "0"}` (unless, coincidentally, there happens to be a holiday currently scheduled in Salesforce)
10. Open a new browser tab and login to your Salesforce org with administrator access
11. Go to **Setup**
12. In the Quick Find, enter `Holidays` and choose **Holidays** from the results
13. Select **New** to create a new holiday
14. For the **Holiday Name**, enter `Test Holiday`
15. For **Description**, enter `Today is a test holiday.`
16. For **Date**, leave this to today's date.
17. Deselect **All Day**, then choose a time range that DOES NOT include the current time. For example, if it is 10:00 set the time from 12:00pm to 2:00pm.
18. **Save** the holiday. Leave the Holiday Detail page open.
19. Return to the AWS Lambda console, and **re-run your test**. You should now see information about the holiday, but the `isHoliday` flag should still be `0`.
20. Return to Salesforce setup
21. Select **Edit**
22. Check the **All Day** box and save the holiday.
23. **Save** the holiday. Leave the Holiday Detail page open.
24. Return to the AWS Lambda console, and **re-run your test**. You should still see information about the holiday, but the `isHoliday` flag should now be `1`.
25. **Configuration validated**
