import glob
import cv2
import numpy as np

image_files = glob.glob("data/images/*.jpg")
image_files.sort()

# Read the first image to get dimensions
first_image = cv2.imread(image_files[0])
height, width, layers = first_image.shape

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('smtennis.mp4', fourcc, 30, (width, height))

for image_file in image_files[0:1800]:
    img = cv2.imread(image_file)
    out.write(img)

out.release()