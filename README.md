# S3 Publisher

Provides a Rest Api for uploading the test results to S3 bucket.

## Overview

This Application is designed to leverage the Serverless architecture by using the AWS Lambda functions and HttpApi which uses an Authorizer for Client authentication.

The communication flow is based on a decoupled design so that the Lambda function for uploading the test artifacts is not directly used. Instead, after a successful client authentication, an S3 signed Url is generated that could be used to upload the test results.

## System Requirements

- AWS Cli ([configured](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html))
- Python 3.9
- NodeJs 16.x
- AWS [SAM](https://aws.amazon.com/serverless/sam/)
- jq

AWS Serverless Application Model was used to design, build and deploy this application which uses Lambda function, HttpApi and S3 buckets. SAM infrastructure as code template is inherited from CloudFormation and the current template is used to deploy all infrastructure used by this application.

## Deployment

For deploying the application in a new environment, you should package and publish the application to sam repository once, after that all subsequent build and deployments could be applied using related sam commands.

Using publish.sh would validate the sam template, build and deploy it to the configured aws region. For the first deployment use up argument, so the missing lambda notification is configured.

After deployment, please configure the environment variables for the authorizer and publish test artifacts lambda functions.

## Test

For testing the functionality, switch to the test folder and run **upload-results.py** command, it will authenticate the client and get the signed url for uploading a test file to s3 bucket. Please update the authorization environment variable according to the environment value you set in the authorizer function. For more information, look into the AuthorizerAPIKey variable in the sam template.

### Local testing keyAuthorizer

```bash
/workspaces/s3-publisher (main) $ sam local invoke ApiKeyAuthorizer -e keyAuthorizer/requestEvent.json -n keyAuthorizer/env.json
```

### Local testing getSignedURL

```bash
/workspaces/s3-publisher (main) $ sam local invoke UploadRequest
```

## Cleanup

In order to remove all created aws resources during deployment, run the following command in app folder

```bash
/workspaces/s3-publisher (main) $ sam delete
```

## Code formatting

Automatic Code formatting is done using [pre-commit](https://pre-commit.com) hooks.

pre-commit manages all of your hooks using a yaml config file: *.pre-commit-config.yaml*

When you run git commit command, it will first execute the configured pre-commit hooks for the staged files.
