import pandas as pd

data = pd.read_csv("event.txt", header=None, names=["game", "clip", "index", "x", "y", "event_cls"])
# 
