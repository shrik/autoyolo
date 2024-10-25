images_dir = "data/taishanimgs_labels/data/images"
labels_dir = "data/taishanimgs_labels/data/labels"

for image_file in os.listdir(images_dir):
    if image_file.endswith(".jpg"):
        label_file = image_file.replace(".jpg", ".txt")
        if not os.path.exists(os.path.join(labels_dir, label_file)):
            print(image_file)
    