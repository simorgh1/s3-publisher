#!/usr/bin/bash

set -e

sam validate
sam build
sam deploy

if [ "$1" == "up" ]; then
    # add notification configuration since cloudformation is unable to create and add the notification into the s3 bucket.
    Incomming=$(aws cloudformation describe-stack-resource --stack-name XrayPublisher --logical-resource-id Incomming --query 'StackResourceDetail.PhysicalResourceId')
    Incomming=$(echo $Incomming | sed 's/"//g')
    PublishLambda=$(aws cloudformation describe-stack-resource --stack-name XrayPublisher --logical-resource-id PublishArtifacts --query 'StackResourceDetail.PhysicalResourceId')
    PublishLambda=$(echo $PublishLambda | sed 's/"//g')
    PublishLambdaArn=$(aws lambda get-function --function-name $PublishLambda --query 'Configuration.FunctionArn')
    ReplaceString='s/PublishArtifactsFunction/'$PublishLambdaArn'/'

    echo 'Configuring S3 bucket '$Incomming' to notify '$PublishLambdaArn
    sed -i.bak $ReplaceString InCommingLambdaNotification.yaml
    aws s3api put-bucket-notification-configuration --bucket $Incomming --cli-input-yaml file://InCommingLambdaNotification.yaml
    mv InCommingLambdaNotification.yaml.bak InCommingLambdaNotification.yaml
fi
