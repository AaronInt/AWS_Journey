import boto3

'''
This script will check for any running EC2 instances and 
'''


def terminate_ec2_instances(instanceid):
    connection = boto3.client('ec2', region_name='us-east-1')
    trash = connection.terminate_instances(
        InstanceIds=instanceid
    )


ec2 = boto3.client('ec2', region_name='us-east-1')
description = ec2.describe_instances(
    Filters=[
        {
            "Name": 'instance-state-name',
            "Values": ['running']
        }
    ]).get("Reservations")

instanceId = []
for obj in description:
    for thing in obj['Instances']:
        instanceId.append(thing['InstanceId'])
        print(f"The Instance with an ID of: {instanceId}, has been terminated")

terminate_ec2_instances(instanceId)

