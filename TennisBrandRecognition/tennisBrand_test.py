import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor

'''
This file is meant to test the recognition model with a given image from the tennispics S3 bucket and 
outputs the brands recognized and the confidence amount associated with it.
'''


def show_faces(photo, bucket, response):
    client = boto3.client('rekognition')

    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # calculate and display bounding boxes for each detected face
    print('Detected faces for ' + photo)
    for faceDetail in response['CustomLabels']:

        box = faceDetail['Geometry']
        thing = box['BoundingBox']
        left = imgWidth * thing['Left']
        top = imgHeight * thing['Top']
        width = imgWidth * thing['Width']
        height = imgHeight * thing['Height']

        print('Left: ' + '{0:.0f}'.format(left))
        print('Top: ' + '{0:.0f}'.format(top))
        print('Face Width: ' + "{0:.0f}".format(width))
        print('Face Height: ' + "{0:.0f}".format(height))

        points = (
        (left, top),
        (left + width, top),
        (left + width, top + height),
        (left, top + height),
        (left, top)

        )
        draw.line(points, fill='#00d400', width=2)

        # Alternatively can draw rectangle. However you can't set line width.
        # draw.rectangle([left,top, left + width, top + height], outline='#00d400')

    image.show()

    return len(response['CustomLabels'])


def main():
    client = boto3.client('rekognition')

    modelarn = 'arn:aws:rekognition:us-east-1:789312782184:project/TennisBrands/version/TennisBrands.2022-03-13T20.16.22/1647216981369'

    response = client.detect_custom_labels(
        ProjectVersionArn=modelarn,
        Image={
            'S3Object': {
                'Bucket': 'tennispics',
                'Name': 'fedtest2.jpg'
            }
        },
        MinConfidence=65
    )

    # im = Image.open(r'C:\Users\Aaron\Pictures\fedtest2.jpg')
    # im.show()

    print(response)
    for data in response['CustomLabels']:
        print(data['Name'])
        print(data['Confidence'])
        print(data['Geometry'])



    bucket = "tennispics"
    photo = "fedtest2.jpg"

    faces_count = show_faces(photo, bucket, response)
    print("faces detected: " + str(faces_count))


if __name__ == "__main__":
    main()



