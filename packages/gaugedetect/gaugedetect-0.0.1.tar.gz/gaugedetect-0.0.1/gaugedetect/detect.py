import json
import datetime
import requests
import imghdr
import pillow_heif
import PIL
import numpy as np
from PIL import Image
from supabase import create_client, Client
pillow_heif.register_heif_opener()

# For deverlop
import os
from dotenv import load_dotenv
load_dotenv()


API_URL = "https://abc.cv.api.apollo21.asia/api/detect"
def convert_image(filepath, name: str):
    """Convert file if file is .HEIC.
    Args:
        filepath (str): The path to image file.
        name (str): Name of new image file (JPEG).
    """
    if imghdr.what(path) == None:
        image = pillow_heif.read_heif(path)
        image = PIL.Image.frombytes( image.mode, image.size, image.data, "raw")
        image.save(path + ".jpg", format("jpeg"))


def check_image_size(url: str):
    """Check image size from URL
    Args:
        url (str): Image URL
    Return:
        size (int): Image size, width and height
    """
    response = requests.get(url, stream=True)
    img = Image.open(response.raw)
    width, height = img.size
    return int(response.headers.get('Content-Length', 0)), width, height

def compress_image(url: str, max_width: int):
    """ Compress image to lower than 2MB.
    Args:
        url (str): Image URL
        max_width (int): New width size
    Return:
        Image (image): New image for lower than 2MB.
    """
    response = requests.get(url, stream=True)
    img = Image.open(response.raw)
    size, width, height = check_image_size(url)
    aspectratio = width / height
    new_height = max_width / aspectratio
    image = img.resize((max_width, round(new_height)))
    return image



def digital_url(user_id: str, product_key: str, image_url: str, gauge_min: int = 0, gauge_max: int = 0, overlay_top: int = 0, overlay_left: int = 0, overlay_width: int = 0, overlay_height: int = 0, confident: int = 0):
    url_key = os.environ.get('KEY_URL')
    response = requests.request("GET", url_key, headers={'Content-Type': 'application/json'}, data=json.dumps({"user_id": user_id, "product_key": product_key}))
    if response.status_code != 200:
        return ValueError("Your user_id or product_key is invalid.")

    key = response.json()['msg']
    image_size, image_width, image_height = check_image_size(image_url)
    if image_size <= (2*1024*1024):
        data=json.dumps({
            'image_url': image_url,
            'gauge_min': gauge_min,
            'gauge_max': gauge_max,
            'image_width': image_width,
            'image_height': image_height,
            'overlay_top': overlay_top,
            'overlay_left': overlay_left,
            'overlay_width': overlay_width,
            'overlay_height': overlay_height,
            'confident': confident,
            'gauge_shape_type': 'DIGITAL'
        })
        response = requests.request('POST', API_URL, headers={ 'SECRET_KEY': f'{key}', 'Content-Type': 'application/json' }, data=data)
        return response.json()
    else:
        return ValueError('The maximum file size allowed is 2MB.')

def digital_image(user_id: str, product_key: str, image_path: str, gauge_min: int = 0, gauge_max: int = 0, overlay_top: int = 0, overlay_left: int = 0, overlay_width: int = 0, overlay_height: int = 0, confident: int = 0):
    url_key = os.environ.get('KEY_URL')
    response = requests.request("GET", url_key, headers={'Content-Type': 'application/json'}, data=json.dumps({"user_id": user_id, "product_key": product_key}))

    if response.status_code != 200:
        return ValueError("Your user_id or product_key is invalid.")

    key = response.json()['msg']

    try:
        supabase_url: str = os.environ.get('SUPABASE_URL')
        supabase_key: str = os.environ.get('SUPABASE_KEY') 
        supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
    except:
        return ValueError("Sever is unavaliable")
    
    date: str = datetime.datetime.now().strftime('%d-%m-%Y')
    timestamp: str = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
    filename = user_id + '/' + date + '/' + timestamp + '.jpg'
    supabase.storage.from_('images').upload(filename, image_path, {"content-type": "image/*"})
    image_url = supabase.storage.from_('images').get_public_url(filename)

    image_size, image_width, image_height = check_image_size(image_url)
    if image_size <= (2*1024*1024):
        data=json.dumps({
            'image_url': image_url,
            'gauge_min': gauge_min,
            'gauge_max': gauge_max,
            'image_width': image_width,
            'image_height': image_height,
            'overlay_top': overlay_top,
            'overlay_left': overlay_left,
            'overlay_width': overlay_width,
            'overlay_height': overlay_height,
            'confident': confident,
            'gauge_shape_type': 'DIGITAL'
        })
        response = requests.request('POST', API_URL, headers={ 'SECRET_KEY': f'{key}', 'Content-Type': 'application/json' }, data=data)
        return response.json()
    else:
        return ValueError('The maximum file size allowed is 2MB.')


