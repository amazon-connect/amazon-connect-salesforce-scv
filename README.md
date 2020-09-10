# Amazon Connect Salesforce SCV Campground

This repository is a collection of code snippets for working with different parts of Amazon Connect with Salesforce Service Cloud Voice (SCV). The snippets are organized by language. There's an additional collection of projects that come with associated CloudFormation templates and Contact Flows in the `projects/` directory.

We currently have snippets in:

* Python under [python/](python/)
* Java under [java/](java/)
* DotNet (C#) under [dotnet/](dotnet/)
* Javascript under [javascript/](javascript/)
* Go under [go/](go/)
* PowerShell [powershell/](powershell/)

Feel free to add more languages. Please follow the requirements in each subdirectory README.

## Snippets

| Name | Description | Links |
| ---- | ----------- | ----- |

## Projects

| Name | Description | Links |
| ---- | ----------- | ----- |
| SCV-CommonLayers | Provides dependencies code and functions for nodejs and python Lambda functions that augment the Service Cloud Voice offering from Salesforce | [CloudFormation](projects/SCV-CommonLayers) |
| SCV-CrossAccountSMS | Uses Lambda and cross account permissions to allow Salesforce Service Cloud Voice provisioned Amazon Connect instances to utilize SNS to send SMS messages. | [CloudFormation](projects/SCV-CrossAccountSMS) |


## Contributions

Make sure the `.gitignore` per language is applied.
Make sure your snippet has no external dependencies.
Make sure your snippet is self contained.
