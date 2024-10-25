import pandas as pd
import cv2
positions = []
for line in open("tmp.txt", "r").readlines():
    filepath = line.strip()
    content = open(filepath, "r").read().strip().split("\n")
    if len(content) != 1:
        print("Error: ", filepath)
        continue
    game, clip, index = filepath.split("/")[-1].split(".")[0].split("_")
    for l in content:
        cls, x, y, w, h = l.split(" ")
        # positions.append(f"{game},{clip},{int(index)},{cls},{x},{y},{w},{h}")
        positions.append([game, clip, int(index), cls, x, y, w, h])

# print("\n".join([",".join(p) for p in positions]))




if __name__ == "__main__":
    def to_pos_data(position):
        game, clip, index, cls, x, y, w, h = position
        x, y, w, h = 1280 * float(x), 720 * float(y), 1280 * float(w), 720 * float(h)
        x1, y1 = x - w / 2, y - h / 2
        x2, y2 = x + w / 2, y + h / 2
        return [x1, y1, x2, y2]
    
    tmp_positions  = [to_pos_data(position) for position in positions]
    res = []

    for index in res:
        game, clip, index, cls, x, y, w, h = positions[index]
        img_path = f"../../games/images/train/{game}_{clip}_{index:04d}.jpg"
        print(img_path)
        cv2.imshow("frame", cv2.imread(img_path))
        cv2.waitKey(0)
