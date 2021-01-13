# SAM Chat Server
AWS Serverless Lambda chat server

## Requirements
- python 3.8
- SAM CLI
- docker
- docker-compose

## Build
```
# buld locally
sam build

# build with docker container
sam build --use-container
```

## Deployment
- ensure deployment machine has the required AWS cred
```
# 1st time
sam deploy --guided

# deploy with existing configurations
sam deploy -t template.yml
```

## Check deployed lambda logs
```
sam logs -n <function> --stack-name <stack> --tail

# example
sam logs -n HelloWorldFunction --stack-name sam-chat-server --tail
```

## Cleanup deployment
- login to aws dashboard and delete stack in cloudformation
- use aws cli
```
aws cloudformation delete-stack --stack-name sam-chat-server
```

## Running locally
- setup local dynamodb (using docker)
- create docker network named `network`
```
# need to be created only once
docker network create network
```
- run local dynamodb
```
# using docker compose to bring up dynamodb
docker-compose up -d

# to cleanup
docker-compose down
```
- run sam-chat-server locally
```
# start locally and connect to docker network "network"
sam local start-api --docker-network network
```

## Run test
```
PYTHONPATH=$(pwd):$(pwd)/chat pytest -v
```