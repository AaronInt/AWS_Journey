import boto3
import pprint

client = boto3.client('ec2')

instance = client.describe_instances(
    Filters=[
        {
            "Name": 'instance-state-name',
            "Values": ['stopped']
        }
    ]
).get('Reservations')

instance_ids=[]

for thing in instance:
    for obj in thing['Instances']:
        instance_ids.append(obj['InstanceId'])


client.start_instances(InstanceIds=instance_ids)
print('Stopped EC2 instances have now been started!')