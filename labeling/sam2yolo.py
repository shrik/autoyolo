
input_dir = "../games/zoom/images/train"
output_dir = "../games/zoom/yolo"
import sys

input_dir = sys.argv[1]
output_dir = sys.argv[2]

import json
import shutil
import os

for json_file in os.listdir(input_dir):
    if json_file.endswith('.json'):
        with open(os.path.join(input_dir, json_file), 'r') as f:
            data = json.load(f)
        if "shapes" in data and len(data["shapes"]) > 0:
            # Copy image to output_dir/images/taisha6k
            image_file = json_file.replace('.json', '.jpg')
            # Save the result to a YOLO-style text file
            folder_name = input_dir.split("/")[-1]
            # create folder if not exists
            os.makedirs(os.path.join(output_dir, 'labels', folder_name), exist_ok=True)
            os.makedirs(os.path.join(output_dir, 'images', folder_name), exist_ok=True)

            shutil.copy(os.path.join(input_dir, image_file), os.path.join(output_dir, 'images', folder_name))
            # Process the json file
            image_width = data["imageWidth"]
            image_height = data["imageHeight"]
            yolo_output = []
            for shape in data["shapes"]:
                label = shape["label"]
                points = shape["points"]
                # Find the minimized rectangle to represent tennis
                min_x = min(point[0] for point in points) / image_width
                max_x = max(point[0] for point in points) / image_width
                min_y = min(point[1] for point in points) / image_height
                max_y = max(point[1] for point in points) / image_height
                # Convert to YOLO classifier style label
                x_center = (min_x + max_x) / 2
                y_center = (min_y + max_y) / 2
                width = max_x - min_x
                height = max_y - min_y
                # Assuming class_id for tennis is 0 (as per the context provided)
                class_id = 0
                yolo_label = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
                yolo_output.append(yolo_label)
            
            
            output_file = os.path.join(output_dir, 'labels', folder_name, image_file.replace('.jpg', '.txt'))
            with open(output_file, "w") as f:
                f.write("\n".join(yolo_output))
            print(f"Processed {json_file} and saved the result to {output_file}")

