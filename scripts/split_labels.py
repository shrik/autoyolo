
import os


def generate_file(filename, x, y):
    with open(f"{output_dir}/{filename}", "w") as f:
        print(filename)
        lx = int(x)/1280.0
        ly = int(y)/720.0
        w = 12/1280.0
        h = 12/720.0
        f.write(f"0 {lx} {ly} {w} {h}")


def rmfile(filename):
    if os.path.exists(filename):
        os.remove(filename)


def split_labels(input_file, output_dir):
    for line in open(input_file, "r").readlines():
        if "jpg" in line:
            # 0001.jpg, 1, 601, 406, 0
            filename, visible, x, y, _ = line.strip().split(",")
            if int(visible) == 0:
                imagepath = output_dir.replace("labels", "images") + "/" + filename
                rmfile(imagepath)
                continue
            generate_file(filename.replace(".jpg", ".txt"), x, y)

input_file = "game1/Clip1/Label.csv"
output_dir = "games/labels/train"
split_labels(input_file, output_dir)

input_file = "game1/Clip2/Label.csv"
output_dir = "games/labels/val"
split_labels(input_file, output_dir)
