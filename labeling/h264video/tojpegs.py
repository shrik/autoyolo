video_path = "right_tennis.video"
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

fp = open(video_path, "rb")
chunk_size = 1024 * 100
last_frame_bts = b""



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


def timestamp_to_int(timestamp):
    # "2024-11-22 10:00:00.001"
    from datetime import datetime
    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    # Convert to milliseconds since epoch (1970)
    return int(dt.timestamp() * 1000)


frame_timestamp = -1
data_index = 0
while True:
    frame_timestamp, jpeg_bytes = get_frame_and_timestamp(fp)
    if frame_timestamp is None:
        continue
    frame_timestamp = timestamp_to_int(frame_timestamp)
    img = cv2.imdecode(np.frombuffer(jpeg_bytes, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.resize(img, (1280, 720))
    cv2.imwrite(f"right_images/{frame_timestamp}.jpg", img)
   
