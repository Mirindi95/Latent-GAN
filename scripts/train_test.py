import numpy as np
import os
from sklearn.model_selection import train_test_split
from crop_images import find_images
from shutil import copyfile


def collect_files(input_dirX: str, inpur_dirY: str) -> tuple:
    """
    Collects tif files from directories to split into train and test.
    """
    X = []
    Y = []
    for root in os.listdir(input_dirX):
        input_path = os.path.join(input_dirX, root)
        X.extend([os.path.join(input_path, file) for file in os.listdir(input_path) if ".tif" in file])

    for root in os.listdir(input_dirY):
        input_path = os.path.join(input_dirY, root)
        Y.extend([os.path.join(input_path, file) for file in os.listdir(input_path) if ".tif" in file])
    
    X = sorted(X, key= lambda x: int(x.split("RGB")[-1].split(".")[0].split("_")[-1]))
    Y = sorted(Y, key= lambda x: int(x.split("RGB")[-1].split(".")[0].split("_")[-1]))
    return X, Y

def split_files(input_dirX: str, inpur_dirY: str,  output_dir: str): 

    X, Y = collect_files(input_dirX, inpur_dirY)
    folders = ["X_train", "X_test", "y_train", "y_test"]
    for index, (data) in enumerate(train_test_split(X, Y, test_size=0.12, random_state=30)): 
        output_path = os.path.join(output_dir, folders[index])
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        for file in data:
            filename = get_filename(file)
            outfilepath = os.path.join(output_path, filename)
            copyfile(file, outfilepath)

def get_filename(file: str): 
    """returns image file name"""
    return file.split("\\")[-1]



if __name__ == "__main__": 
    input_dirX = "./../Images/Orthoplots/clipped_04_23_RGB/cropped/"
    input_dirY = "./../Images/Orthoplots/clipped_06_16_RGB/cropped/"
    output_dir = "./../Images/Orthoplots/Training_data/"
    split_files(input_dirX, input_dirY, output_dir)
    print()