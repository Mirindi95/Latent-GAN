import rasterio
from rasterio.enums import Resampling
from rasterio.plot import show
import numpy as np
import matplotlib.pyplot as plt
from rasterio import Affine, MemoryFile
from rasterio.enums import Resampling

with rasterio.open("./../../Images/clipped_05_19_RGB/raw/row_A/05_19_RGB_.tif") as raster:

    # rescale the metadata
   
    height=raster.height
    width=raster.width
    profile = raster.profile

    # resample data to target shape
    data = raster.read(    
            out_shape=(
            raster.count,
            raster.width,
            raster.height),
    )
    transform_old = raster.transform * raster.transform.scale(
        (raster.width / data.shape[-1]),
        (raster.height / data.shape[-2])
    )
    
    pixel_size = (0.0032,-0.0032)
    transform = rasterio.Affine(pixel_size[0], transform_old[1], transform_old[2], transform_old[3], pixel_size[1], transform_old[4])
    
    scaling_width = abs(transform_old[4] / abs(pixel_size[1]))
    scaling_height = abs(transform_old[0] / abs(pixel_size[0]))
    print(int(width * scaling_width), int(height * scaling_height), width, height, scaling_width, scaling_height)

    data_new = raster.read(
        out_shape=(
            raster.count,
            int(width * scaling_width),
            int(height * scaling_height)
        ),
        resampling=Resampling.bilinear
    )
    profile.update(transform=transform, driver='GTiff', height=int(width * scaling_width), width=int(height * scaling_height))

    new_dataset = rasterio.open('./../../Images/clipped_05_19_RGB/raw/row_A/test01.tif','w',**profile
                                
     )
    new_dataset.write(data_new)
    new_dataset.close()