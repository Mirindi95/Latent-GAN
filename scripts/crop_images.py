import tifffile as tiff
import numpy as np
import os
from PIL import Image
import sys
import math
import time
import pyximport
#pyximport.install()
#from iterate import getbox

def crop_images(input_dir: str, output_dir: str, resample_dict = None) -> None:
    """
    Crops an image by a bounding box. 
    
    Arguments:
    ----------
        input_dir: input directory
        output_dir: output_directory
    
    Returns:
    --------
        None        
    """
    
    for file, file_path in find_images(input_dir):
        save_path = os.path.join(output_dir, file)
        image = read_image(file_path)
        if resample_dict is not None:
            image = resize_image(image, resample_dict, file)
        cropped = crop(image)
        cropped.save(save_path)


def read_image(file_path: str) -> Image:
    """
    Reads and rotates a tiff image and returns it as numpy array. 
    
    Arguments:
    ----------
        file_path: path of image file 
    
    Returns:
    --------
        Image
    """
    try:
        return Image.open(file_path).convert("RGB")
    except: raise Exception("unable to read tif file.")
    

    
def find_images(input_dir: str) -> tuple: 
    """
    Generator function that successively yields the path of an
    image within a given directory.
    
    Arguments:
    ----------
        input_dir: input_directory

    Returns:
    --------
        tuple: file, file_path
    """
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path) and ".tif" in file:
            print("processing image: {}".format(file))
            yield file, file_path


def crop(image: Image) -> Image:
    """
    Rotates and cropps an image by a bounding box. 
    
    Arguments:
    ----------
        image: Image
    
    Returns:
    --------
        rotated and cropped Image        
    """
    angle = rotation_angle(image)
    image = image.rotate(-angle)
    width , height = image.size
    t = time.time()
    bbox = getbox(image, width, height)
    print(time.time() - t)
    return image.crop(bbox)


def resize_image(image: Image, resample_dict: dict, file: str) -> Image:
    """
    Resize image to its predecessor.
    Arguments:
    ----------
        image: Image
        resample_dict: dict
        file: str
    
    Returns:
    --------
        resized image        
    """
    encoder = get_encoder(file)
    resample_size = resample_dict[encoder]
    return image.resize(resample_size)

            
def map_sample_size(input_dir: str) -> dict:
    """
    Maps time start point to image sample size with
    image identifier as key and sample size as value

    Arguments:
    ----------
        input_dir: input directory
    
    Returns:
    --------
        dictionary of start image and sample size
    """ 
    resample_dict = {}
    for file, file_path in find_images(input_dir):
        encoder = get_encoder(file)
        image = read_image(file_path)
        resample_dict[encoder] = image.size
    return resample_dict


def getbox(image, width, height): 

    pixel_true = []
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x,y))
            if pixel != (0, 0, 0):
                pixel_true.append((x,y))
    return (min(pixel_true, key=lambda x:x[0])[0], min(pixel_true, key= lambda y:y[1])[1], 
            max(pixel_true, key=lambda x:x[0])[0], max(pixel_true, key= lambda y:y[1])[1])



def rotation_angle(image: Image) -> float:
    """
    Calculates the roattion angle of the image to get cropped image.
    Rotation angle is calculated based on the lower triangle formed by the image.
    
    Arguments:
    ----------
        image: Image
    
    Returns:
    --------
        rotation angle 
    """
    ankathete, gegenkathete = get_triangle(image)
    tan_alpha = ( ankathete / gegenkathete )
    return 90 - math.degrees(math.atan(tan_alpha))   


def get_triangle(image: Image) -> tuple:
    """
    Returns three image coordinates that form a triangle to calculate the rotation angle.
    
    Arguments:
    ----------
        image: Image
    
    Returns:
    --------
        tuple of coordinates
        
    """

    width , height = image.size 
    x_border = walkboarder(image, width, height-1, swap= False)
    y_border = walkboarder(image, height, width-1, swap=True)
    ankathete = width - x_border[0]
    gegenkathete = height - y_border[1]
    return ankathete, gegenkathete


def walkboarder(image: Image, border: int, j : int, swap: False) -> tuple:
    """
    Walks the border of an image to return the non-zero pixel
    
    Arguments:
    ---------
        image: Image
        border: border pixels
        j: width or height of image
        swap: swap pixels and border
    
    Returns:
    --------
        non-zero pixel coordinate
    
    """
    pixel_true = set()
    tmp = j
    for temp in range(j):
        for i in range(border):
            j = (tmp - temp)
            if swap: 
                i, j = swap_values(i, j)
            pixel = image.getpixel((i, j))
            if pixel != (0, 0, 0):
                return i,j


def swap_values(x: int, y: int) -> tuple:
    """ Returns swap values """
    temp = x
    x = y
    y = temp 
    return x, y


def get_encoder(file: str) -> str:
    """
    Returns the index encoding for a patch
    Example: _0_0 = first patch of first image
    """
    return file.split('RGB')[-1].split('.')[0]

    
    