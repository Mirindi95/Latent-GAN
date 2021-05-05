import tifffile as tiff
import numpy as np
from PIL import Image
from crop_images import read_image, find_images
from utils import read_json, write_json
import matplotlib.pyplot as plt
import sys
import os


def concat_patches(patchMap: dict, output_dir: str):
    """Reads patch pairs and save the concatenated version"""
    for index, (patch01, patch02) in enumerate(patchMap.items()):
        patch01_array, patch02_array = get_patch_pair(patch01, patch02)
        concated_patch = np.concatenate((patch02_array, patch01_array), axis=1)
        concated_patch = Image.fromarray(np.uint8(concated_patch))
        save_path = os.path.join(output_dir, get_concat_path(patch01))
        concated_patch.save(save_path)

def find_patch_pairs(input_dir01: str, input_dir02: str, patchMap: dict = {}) -> dict:
    """Returns a dictionary that maps each patch pairs"""
    
    for file, file_path in find_images(input_dir01):
        encoder = get_encoder(file)
        map_pair = get_map(encoder, input_dir02)
        patchMap[file_path] = map_pair
    return patchMap

def get_map(encoder: str, input_dir02: str) -> str:
    """returns the matching patch for encoder"""
    for file, file_path in find_images(input_dir02):
        if get_encoder(file) == encoder: 
            return file_path

def get_encoder(file: str) -> str:
    """
    Returns the index encoding for a patch
    Example: _0_0 = first patch of first image
    """
    return file.split('RGB')[-1].split('.')[0]

def get_patch_pair(patch_path01: str, patch_path02: str) -> tuple:
    """Returns a tuple containing two Image object pairs"""
    return np.array(read_image(patch_path01)), np.array(read_image(patch_path02))

def get_concat_path(patch: str):
    """Returns the save name for the patch pair"""
    return 'patch' + patch.split('/')[-1].split('RGB')[-1].split('.')[0]+'.jpg'


if __name__ == "__main__":
    input_dir01 = sys.argv[1]
    input_dir02 = sys.argv[2]
    output_dir = sys.argv[3]
    patchMap = find_patch_pairs(input_dir01, input_dir02)
    write_json(patchMap, 'patchMap.json')
    concat_patches(patchMap, output_dir)