import boto3

'''
This file will start the model
'''


client = boto3.client('rekognition')

modelarn = 'arn:aws:rekognition:us-east-1:789312782184:project/TennisBrands/version/TennisBrands.2022-03-13T20.16.22/1647216981369'

response = client.start_project_version(ProjectVersionArn=modelarn, MinInferenceUnits=1)
print(response)

