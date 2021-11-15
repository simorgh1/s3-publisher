#!/usr/bin/env bash

set -e
API_Endpoint=$(aws apigatewayv2 get-apis --query 'Items[?Name==`S3Publisher`].ApiEndpoint | [0]')

if [ $API_Endpoint = "null" ]; then
	exit
fi

API_Endpoint=$(echo $API_Endpoint | sed 's/"//g')
API_Endpoint=$API_Endpoint'/uploads'
API_Endpoint="${API_Endpoint}?target=xray"

echo $API_Endpoint
