import sys
import os
import glob
import cv2
import shutil
# This script takes three command line arguments: the directory containing images, the directory containing labels, and the directory to move files to.
image_dir = sys.argv[1]
label_dir = sys.argv[2]
result_dir = sys.argv[3]

output_label_dir = os.path.join(result_dir, "labels")
output_image_dir = os.path.join(result_dir, "images")
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

# This function logs an action taken on an image file to a log file.
def log_action(action, image_path):
    with open("logs.txt", "a") as log_file:
        log_file.write(f"{action}: {image_path}\n")

# This function displays an image with its labels and waits for user input.
def image_label_show(image_path, label_path):
    image = cv2.imread(image_path)
    im_w, im_h = image.shape[1], image.shape[0]
    # add text to image
    cv2.putText(image, os.path.basename(image_path), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    for line in open(label_path, 'r').readlines():
        _, x, y, w, h = line.split()
        x = float(x) * im_w
        y = float(y) * im_h
        w = float(w) * im_w
        h = float(h) * im_h
        cv2.rectangle(image, (int(x-w/2), int(y-h/2)), (int(x+w/2), int(y+h/2)), (0, 0, 255), 1)    
    cv2.imshow("Image", image)

# This is the main loop of the script. It iterates over each image and its corresponding label file.
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1920, 1080)
index = 0
actions = []
while index < len(image_files):
    image_path = image_files[index]
    label_path = os.path.join(label_dir, os.path.basename(image_path).replace(".jpg", ".txt"))
    if not os.path.exists(label_path):
        index += 1
        continue  # Skip if the label file does not exist.
    image_label_show(image_path, label_path)
    
    key = cv2.waitKey(0)
    while key not in [ord('y'), ord('d'), ord('q'), ord('n'), ord('b')]:
        key = cv2.waitKey(0)
    if key == ord('y'):
        log_action("Continue", image_path)  # Log the action if 'y' is pressed.
        cp_valid_file(image_path, label_path)
        actions.append(('y', image_path, label_path))
        index += 1
    elif key == ord('n'):
        log_action("Next", image_path)  # Log the action.
        actions.append(('n', image_path, label_path))
        index += 1
    elif key == ord('d'):
        log_action("Deleted", image_path)  # Log the action.
        actions.append(('d', image_path, label_path))
        index += 1
    # elif key == ord('b'):
    #     if actions:
    #         last_action, last_image, last_label = actions.pop()
    #         log_action("Reverted", last_image)
    #         if last_action == 'y':
    #             os.remove(os.path.join(output_image_dir, os.path.basename(last_image)))
    #             os.remove(os.path.join(output_label_dir, os.path.basename(last_label)))
    #         index -= 1
    elif key == ord('q'):
        break  # Exit the loop if 'q' is pressed.

cv2.destroyAllWindows()
