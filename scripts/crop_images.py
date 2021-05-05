from numpy.core import shape_base
import tifffile as tiff
import numpy as np
import os
from PIL import Image, ImageOps
import sys
#->

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
    image = Image.open(file_path).convert("RGB")
    return image

def crop_image(input_dir: str, output_dir: str) -> None:
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
        image = read_image(file_path).rotate(-44.4)
        bbox = get_bbox(image)
        croped = image.crop(bbox)
        croped.save(save_path)
    
    
def find_images(input_dir: str) -> tuple: 
    """
    Generator function that successively yields the path of an
    image within a given directory.
    
    Arguments:
    ----------
        input_dir: input_directory

    Returns:
    --------
        tuple: file, file_path, save_path    
    """
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        if os.path.isfile(file_path) and ".tif" in file:
            #print("processing image: {}".format(file))
            yield file, file_path
            
            
def get_bbox(image) -> tuple: 
    """
    Computes the bounding box for any non-zero data in the image.
    The bounding box is defined as the first upper left, right, lower, right
    pixel belonging to the non-zero element. 
    
    Arguments:
    ----------
        image: Image
    
    Returns:
    --------
        tuple: containing the bbox coordinates
    """
    width, height = image.size
    pixel_true = set() 
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x,y))
            if pixel != (0, 0, 0):
                pixel_true.add((x,y))
    return (min(pixel_true, key=lambda x:x[0])[0], min(pixel_true, key= lambda y:y[1])[1], 
            max(pixel_true, key=lambda x:x[0])[0], max(pixel_true, key= lambda y:y[1])[1])


if __name__ == "__main__":
    
    input_dir = sys.argv[1] #input folder with raw and uncropped images
    output_dir = sys.argv[2] #output folder for cropped images
    crop_image(input_dir, output_dir)