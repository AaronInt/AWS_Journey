import boto3

'''
A simple script to launch an EC2 instance with SNS to get a notification after each start of an instance.
Will first check to see if there are any running instances, if not, it will launch a new instance.
You must pass in the ImageId (AMI ID), Max and Min Count (specifies how many instances to launch) to create an instance.
'''

ec2 = boto3.client('ec2', region_name='us-east-1')
instances = ec2.describe_instances(
    Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"]
        }
    ]
).get('Reservations')

if not bool(instances):
    sns = boto3.client('sns')
    response = sns.create_sms_sandbox_phone_number(
        PhoneNumber='+17747578486',
        LanguageCode='en-US'
    )
    response2 = sns.publish(
        PhoneNumber='+17747578486',
        Message='An EC2 instance has been launched on your account from the launch_ec2_instance Python script!'
    )
    new_instance = ec2.run_instances(
        ImageId='ami-0e1d30f2c40c4c701',
        MinCount=1,
        MaxCount=1
    )
else:
    print("There is already a running EC2 instance!")