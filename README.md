# Amazon Connect Salesforce SCV Campground

This repository contains sample solutions to common use cases that we have encountered with Service Cloud Voice deployments. We have organized this respository by solution, with some underlying common resources.

## Common Resources

| Name | Description | Links |
| ---- | ----------- | ----- |
| SCV-CommonLayers | Lambda layers to provides dependencies, code, and functions for nodejs and python Lambda functions that augment the Service Cloud Voice offering from Salesforce | [CloudFormation](projects/SCV-CommonLayers) |

## Use Case Examples

| Name | Description | Links |
| ---- | ----------- | ----- |
| SCV-CrossAccountSMS | Uses Lambda and cross account permissions to allow Salesforce Service Cloud Voice provisioned Amazon Connect instances to utilize SNS to send SMS messages. | [CloudFormation](projects/SCV-CrossAccountSMS) |


## Contributions

Make sure the `.gitignore` per language is applied.
Make sure your snippet has no external dependencies.
Make sure your snippet is self contained.
