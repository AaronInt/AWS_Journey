import boto3

'''
This file will start the model
'''


client = boto3.client('rekognition')

modelarn = 'arn:aws:rekognition:us-east-1:789312782184:project/TennisBrands/version/TennisBrands.2022-03-12T19.13.38/1647130418261'

response = client.start_project_version(ProjectVersionArn=modelarn, MinInferenceUnits=1)
print(response)