def clock_url(user_id: str, product_key: str, image_url: str, gauge_min: int = 0, gauge_max: int = 100, overlay_top: int = 0, overlay_left: int = 0, overlay_width: int = 0, overlay_height: int = 0):
    url_key = os.environ.get('KEY_URL')
    response = requests.request("GET", url_key, headers={'Content-Type': 'application/json'}, data=json.dumps({"user_id": user_id, "product_key": product_key}))
    
    if response.status_code != 200:
        return ValueError("Your user_id or product_key is invalid.")

    key = response.json()['msg']
    image_size, image_width, image_height = check_image_size(image_url)
    if image_size <= (2*1024*1024):
        data=json.dumps({
            'image_url': image_url,
            "gauge_min": gauge_min,
            "gauge_max": gauge_max,
            "image_width": image_width,
            "image_height": image_height,
            "overlay_top": overlay_top,
            "overlay_left": overlay_left,
            "overlay_width": overlay_width,
            "overlay_height": overlay_height,
            "gauge_shape_type": "DIAL"
        })
        response = requests.request('POST', API_URL, headers={ 'SECRET_KEY': f'{key}', 'Content-Type': 'application/json' }, data=data)
        return response.json()       
    else:
        return ValueError('The maximum file size allowed is 2MB.')

def clock_image(user_id: str, product_key: str, image_path: str, gauge_min: int = 0, gauge_max: int = 100, overlay_top: int = 0, overlay_left: int = 0, overlay_width: int = 0, overlay_height: int = 0):
    url_key = os.environ.get('KEY_URL')
    response = requests.request("GET", url_key, headers={'Content-Type': 'application/json'}, data=json.dumps({"user_id": user_id, "product_key": product_key}))
    
    if response.status_code != 200:
        return ValueError("Your user_id or product_key is invalid.")

    key = response.json()['msg']

    try:
        supabase_url: str = os.environ.get('SUPABASE_URL')
        supabase_key: str = os.environ.get('SUPABASE_KEY') 
        supabase: Client = create_client(supabase_url=supabase_url, supabase_key=supabase_key)
    except:
        return ValueError("Sever is unavaliable")

    date: str = datetime.datetime.now().strftime('%d-%m-%Y')
    timestamp: str = datetime.datetime.now().strftime('%d%m%Y%H%M%S')
    filename = user_id + '/' + date + '/' + timestamp + '.jpg'
    supabase.storage.from_('images').upload(filename, image_path, {"content-type": "image/*"})
    image_url = supabase.storage.from_('images').get_public_url(filename)

    image_size, image_width, image_height = check_image_size(image_url)
    if image_size <= (2*1024*1024):
        data=json.dumps({
            'image_url': image_url,
            "gauge_min": gauge_min,
            "gauge_max": gauge_max,
            "image_width": image_width,
            "image_height": image_height,
            "overlay_top": overlay_top,
            "overlay_left": overlay_left,
            "overlay_width": overlay_width,
            "overlay_height": overlay_height,
            "gauge_shape_type": "DIAL"
        })
        response = requests.request('POST', API_URL, headers={ 'SECRET_KEY': f'{key}', 'Content-Type': 'application/json' }, data=data)
        return response.json()       
    else:
        return ValueError('The maximum file size allowed is 2MB.')