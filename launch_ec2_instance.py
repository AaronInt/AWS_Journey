import boto3

'''
A simple script to launch an EC2 instance.
You must pass in the ImageId (AMI ID), Max and Min Count (specifies how many instances to launch) to create an instance.
'''
ec2 = boto3.resource('ec2')

ec2.create_instances(
    ImageId='ami-0c293f3f676ec4f90',
    MaxCount=1,
    MinCount=1
)

print('Your EC2 instance has been launched successfully!')