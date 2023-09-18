import numpy as np
from imageio.v3 import imread
import socket
import pickle

class Scroller:
  def __init__(self, charset_path, charset_lookup, host, port, debug=False):
    self.__charset = np.dot(imread(charset_path), [0, 1, 0, 0])
    self.__chars = []
    self.__switch_msg = False
    self.__debug = debug
    self.__charset_lookup = charset_lookup

    for y in range(0, 32, 16):
      for x in range(0, 512, 16):
        char = self.__charset[y : y + 16, x : x + 16]
        self.__chars.append(char)

    self.__update_buffer("Init")

    self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__sock.connect((host, port))
    self.__out = self.__sock.makefile('wb', buffering=0)

  def __del__(self):
    # Clean up :)
    self.__out.close()
    self.__sock.close()

  def __update_buffer(self, message):
    '''Updates the internal message buffer to display a certain message.'''
    self.__offset = 0
    buflen = 16 * (len(message) + 2) # +2 for front and back blanking
    self.__buffer = np.zeros((16, buflen))

    for c, idx in zip(message, range(16, buflen, 16)):
      char = self.__chars[self.__charset_lookup.index(c)]
      self.__buffer[0:16, idx:idx+16] = char

  def pprint_arr(self, arr):
    '''Prints a 2d pixel matrix to the terminal.'''
    for row in arr:
      for pxl in row:
        print("█" if pxl else ".", end="")
      print("")

  def tick(self):
    '''Advances the animation by one frame, switching to next message if needed.'''
    window = self.__buffer[0 : 16, self.__offset : self.__offset + 16]
    if self.__debug:
      self.pprint_arr(window)

    pickle.dump(window, self.__out)

    self.__offset = (self.__offset + 1) % (len(self.__buffer[0]) - 16) # minus last blaking area
    if self.__offset == 0 and self.__switch_msg:
      self.__update_buffer(self.__next_msg)
      self.__switch_msg = False

  def set_message(self, msg):
    '''Sets a new message to be displayed next.'''
    self.__switch_msg = True
    self.__next_msg = msg

charset_path = 'charset.png'
charset_lookup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz°1234567890@'
host = "127.0.0.1"
port = 6969

sc = Scroller(charset_path, charset_lookup, host, port, debug=True)
sc.set_message("peepee")
import time
while True:
 sc.tick()
 time.sleep(0.1)