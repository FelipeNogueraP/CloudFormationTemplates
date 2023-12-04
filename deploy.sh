#!/bin/bash

# Log messages
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Function to deploy a template and track time
deploy_template() {
    template_path=$1
    stack_name=$2

    # Start timer
    start_time=$(date +%s)

    log "Starting deployment of stack: $stack_name"
    if ! aws cloudformation create-stack --stack-name $stack_name --template-body file://$template_path --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM; then
        log "Failed to initiate stack creation for $stack_name. Aborting."
        exit 1
    fi

    log "Waiting for stack $stack_name to be created..."
    if ! aws cloudformation wait stack-create-complete --stack-name $stack_name; then
        log "Failed to create stack $stack_name. Check CloudFormation console for details."
        exit 1
    fi
    
    # End timer and calculate duration
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    log "Stack $stack_name deployed successfully. Time taken: $duration seconds."
}

# Template paths
template1="G_ProfilePage/networkAndSecurity.yaml"
template2="G_ProfilePage/s3BucketStaticWeb.yaml"
template3="G_ProfilePage/cloudFrontDistribution.yaml"


# Deploy templates
deploy_template $template1 "NetworkStack"
deploy_template $template2 "S3BucketStack"
deploy_template $template3 "CloudFrontStack"
