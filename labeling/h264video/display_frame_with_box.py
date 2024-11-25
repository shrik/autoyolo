video_path = "tennis.video"
import cv2
import numpy as np
import json

def split_frame_data(frame_bts):
    pos = frame_bts.find("__DATETIME_SEP__".encode("utf-8"))
    if pos == -1:
        return None, None
    if pos !=0 :
        raise Exception("Invalid frame data")

    start_pos = pos + len("__DATETIME_SEP__".encode("utf-8"))
    end_pos = start_pos + 23 + 16
    timestamp = frame_bts[start_pos:end_pos].decode("utf-8")[0:23]
    jpeg_bytes = frame_bts[end_pos:]
    return timestamp, jpeg_bytes

data = [json.loads(line) for line in open("data.json", "r").readlines()]
data = [(item["timestamp"], item["pos"][0]["box"]) for item in data]

fp = open(video_path, "rb")
chunk_size = 1024 * 100
last_frame_bts = b""

import pandas as pd
val = pd.read_csv("val_0.1.csv")


def get_frame_and_timestamp(fp):
    global last_frame_bts
    while True:
        pos = last_frame_bts.find("__FRAME_SEP__".encode("utf-8"))
        if pos == -1:
            bts = fp.read(chunk_size)
            if len(bts) == 0:
                raise Exception("EOF")
            last_frame_bts += bts
        else:
            cur_frame = last_frame_bts[0:pos]
            frame_timestamp, jpeg_bytes = split_frame_data(cur_frame)
            next_frame = last_frame_bts[pos+len("__FRAME_SEP__".encode("utf-8")):]
            last_frame_bts = next_frame
            return frame_timestamp, jpeg_bytes


def display_frame(frame_timestamp, jpeg_bytes, box, land):
        img = cv2.imdecode(np.frombuffer(jpeg_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
        img = cv2.resize(img, (1280, 720))
        cv2.putText(img, str(frame_timestamp), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if land:
            cv2.putText(img, "land", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        x, y = int(box['x']), int(box['y'])
        cv2.rectangle(img, (x-2, y-2), (x+2, y+2), (0, 0, 255), 2)
        cv2.imshow("check", img)
        

def timestamp_to_int(timestamp):
    # "2024-11-22 10:00:00.001"
    from datetime import datetime
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    # Convert to milliseconds since epoch (1970)
    return int(dt.timestamp() * 1000)



def display_recent_frames(recent_frames):
    current_index = len(recent_frames) - 1
    while current_index < len(recent_frames):
        frame_timestamp, jpeg_bytes, box, land = recent_frames[current_index]
        display_frame(frame_timestamp, jpeg_bytes, box, land)
        key = cv2.waitKey(0)
        if key & 0xFF == ord('q'):
            raise Exception("Quit")
        elif key & 0xFF == ord('f'):
            current_index += 1
        elif key & 0xFF == ord('b'):
            current_index -= 1
            if current_index < 0:
                current_index = 0
        else:  # Enter key pressed
            pass


frame_timestamp = -1
data_index = 0
recent_frames = []
while True:
    frame_timestamp, jpeg_bytes = get_frame_and_timestamp(fp)
    if frame_timestamp is None:
        continue
    frame_timestamp = timestamp_to_int(frame_timestamp)
    land = False
    if frame_timestamp in val['timestamp'].values:
        land = True
    box = None
    for i in range(data_index, len(data)):
        if data[i][0] > frame_timestamp:
            break
        if data[i][0] == frame_timestamp:
            box = data[i][1]
            data_index = i
    if box is None:
        print(f"No box for {frame_timestamp}")
        continue
    recent_frames.append((frame_timestamp, jpeg_bytes, box, land))
    if len(recent_frames) > 100:
        recent_frames.pop(0)
    display_recent_frames(recent_frames)
    