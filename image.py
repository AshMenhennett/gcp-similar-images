import os
import base64
import requests

from PIL import Image
from io import BytesIO

class StoredImage:
    """Provides functionality to store an image in local file system

    Attributes:
        url: Url of Image to download
        file_name: The filename of the downloaded file
        directory: Directory to store the file
    """
    
    url = None
    file_name = None
    directory = None

    def __init__(self, url, directory):
        self.url = url
        self.directory = directory

    def downloadImage(self):
        req = requests.get(self.url)

        if req.status_code > 299:
            return None

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        url_split = self.url.split('/') # guesstimate the filename
        self.file_name = url_split[-1]
        
        content = req.content
        
        image = Image.open(BytesIO(content))
        full_image_path = os.path.join(self.directory, self.file_name)
        full_image_path = full_image_path.split('?')[0] # trim query params from filename
        image.save(full_image_path, format=image.format)

        return { 'fileName': self.file_name, 'directory': self.directory }

    def __str__(self):
        return self.file_name