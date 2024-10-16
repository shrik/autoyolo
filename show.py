import os
import cv2
import matplotlib.pyplot as plt

# imagesdir = "coco8/images/val"
imagesdir = "games/images/val"
imagefiles = os.listdir(imagesdir)
imagefiles.sort()

for imagefile in imagefiles:
    image_path = os.path.join(imagesdir, imagefile)
    image = cv2.imread(image_path)
    with open(imagesdir.replace("images", "labels")+"/"+imagefile.split(".")[0]+".txt") as f:
        cat, x1, y1, w, h = map(float, f.read().split("\n")[0].strip().split(" "))
    x1 = x1 - w/2.0
    y1 = y1 - h/2.0
    x2 = x1 + w
    y2 = y1 + h
    x1, y1, x2, y2 = int(x1*image.shape[1]), int(y1*image.shape[0]), int(x2*image.shape[1]), int(y2*image.shape[0])

    newimg = cv2.rectangle(image, (x1,y1), (x2,y2), (255,0,0), 1)
    plt.imshow(newimg)
    plt.show()
    cv2.waitKey(0)
