import sys
import os
import glob
import cv2
import shutil
import json
# This script takes three command line arguments: the directory containing images, the directory containing labels, and the directory to move files to.
image_dir = sys.argv[1]
label_dir = sys.argv[2]
result_dir = sys.argv[3]

folder_name = image_dir.split("/")[-1]
output_label_dir = os.path.join(result_dir, "labels", folder_name)
output_image_dir = os.path.join(result_dir, "images", folder_name)
os.makedirs(output_label_dir, exist_ok=True)
os.makedirs(output_image_dir, exist_ok=True)

# This line finds all .jpg files in the image directory.
image_files = glob.glob(os.path.join(image_dir, '*.jpg'))   
# This line finds all .txt files in the label directory.
label_files = glob.glob(os.path.join(label_dir, '*.txt'))
image_files.sort()
label_files.sort()

def cp_valid_file(image_path, label_path):
    shutil.copy(image_path, os.path.join(output_image_dir, os.path.basename(image_path)))
    shutil.copy(label_path, os.path.join(output_label_dir, os.path.basename(label_path)))

def rm_copied_file(image_path, label_path):
    if os.path.exists(os.path.join(output_image_dir, os.path.basename(image_path))):
        os.remove(os.path.join(output_image_dir, os.path.basename(image_path)))
    if os.path.exists(os.path.join(output_label_dir, os.path.basename(label_path))):
        os.remove(os.path.join(output_label_dir, os.path.basename(label_path)))

# This function logs an action taken on an image file to a log file.
def log_action(action, image_path):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"{action}: {image_path}\n")

# This function displays an image with its labels and waits for user input.
def image_label_show(image_path, label_path):
    discard_tag = label_path + ".discard"
    image = cv2.imread(image_path)
    im_w, im_h = image.shape[1], image.shape[0]
    cv2.putText(image, os.path.basename(image_path), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if os.path.exists(discard_tag):
        cv2.putText(image, "Discarded", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    else:
        # add text to image
        for line in open(label_path, 'r').readlines():
            d = json.loads(line.strip())
            x, y, w, h = d["box"]
            x = float(x) * im_w
            y = float(y) * im_h
            w = float(w) * im_w
            h = float(h) * im_h
            cv2.rectangle(image, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), (0, 0, 255), 1)    
        if os.path.exists(os.path.join(output_image_dir, os.path.basename(image_path))):
            cv2.putText(image, "Accepted", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Image", image)


def display_recent_frames(recent_frames):
    current_index = len(recent_frames) - 1
    while current_index < len(recent_frames):
        image_path, label_path = recent_frames[current_index]
        image_label_show(image_path, label_path)
        key = cv2.waitKey(0)
        if key == ord('y'): # accept the image
            discard_tag = label_path + ".discard"
            if os.path.exists(discard_tag):
                os.remove(discard_tag)
            cp_valid_file(image_path, label_path)
            current_index += 1
        elif key == ord('n'): # next image
            current_index += 1
        elif key == ord('d'): # discard the image
            open(label_path + ".discard", 'a').close()
            rm_copied_file(image_path, label_path)
        elif key == ord('s'): # save for mannual check
            # TODO: save the image and label to a new folder
            current_index += 1
        elif key == ord('b'):    # back to previous image
            current_index -= 1
            if current_index < 0:
                current_index = 0
        elif key == ord('q'):
            raise Exception("Quit")

recent_frames = []
index = 0
while index < len(image_files):
    image_path = image_files[index]
    label_path = os.path.join(label_dir, os.path.basename(image_path).replace(".jpg", ".txt"))
    if not os.path.exists(label_path):
        index += 1
        continue  # Skip if the label file does not exist.
    recent_frames.append((image_path, label_path))
    if len(recent_frames) > 100:
        recent_frames.pop(0)
    display_recent_frames(recent_frames)
    index += 1



# y : keep
# n : next
# d : discard
# b : back to previous
# q : quit