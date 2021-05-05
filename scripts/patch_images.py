from crop_images import read_image, find_images
import numpy as np 
import os
import tifffile as tiff
from utils import read_json, write_json, read_file
import sys

HASHMAP_PLOTID = {}

def patch_image(input_dir: str, output_dir: str) -> None:
    """
    Partitions an image into patches and saves them respectively. 
    Patches have are extracted via a kernel of defined size. The kernel traverses
    the image with a defined stride.
    
    Arguments:
    ----------
        input_dir: input directory
        output_dir: output directory
        text_list: list of orthoplot mapping
    
    Returns:
    --------
        None
    """
    for file, file_path in find_images(input_dir):
        image = tiff.imread(file_path)
        image_array = np.array(image)
        save_path = os.path.join(output_dir, file)
        for n_index, patch in enumerate(get_single_patch(image_array)):
            patch_name = get_patch_path(save_path, n_index)
            patch_path = os.path.join(output_dir, patch_name)
            tiff.imsave(patch_path, patch)
            
def get_patch(img: np.array, stride: int = 200, kernel: tuple = (400, 400)) -> np.array:
    """
    Generator function that yields patches of an image with a specific kernel size and stride.
    
    Arguments:
    ----------
        img: image array
        stride: stride
        kernel: kernel 
    
    Returns:
    --------
        image patch
    """

    width, height, _  = img.shape   
    for y in range(0, height, kernel[1]): 
        for x in range(0, width, kernel[0]):
            if x+kernel[1] >= width:
                x = compute_last_pos(x, width, kernel)
                yield img[y:y+kernel[0], x:x+kernel[1]]
            elif y+kernel[1] >= height: 
                y = compute_last_pos(y, height, kernel)
                yield img[y:y+kernel[0], x:x+kernel[0]]
            else:
                yield img[y:y+kernel[0], x:x+kernel[1]]

def get_single_patch(img: np.array, stride: int = 428, kernel: tuple = (470, 470)) -> np.array:
    """
    Generator function that yields patches of an image with a specific kernel size.
    Kernel only moves along x-axis and is centered along y-axis.
    
    Arguments:
    ----------
        img: image array
        stride: stride
        kernel: kernel 
    
    Returns:
    --------
        image patch

    """
    
    height, width, _  = img.shape   
    y = compute_center(height, kernel)
    for x in range(0, width, stride):
        if x+kernel[1] <= width:
            yield img[y:y+kernel[0], x:x+kernel[1]]
        else: 
            print("number of missing pixels: {}".format(width-x))

def compute_last_pos(pos: int, boarder: int, kernel: tuple) -> int: 
    """Computes the last possible patch position"""
    return pos - (kernel[0] - (boarder - pos))

def compute_center(height: int, kernel: tuple) -> int : 
    """
    Number of pixels that should be shifted down to set the kernel into the middel.
    
    Arguments:
    ----------
        height: height of image
        kernel: kernel
    
    Returns:
    --------
        int
    
    """
    return (height // 2) - (kernel[0]//2)

def get_file_index(file: str) -> int:
    """Returns the index of the image"""
    return int(file.split('_')[-1].split('.')[0])

def get_patch_path(save_path: str, index: int) -> str:
    """output path for patch"""
    return save_path.split('patched')[-1][1:].split('.')[0]+"_{}.tif".format(index)

if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    patch_image(input_dir=input_dir, output_dir=output_dir)
