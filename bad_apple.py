import numpy as np
import LedController
import numpy as np
from imageio.v3 import imread
from pathlib import Path

# pin configuration
CLK_PIN = 29
DATA_PIN = 13
LATCH_PIN = 33
EN_PIN = 32

leds = LedController.Panel(CLK_PIN, DATA_PIN, LATCH_PIN, EN_PIN)

leds.set_brightness(100)

# read frames
frames = []
for file in sorted(Path('bad_apple_frames').iterdir(), key=lambda x: int((x.name)[:-4])):
  if not file.is_file():
    continue
  # isolates just the red channel but whatever..
  frame = np.dot(imread(file), [1, 0, 0])
  frames.append(frame)


for frame in frames:
  leds.display_frame(frame)