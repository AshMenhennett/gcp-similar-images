import io 
import os
import uuid
import requests

from PIL import Image
from image import StoredImage
from google.cloud import vision
from google.cloud.vision import types
from flask import Flask, send_file, request, jsonify

gcp_client = vision.ImageAnnotatorClient()

app = Flask(__name__)

WD = os.getcwd()
TMP_DIR = os.path.join(WD, 'tmp')

@app.route('/croppedImages', methods=['POST'])
def create_cropped_face():
    request_image = request.files.get('image')
    request_image_o = Image.open(request_image.stream)

    image_file_id = uuid.uuid4().hex

    request_image_bytes = io.BytesIO()
    request_image_format = request_image_o.format
    request_image_o.save(request_image_bytes, format=request_image_format)

    vision_image = types.Image(content=request_image_bytes.getvalue())
    response = gcp_client.face_detection(image=vision_image)

    vertices_to_crop = response.face_annotations[0].bounding_poly.vertices

    vertices_t = (vertices_to_crop[0].x, 
                    vertices_to_crop[0].y, 
                        vertices_to_crop[2].x, 
                            vertices_to_crop[2].y)

    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    cropped_image = request_image_o.crop(vertices_t)
    cropped_image_file_name = image_file_id + '.' + request_image_format.lower()
    cropped_image_file_path = os.path.join(TMP_DIR, cropped_image_file_name)
    cropped_image.save(cropped_image_file_path, format=request_image_format)

    return jsonify({ 'croppedFilePath' :  TMP_DIR + '/' + cropped_image_file_name }), 201
    

@app.route('/croppedImages/similar', methods=['POST'])
def create_similar_faces():

    cropped_image_file_name = request.args.get('croppedImageFileName') # TODO should only pass file id, which would be stored in cache with filename value
    cropped_image_file_path = os.path.join(TMP_DIR, cropped_image_file_name)
    similar_image_o = Image.open(cropped_image_file_path)

    similar_image_bytes = io.BytesIO()
    similar_image_format = similar_image_o.format
    similar_image_o.save(similar_image_bytes, format=similar_image_format)

    vision_image = types.Image(content=similar_image_bytes.getvalue())
    response = gcp_client.web_detection(image=vision_image)

    web_detection = response.web_detection

    images = web_detection.visually_similar_images

    cropped_file_id = cropped_image_file_name.split('.')[0]
    similar_images_directory = os.path.join(TMP_DIR, cropped_file_id)

    image_name_list = []
    for image in images:
        stored_image = StoredImage(image.url, similar_images_directory)
        created_file = stored_image.downloadImage()
        created_file and image_name_list.append(created_file)

    return jsonify({'recordsSize': len(image_name_list), 'directory': TMP_DIR + '/' + cropped_file_id + '/' }), 201

app.run(debug=True)