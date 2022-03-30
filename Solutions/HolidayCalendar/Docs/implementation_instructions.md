# Implementing the Salesforce Holiday Calendar
In order to use this holiday check in your contact center, you will need to perform some additional configuration. The main Lambda function is added to your Amazon Connect instance by default, but you still need to modify your contact flows to use it as appropriate. We have provided an example contact flow that you can use to validate function within Amazon Connect, and as a starting point for creating your own flows. The holiday Lambda does not require any additional configuration to function, however you can pass along a time zone parameter if you want to check for holidays in a time zone other than the default. You can configure this as follows:

*  tz: set a new User Defined contact attribute with a Destination Attribute value of `tz` and a value of the hours offset from GMT. Negative and partial numbers are allowed.
   *  New York = -5.0
   *  Tokyo = +9.0
   *  Adelaide = +9.5

## Creating Holidays in Salesforce
You [set up your holidays in Salesforce](https://help.salesforce.com/s/articleView?id=sf.customizesupport_holidays.htm&type=5). When doing so, there are a few things to note concerning how Holidays work in this configuration:
1.  This setup supports single holidays, recurring holidays, all day holidays and time limited holidays. This gives you the flexibility to control your routing appropriately. For example, you can create a holiday that closes the center for the entire day on Christmas every year, or one that closes until 1pm on New Years Day.
2.  The function scans all holidays when it checks and finds holidays that are either:
    *  Scheduled for this specific date as a one-time event -or-
    *  Recurring for this date
    *  Are an all-day event -or-
    *  Scheduled during the current time
3.  If it does find a holiday, it will return a response that includes `"isHoliday":"1"`, which is the primary indication that it is currently a scheduled holiday. You can use this value to branch your contact flow accordingly.
4.  If it is a holiday, the response will include the name and description as well. The description can be used as an alternative text to be played to the customer.

Sample holiday response:
```
{
  "isHoliday": "1",
  "holidayName": "SampleHoliday",
  "description": "Today is a sample holiday.",
  "isInHours": "1"
}
```
In this case, the customer would hear "Thank you for calling our contact center. **Today is a sample holiday.** We are currently closed. Please try back during our normal open hours. Thank you. Goodbye."

Sample non-holiday response:
```
{
  "isHoliday": "0"
}
```

## Importing the sample flow
The [Sample Holiday Flow](../ContactFlows/Sample Holiday Check) can be imported into your Amazon Connect instance. Once imported, one block needs to be modified in order for the flow to work appropriately. Here are the steps to import and modify the flow:
1.	Right-click/control-click and open the [Sample Holiday Flow](../ContactFlows/Sample Holiday Check) in a new window/tab.
2.  Right-click/control-click the **Raw** button and save the link as **Sample Holiday Flow**.
3.  Log in to your Amazon Connect instance.
4.  On the navigation menu, choose Routing, Contact flows.
5.  Do one of the following:
    *  To replace an existing contact flow with the one you are importing, open the contact flow to replace.
    *  Create a new contact flow of the same type as the one you are importing.
6.  Choose Save, Import flow.
7.  Select the file to import, and choose Import.
    *  **NOTE:** When the contact flow is imported into an existing contact flow, the name of the existing contact flow is updated, too.
8.  Find the **Set contact attributes** block and open it
9.  Change the **Value** for **use_queue** from `SET QUEUE ARN` to the ARN of the queue you want to use
10. Change the **Value** for **use_function** from `SET FUNCTION ARN` to the ARN of the of the **SFCalendarLambda** that was created with the deployment.
11. To save the imported flow, choose Save. To publish, choose Publish.
12. [Associate a phone number](https://docs.aws.amazon.com/connect/latest/adminguide/associate-phone-number.html) to the sample flow.

You are now able to validate the flow.
