def get_pos(game, clip, index):
    filepath = f"../../games/labels/train/{game}_{clip}_{'%04d' % int(index)}.txt"  
    content = open(filepath, "r").read().strip().split("\n")
    if len(content) != 1:
        raise ValueError(f"tennis is not 1, {filepath}")
    cls, x, y, w, h = content[0].split(" ")
    return [x, y, w, h]

stroke_data = {}
for line in open("stroke_label.txt", "r").readlines():
    line = line.strip()
    if "#" in line:
        continue
    if line == "":
        continue
    game, clip, index, cls = line.split(",")
    key = f"{game}_{clip}"
    if key not in stroke_data:
        stroke_data[key] = []
    stroke_data[key].append([index, cls])

import os
def list_clip_files(game_clip):
    file_paths = [f"../../games/clips/train/{filep}" for filep in os.listdir("../../games/labels/train/") if filep.startswith(f"{game_clip}_")]
    res = []
    for file_path in file_paths:
        if f"{game_clip}_" not in file_path:
            continue
        res.append(file_path)
    return res

def get_data(game, clip, index):
    x, y, w, h = get_pos(game, clip, index)
    stroke_cls = "unknown"
    for item in stroke_data[f"{game}_{clip}"]:
        if "%04d" % int(item[0]) == index:
            stroke_cls = item[1]
            break
    return game, clip, index, x, y, stroke_cls

for key, value in stroke_data.items():
    clip_files = list_clip_files(key)
    clip_files.sort()
    for filepath in clip_files:
        game, clip, index = filepath.split("/")[-1].split(".txt")[0].split("_")[0:3]
        game, clip, index, x, y, stroke_cls = get_data(game, clip, index)
        print(f"{game},{clip},{index},{x},{y},{stroke_cls}")
