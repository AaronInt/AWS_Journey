import os
import boto3
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        basedir = os.path.abspath(os.path.dirname(__file__))

        file.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        upload_image_to_s3(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename), filename)
        test_model(filename, 'tennispics', filename)
        flash('Image successfully uploaded and displayed below' + os.path.join(basedir, app.config['UPLOAD_FOLDER']))
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def upload_image_to_s3(filepath, filename):
    client = boto3.client('s3', region_name='us-east-1')
    bucket = client.create_bucket(
        Bucket='tennispics'
    )

    resource = boto3.resource('s3', region_name='us-east-1')
    image = resource.meta.client.upload_file(filepath, 'tennispics', filename)


def test_model(filename, bucket, photo):
    client = boto3.client('rekognition')

    modelarn = 'arn:aws:rekognition:us-east-1:789312782184:project/TennisBrands/version/TennisBrands.2022-03-13T20.16.22/1647216981369'

    response = client.detect_custom_labels(
        ProjectVersionArn=modelarn,
        Image={
            'S3Object': {
                'Bucket': 'tennispics',
                'Name': filename
            }
        },
        MinConfidence=65
    )


    print(response)
    for data in response['CustomLabels']:
        print(data['Name'])
        print(data['Confidence'])

    # Load image from S3 bucket
    s3_connection = boto3.resource('s3')
    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)


    for lab in response['CustomLabels']:
        box = lab['Geometry']
        thing = box['BoundingBox']
        left = imgWidth * thing['Left']
        top = imgHeight * thing['Top']
        width = imgWidth * thing['Width']
        height = imgHeight * thing['Height']

        points = (
            (left, top),
            (left + width, top),
            (left + width, top + height),
            (left, top + height),
            (left, top)

        )
        draw.line(points, fill='#00d400', width=2)

    image.show()

    return len(response['CustomLabels'])


if __name__ == "__main__":
    app.run()