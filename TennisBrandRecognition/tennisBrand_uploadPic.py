import boto3

s3 = boto3.client('s3', region_name='us-east-1')
s3resource = boto3.resource('s3', region_name='us-east-1')


def create_bucket():
    bucket = s3.create_bucket(
        Bucket='tennispics',
)


def upload_sample_images():
    s3 = boto3.resource('s3',region_name='us-east-1')
    file = s3.meta.client.upload_file('C:/Users/Aaron/Pictures/fedtest2.jpg', 'tennispics', 'fedtest2.jpg')



create_bucket()
upload_sample_images()