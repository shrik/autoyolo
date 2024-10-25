import os
import shutil
    
labeldir = "games/labels/taishan6k"
imagedir = "data/taishanimgs"
outputdir = "games/images/taishan6k"

for label_file in os.listdir(labeldir):
    if label_file.endswith(".txt"):
        image_file = label_file.replace(".txt", ".jpg")
        shutil.copy(os.path.join(imagedir, image_file), os.path.join(outputdir, image_file))
