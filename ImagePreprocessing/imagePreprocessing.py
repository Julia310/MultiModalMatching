import cv2
import socket
import numpy as np
from urllib.request import Request, urlopen
import os
import io
from PIL import Image
from keras.applications.resnet import preprocess_input
from glob import glob

#TODO: Adjust pathing to relative
gerry_web_base_path = r'D:\pythonProject\MultiModalMatching\GerryWeber'
tommy_h_base_path   = r"D:\pythonProject\MultiModalMatching\TommyHilfiger"
zalando_base_path   = r"D:\pythonProject\MultiModalMatching\Zalando"


def download_image(img_url_dict):
    img_url = img_url_dict['url']
    timeout = 20
    socket.setdefaulttimeout(timeout)

    req = Request(img_url,
                  headers={'User-Agent': 'Mozilla/5.0 Windows NT 6.1; WOW64; rv:12.0 Gecko/20100101 Firefox/12.0'})
    with urlopen(req) as response:
        img_bytes = response.read()
        arr = np.asarray(bytearray(img_bytes), dtype=np.uint8)
        save_image_to_file_local(img_bytes, img_url_dict)
        img = cv2.imdecode(arr, -1)
        return {'articleId': img_url_dict['articleId'], 'image': img}


def save_image_to_file_local(img_bytes, img_url_dict):
    image = Image.open(io.BytesIO(img_bytes))

    file_path = os.path.join(get_base_path_by_brand_and_data_source(img_url_dict['brand'], img_url_dict['data_source']), img_url_dict['path'])
    if img_url_dict['brand'] == 'tommy hilfiger' and img_url_dict['data_source'] == 'th_gw':
        file_path = file_path + '.jpeg'
    image.save(file_path)
    print('==>image saved under ' + file_path)


def load_images_from_file_system(img_dict):
    brand = img_dict['brand']
    data_source = img_dict['data_source']
    base_path = get_base_path_by_brand_and_data_source(brand, data_source)

    file_path = os.path.join(base_path, img_dict["path"])
    file_result = glob(file_path + '*')
    if len(file_result) == 0:
        print('File not found - trying to download file : :' + img_dict["path"])
        return download_image(img_dict)
    else:
        file = file_result[0]

        try:
            rgb_image = Image.open(file).convert('RGB')
        except:
            print('local file corrupt - DELETE THIS: ' + file_path)
            print('ignoring file and trying to download')
            return download_image(img_dict)

        np_image = np.array(rgb_image)[:, :, ::-1].copy()
        return {'articleId': img_dict['articleId'], 'image': np_image}


def get_base_path_by_brand_and_data_source(brand, data_source):
    base_path = ""
    if brand == 'gerry weber' and data_source == 'th_gw':
        base_path = gerry_web_base_path
    if brand == 'tommy hilfiger' and data_source == 'th_gw':
        base_path = tommy_h_base_path
    if data_source == 'zal':
        base_path = zalando_base_path
    return base_path


def get_image(img_url_dict, file_system=False):
    if file_system:
        return load_images_from_file_system(img_url_dict)
    return download_image(img_url_dict)


def preprocess_image(image_dict):
    articleId = image_dict['articleId']
    img = image_dict['image']
    img = cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)

    img = img.reshape((1,) + img.shape)
    img = preprocess_input(img)

    return {'articleId': articleId, 'image': img}


def get_and_preprocess_image(img_url_dict):
    image_dict = get_image(img_url_dict, True)
    if not image_dict:
        return image_dict
    return preprocess_image(image_dict)
