import boto3
import datetime
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='ap-south-1')

    # Get instance ID from the event
    instance_id = event['detail']['instance-id']
    logging.info(f"New instance {instance_id}")

    # Define tags
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    tags = [
        {'Key': 'LaunchDate', 'Value': current_date},
        {'Key': 'Environment', 'Value': 'Test'}
    ]

    # Tag the instance
    ec2_client.create_tags(Resources=[instance_id], Tags=tags)

    # Print a confirmation message
    logging.info(f"Tagged instance {instance_id} with LaunchDate: {current_date} and Environment Tag.")
