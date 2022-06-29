import cv2
import socket
import numpy as np
from urllib.request import Request, urlopen
import os
from PIL import Image
from keras.applications.resnet import preprocess_input


def download_image(img_url_dict):
    img_url = img_url_dict['path']
    articleId = img_url_dict['articleId']
    timeout = 20
    socket.setdefaulttimeout(timeout)

    req = Request(img_url,
                  headers={'User-Agent': 'Mozilla/5.0 Windows NT 6.1; WOW64; rv:12.0 Gecko/20100101 Firefox/12.0'})
    with urlopen(req) as response:
        img_bytes = response.read()
        arr = np.asarray(bytearray(img_bytes), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)

        return {'articleId': articleId, 'image': img}


def get_image(img_url_dict):
    try:
        return download_image(img_url_dict)
    except:
        path = os.path.join(os.path.abspath(r'ImagePreprocessing'), 'MissingImages')
        image_path = os.path.join(path, img_url_dict['path'].split('/')[-1].replace('?', '_')) + '.jpg'
        image = Image.open(image_path).convert('RGB')
        image = np.array(image)[:, :, ::-1].copy()

        return {'articleId': img_url_dict['articleId'], 'image': image}


def preprocess_image(image_dict):
    articleId = image_dict['articleId']
    img = image_dict['image']
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

    img = img.reshape((1,) + img.shape)
    img = preprocess_input(img)

    return {'articleId': articleId, 'image': img}


def get_and_preprocess_image(img_url_dict):
    image_dict = get_image(img_url_dict)
    image_dict = preprocess_image(image_dict)
    return image_dict
