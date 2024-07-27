import boto3
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2', region_name='ap-south-1')

    # Specify the volume ID
    volume_id = 'vol-03a1e9a46085c4541'

    # Create a snapshot of the specified EBS volume_id
    snapshot = ec2_client.create_snapshot(
        VolumeId=volume_id,
        Description=f"Snapshot of volume {volume_id} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    snapshot_id = snapshot['SnapshotId']
    logger.info(f"Created snapshot: {snapshot_id}")

    current_time = datetime.datetime.now(datetime.timezone.utc)
    cutoff_time = current_time - datetime.timedelta(days=30)

    # List snapshots for the specified volume and delete those older than 30 days
    snapshots = ec2_client.describe_snapshots(Filters=[{'Name': 'volume-id', 'Values': [volume_id]}])
    logger.info(f"snapshot: {snapshots}")
    for snapshot in snapshots['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        start_time = snapshot['StartTime']
        if start_time < cutoff_time:
            ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            logger.info(f"Deleted snapshot: {snapshot_id}")

    return {
        'statusCode': 200,
        'body': 'Snapshot creation and cleanup process complete'
    }
