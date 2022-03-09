import boto3

'''
This script creates two EC2 instances with a key pair
'''

def create_key_pairs():
    connection = boto3.client('ec2',region_name='us-east-1')
    '''
    The private key can be accessed by using: KeyName['KeyMaterial'] since create_key_pair() returns a dictionary.
    '''
    key_pair = connection.create_key_pair(
        KeyName='TestKey'
    )


create_key_pairs()
ec2 = boto3.client('ec2', region_name='us-east-1')
instance = ec2.run_instances(
    ImageId='ami-01b20f5ea962e3fe7',
    MinCount=1,
    MaxCount=2,
    KeyName='TestKey'
)

print("You're EC2 instances have been launched successfully!")

