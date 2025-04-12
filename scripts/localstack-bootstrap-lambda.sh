#!/bin/bash
set -e
export AWS_PAGER=""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd ../src && zip -r ../lambda.zip ./*
cd $SCRIPT_DIR

export ENDPOINT_URL="http://localhost:4566"

QUEUE_NAME="notificacao-email"
LAMBDA_NAME="vidsnap-notification"
IMAGE_NAME=lambda-notification:latest
REGION="us-east-1"

# Cria a fila SQS
aws --endpoint-url=$ENDPOINT_URL sqs create-queue --queue-name $QUEUE_NAME

# Cria a lambda function com container
aws --endpoint-url=$ENDPOINT_URL lambda create-function \
  --function-name $LAMBDA_NAME \
  --runtime python3.10 \
  --handler lambda_function.handler \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --zip-file fileb://../lambda.zip \
  --region $REGION \
  --environment Variables="{MAIL_USER=<EMAIL>,MAIL_PASS=<SENHA>}"

# Obtém a ARN da fila
QUEUE_ARN=$(aws --endpoint-url=$ENDPOINT_URL sqs get-queue-attributes \
  --queue-url $ENDPOINT_URL/000000000000/$QUEUE_NAME \
  --attribute-name QueueArn \
  --query 'Attributes.QueueArn' --output text)

# Cria a trigger entre SQS e Lambda
aws --endpoint-url=$ENDPOINT_URL lambda create-event-source-mapping \
  --function-name $LAMBDA_NAME \
  --batch-size 1 \
  --event-source-arn $QUEUE_ARN