# Salesforce Config
The Salesforce Config deployment process establishes a Self-Signed SSL Certificate, Salesforce Connected App, Salesforce User, and information about the Salesforce org. The included CloudFormation template then saves the Salesforce configuration information to the AWS account using AWS Secrets Manager. This allows various AWS Lambda functions to access config information from a secure storage location as needed. It also creates an IAM Policy and Role common to the deployments from this repository. Finally, it creates a set of common Lambda layers, and a Lambda function that can be used to validate API connectivity between Lambda and your Salesforce Org.

**This deployment is the foundation for all Salesforce solutions and examples in this repository and is a common requirement.**

## Deploying this Configuration
It is a two step process to deploy Salesforce Config. Please perform the following steps in order:

1.  [Perform the prerequisite configuration](Docs/prerequisites.md)
2.  [Deploy the template and validate](Docs/installation.md)

**Current Published Version:** 2022.08.01
Current published version is the version of the code and templates that has been deployed to our S3 buckets 
