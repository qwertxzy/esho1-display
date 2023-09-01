import socket
import numpy as np
import LedController
import pickle

# pin configuration
CLK_PIN = 29
DATA_PIN = 13
LATCH_PIN = 33
EN_PIN = 32

# socket configuration
HOST = "127.0.0.1"
PORT = 6969

leds = LedController.Panel(CLK_PIN, DATA_PIN, LATCH_PIN, EN_PIN)

leds.clear_screen()
leds.set_brightness(100)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  print(f"Listening on {HOST}:{PORT}")
  s.listen(1)
  while True:
    conn, addr = s.accept()
    print("Connection established")
    with conn, conn.makefile('rb') as r:
      while True:
        try:
          data = pickle.load(r)
        except EOFError:
          # Client has closed the connection
          break
        print(data)
        leds.display_frame(data)
      print("Connection closed")
