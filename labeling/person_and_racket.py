from ultralytics import YOLO
import os
import glob

model = YOLO("yolov10l.pt")
results = model.predict("../games/images/taishan6k/000005.jpg")
print(results)

def outputs(result, imagename, output_dir):
    filepath = os.path.join(output_dir, imagename).replace(".jpg", ".txt")
    with open(filepath, "w") as f:
        for r in result:
            if r.cls == 0: # person
                f.write(f"{1} {r.x} {r.y} {r.w} {r.h}\n")
            elif r.cls == 38: # racket
                f.write(f"{2} {r.x} {r.y} {r.w} {r.h}\n")


imagefiles = glob.glob("../games/images/taishan6k/*.jpg")
for imagepath in imagefiles:
    imagename = os.path.basename(imagepath)
    results = model.predict(imagepath)
    outputs(results, imagename, "../games/labels/person_and_racket")


