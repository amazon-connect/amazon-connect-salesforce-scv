# Holiday Calendar for Service Cloud Voice
While Amazon Connect has an Hours of Operation function, it does not have a built-in holiday calendar system. It was always left to the customer to integrate against whatever system normally tracks holiday closures. In many cases, customers used existing AWS services to build a holiday calendar, or used predefined partner solutions. In the case of Service Cloud Voice, we have an available Holiday tracking systems already: Salesforce. This solution uses the holiday object in Salesforce to determine when there should be a center closed event.

This solution functions as follows (relevant Salesforce fields in parenthesis):
1.  Contact flow invokes an AWS Lambda function to query Salesforce
2.  Function pulls all holidays that have been configured in Salesforce
3.  Function iterates through the list, looking at two criteria:
    1. Is there a single or recurring(IsRecurrence) holiday event for this specific date (ActivityDate)
    2. If yes, is that holiday an all day event (IsAllDay) or is it currently within the timeframe defined in the holiday (>StartTimeInMinutes, <EndTimeInMinutes).
4. If both conditions are met, the function returns:
    1. The name of the holiday (Name)
    2. A flag indicating that there is a holiday
    3. A flag indicating that it is in the timeframe for the holiday
    4. The description (Description)
5. The contact flow branches on the flag
6. Connect plays the returned description as the closure message.

Additionally, this deployment configures an Amazon EventBridge rule to execute the function every 3 minutes, keeping it warm and ensuring that it returns a response quickly.

To deploy the Holiday Calendar, you will need to complete the following:
1. Complete the [AWSSCV Salesforce Config](../../Common/AWSSCV-SalesforceConfig/readme.md) setup
2. Complete the [Salesforce Holiday Calendar Installation](Docs/installation_instructions.md)
