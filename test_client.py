import numpy as np
from imageio.v3 import imread
from pathlib import Path
import socket
import pickle

HOST = "127.0.0.1"
PORT = 6969

# read frames
frames = []
for file in sorted(Path('frames').iterdir(), reverse=False):
  if not file.is_file():
    continue
  # isolates just the red channel but whatever..
  frame = np.dot(imread(file), [1, 0, 0])
  frames.append(frame)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  # Make a file out of the socket to include EOF markers for pickle
  with s, s.makefile('wb', buffering=0) as w:
    for frame in frames:
      pickle.dump(frame, w)
