# Data-Directed Routing: Flow Routing
In this data-directed routing example, a Salesforce flow is invoked to provide routing direction to Amazon Connect. We use data gathered within the Amazon Connect contact flow, passing that data to the Salesforce flow, which then uses it to determine the best route for the call. 

## Architecture
(DIAGRAM HERE)

## Solution Desription
In this example, we have a call come into Amazon Connect, and we use an Amazon Lex bot to provide an NLU interaction with the customer. We gather the intent and slot values, then send that data through an AWS Lambda function to our Salesforce flow via the REST API. The flow executes and ultimately provides two destination types:
1. A specific queue
2. A collection of agents that could take the call

For the specific queue, we simple do pattern matching on the name to find a queue that contains all of the data elements that we retrieved via Lex. For the agent collection, we use two custom Apex classes to 1) build the list of skills required to take the call and 2) build the list of agents that match the skillset. 