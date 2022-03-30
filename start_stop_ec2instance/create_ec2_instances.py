import boto3
import pprint

# This script creates two EC2 instances if there is no existing key pair with the same key name
ec2 = boto3.resource('ec2', region_name='us-east-1')
client = boto3.client('ec2')

# pprint.pprint(test)


def create_new_keypair():
    new_keypair = 'testKey_2'

    test = client.describe_key_pairs()

    for pair in test['KeyPairs']:
        if pair['KeyName'] == new_keypair:
            return False

    client.create_key_pair(
        KeyName=new_keypair
    )

    return new_keypair


new_key = create_new_keypair()

if new_key:
    ec2.create_instances(
        ImageId='ami-0c02fb55956c7d316',
        MinCount=1,
        MaxCount=2,
        KeyName=new_key
    )
    print('EC2 Instances have successfully been created!')
else:
    print('There is already an existing key associated with another instance...did not make a new instance!')





