# {"class": 0.0, "box": [0.4661724865436554, 0.11323930323123932, 0.011972046457231045, 0.02178165875375271], "conf": 0.6507109999656677}

import json
import os
import sys
INPUT_DIR = sys.argv[1] 
# INPUT_DIR = "games/zoom/images/taishan6k_labels/"
OUTPUT_DIR = os.path.join(INPUT_DIR, "yolo")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_output_file_path(json_file, output_dir):
    json_file_name = os.path.basename(json_file).split("/")[-1]
    return output_dir + "/" + json_file_name.replace(".json", ".txt")

def json2yolo(json_file, output_dir):
    data = []
    for line in open(json_file, 'r').readlines():
        data.append(json.loads(line))
    with open(get_output_file_path(json_file, output_dir), "w") as f:
        for item in data:
            f.write(f"{int(item['class'])} {item['box'][0]} {item['box'][1]} {item['box'][2]} {item['box'][3]}\n")

for json_file in os.listdir(INPUT_DIR):
    if json_file.endswith('.txt'):
        json2yolo(os.path.join(INPUT_DIR, json_file), OUTPUT_DIR)


