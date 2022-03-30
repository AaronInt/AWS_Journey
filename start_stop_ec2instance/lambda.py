import boto3
import pprint


def lambda_handler(event, context):
    ec2 = boto3.client('ec2')

    instance = ec2.describe_instances(
        Filters=[
            {
                "Name": "instance-state-name",
                "Values": ["running"]
            }
        ]
    ).get("Reservations")

    instance_ids = []
    for thing in instance:
        for obj in thing['Instances']:
            instance_ids.append(obj['InstanceId'])


    ec2.stop_instances(InstanceIds=instance_ids)
    print("All running EC2 instances have been stopped")
    # pprint.pprint(instance)


