import boto3
import pprint

ec2 = boto3.client('ec2')

instance = ec2.describe_instances(
    Filters=[
        {
            "Name": 'instance-state-name',
            "Values": ['running']
        }
    ]
).get('Reservations')


instanceids = []
for thing in instance:
    for obj in thing['Instances']:
        instanceids.append(obj['InstanceId'])


ec2.stop_instances(InstanceIds=instanceids)
print("EC2 Instances have been stopped!")
