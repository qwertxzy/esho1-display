from TextUtils import Scroller

charset_path = 'charset.png'
charset_lookup = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz°1234567890@-%:'
host = "127.0.0.1"
port = 6969

sc = Scroller(charset_path, charset_lookup, host, port, debug=True)
sc.set_message("peepee")
import time
while True:
 sc.tick()
 time.sleep(0.1)