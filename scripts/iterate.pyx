from PIL import Image
import time

def getbox(image, int width, int height): 
    cdef int x
    cdef int y 
    cdef list pixel_true = []
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x,y))
            if pixel != (0, 0, 0):
                pixel_true.append((x,y))
    return (min(pixel_true, key=lambda x:x[0])[0], min(pixel_true, key= lambda y:y[1])[1], 
            max(pixel_true, key=lambda x:x[0])[0], max(pixel_true, key= lambda y:y[1])[1])
