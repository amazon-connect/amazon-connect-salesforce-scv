# SCV Common Layers

This project shows how to build common Lambda Layers for use in Lambda development.

## Project Components
- CloudFormation template that builds:
  - NodeJS Lambda Layer:
  - Python Lambda Layer
    
## Project Requirements
- Amazon Web Services account

## Deployment Steps
1. Launch the Amazon Cloudformation template scv_common_layers.yaml
2. The template will ask for one parameter:
   - AWSRegion - This is the region code for the region to which you are deploying.
3. The ARN's for the two (2) layers will be available in the Cloudformation stack outputs
   
