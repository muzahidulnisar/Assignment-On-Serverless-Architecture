import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    #describe_ec2_instance = ec2.describe_instances()
    #logger.info(f"describe ec2 instance: {describe_ec2_instance}")

    # Find an EC2 instance with the Auto-Stop tag
    stop_ec2_instance = ec2.describe_instances(
        Filters=[{'Name': 'tag:Auto-Stop', 'Values': ['Auto-Stop']}]
    )
    logger.info(f"Stop ec2 instance: {stop_ec2_instance}")

    # Stop EC2 instance with the Auto-Stop tag
    for res_value in stop_ec2_instance['Reservations']:
        for instance in res_value['Instances']:
            instance_id = instance['InstanceId']
            ec2.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Stopped instance: {instance_id}")

    # Find an EC2 instances with the Auto-Start tag
    start_ec2_instance = ec2.describe_instances(
        Filters=[{'Name': 'tag:Auto-Start', 'Values': ['Auto-Start']}]
    )
    logger.info(f"Stop ec2 instance: {start_ec2_instance}")

    # Stat EC2 instance with the Auto-Start tag
    for res_value in start_ec2_instance['Reservations']:
        for instance in res_value['Instances']:
            instance_id = instance['InstanceId']
            ec2.start_instances(InstanceIds=[instance_id])
            logger.info(f"Started instance: {instance_id}")

