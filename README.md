## GCP Vision API Similar Image Search (Demo)

Simple interaction with GCP Vision API to obtain images of people that look similar to a given person.

The aim of this project is to simply display some of the capabilities of the GCP Vision API

This achieved by standing up a Flask API and making two API calls.
1. The first call is made to upload an image of a Person and crop the face of the person, storing the cropped image on the file system.
2. The second call is to download matching images of the cropped facial image to the file system.

### Install Dependencies
TODO

### Set GCP Client Credentials
Be sure to create an account with GCP and obtain your credentials in JSON format and add them to your Terminal session:
```export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json```

### Run the Application
```python3 api.py```

### Upload Image to Crop
Request:
```
POST /croppedImages HTTP/1.1
Host: 127.0.0.1:5000
Cache-Control: no-cache
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="image"; filename="billgates.jpg"
Content-Type: image/jpeg


------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

Response:
```
{
    "basePath": "/Users/someuser/projects/gcp-similar-images/tmp",
    "filename": "e4de332c19fc4b27afaa67fc0129ad4c.jpeg"
}
```

### Download Matching Images
Request:
```
POST /croppedImages/similar?croppedImageFileName=e4de332c19fc4b27afaa67fc0129ad4c.jpeg HTTP/1.1
Host: 127.0.0.1:5000
Cache-Control: no-cache
```

Response:
```
{
    "basePath": "/Users/someuser/projects/gcp-similar-images/tmp",
    "imageDirectory": "e4de332c19fc4b27afaa67fc0129ad4c",
    "recordsSize": 7
}
```

All matching images that the GCP Vision API found will be located at `response.basePath/response.imageDirectory` 