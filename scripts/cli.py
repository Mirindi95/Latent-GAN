import click
import os
from crop_images import crop_images, map_sample_size
from patch_images import patch_image

@click.group()
def main():
    """Entry method"""
    pass

@main.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=True))
@click.option("-r", "--resize", type=click.Path(exists=True), help="directory of root image to resize")
def preprocessing(input_dir: str, output_dir: str, resize:bool =True):
    """
    Orthoplots are rotated and cropped. The input directory should list all folders. 
    Rezising is done according to the previous time point given as the parent folder. 
    Images are mapped to its predecessor and rezised accordingly.

    input_directory: 
        clipped_04_34
             |_rowA	
             |_rowB
    

    the Output directory should be empty or with the same folder structure as the input directory
    """
    output_dir = os.path.join(output_dir, "cropped")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for root in os.listdir(input_dir):
        input_path = os.path.join(input_dir, root)
        output_path = os.path.join(output_dir, root)
        if resize is not None and "cropped" not in root: 
                resample_path = os.path.join(resize, root)
                resize = map_sample_size(resample_path)
        if "cropped" not in input_path: 
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            crop_images(input_path, output_path, resize)

@main.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path(exists=True))
def patch(input_dir: str, output_dir: str): 

    patch_path = os.path.join(output_dir, "patched")
    if not os.path.exists(patch_path):
        os.mkdir(patch_path)
    patch_image(input_dir=input_dir, output_dir=patch_path)

if __name__ == "__main__":
    main()
