import boto3

'''
This file is meant to test the recognition model with a given image from the tennispics S3 bucket and 
outputs the brands recognized and the confidence amount associated with it.
'''

client = boto3.client('rekognition')

modelarn = 'arn:aws:rekognition:us-east-1:789312782184:project/TennisBrands/version/TennisBrands.2022-03-12T19.13.38/1647130418261'

response = client.detect_custom_labels(
    ProjectVersionArn=modelarn,
    Image={
        'S3Object': {
            'Bucket': 'tennispics',
            'Name': 'fedtest2.jpg'
        }
    }
)

print(response)
for data in response['CustomLabels']:
    print(data['Name'])
    print(data['Confidence'])

