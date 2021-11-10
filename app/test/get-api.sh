#!/usr/bin/bash

set -e
API_Endpoint=$(aws apigatewayv2 get-apis --query 'Items[?Name==`XrayPublisher`].ApiEndpoint | [0]')
API_Endpoint=$(echo $API_Endpoint | sed 's/"//g')
API_Endpoint=$API_Endpoint'/uploads'
API_Endpoint="${API_Endpoint}?target=xray"

echo "Upload Api ${API_Endpoint}"
