import json


def find_game_ball(positions):
    for pos in positions:
        if pos["class"] == 0:
            return pos
    return None



class BallPosition:
    def __init__(self, x, y, index, conf=1.0):
        self.x = x
        self.y = y
        self.conf = conf
        self.index = index


class BallTrajectory:
    def __init__(self):
        self.positions = []

    def add_position(self, position):
        self.positions.append(position)


class 

    
for line in open("tennis_pos.json", "r").readlines():
    data = json.loads(line.strip())
    image_path = data["image_path"]
    positions = data["pos"]
    index = data["index"]




