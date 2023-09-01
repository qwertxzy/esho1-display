import RPi.GPIO as GPIO
import numpy as np
from time import sleep

# constants
SLEEP_S = 0.00001
PWM_FREQ = 75

class Panel:

  @staticmethod
  def __convert_frame(frame: np.ndarray):
    """Converts a standard 2d frame with top-left origin to 1d array
    for the led matrix.
    """
    # Initialize an empty buffer
    output_buffer = np.zeros(16**2)

    if frame.shape != (16, 16):
      raise ValueError

    # Loop over frame
    for line_idx, line in enumerate(frame):
      # split line into two
      (left, right) = np.array_split(line, 2)

      # put left half into line_idx * 8
      start_idx = line_idx * 8
      idxs = [i for i in range(start_idx, start_idx + len(left))]
      np.put(output_buffer, idxs, left)

      # put right half into line_idx * 8 + 128 to get second half of the buffer
      start_idx = line_idx * 8 + 128
      idxs = [i for i in range(start_idx, start_idx + len(right))]
      np.put(output_buffer, idxs, right)

    return output_buffer

  def __init__(self, clk_pin, data_pin, latch_pin, en_pin):
    self.__clk_pin = clk_pin
    self.__data_pin = data_pin
    self.__latch_pin = latch_pin

    GPIO.setmode(GPIO.BOARD)

    # set gpio modes
    GPIO.setup(clk_pin, GPIO.OUT)
    GPIO.setup(data_pin, GPIO.OUT)
    GPIO.setup(latch_pin, GPIO.OUT)
    GPIO.setup(en_pin, GPIO.OUT)

    #set default values
    GPIO.output(clk_pin, GPIO.LOW)
    GPIO.output(data_pin, GPIO.LOW)
    GPIO.output(latch_pin, GPIO.LOW)
    GPIO.output(en_pin, GPIO.LOW)
    self.clear_screen()
    self.__pwm = GPIO.PWM(en_pin, PWM_FREQ)
    self.__pwm.start(70)

  def __del__(self):
    self.__pwm.stop()
    GPIO.cleanup()

  def write_bit(self, val):
    """Write a single bit into the shift registers."""
    gpio_val = GPIO.HIGH if val else GPIO.LOW
    GPIO.output(self.__data_pin, gpio_val)
    sleep(SLEEP_S)
    GPIO.output(self.__clk_pin, GPIO.HIGH)
    sleep(SLEEP_S)
    GPIO.output(self.__clk_pin, GPIO.LOW)

  def latch_data(self):
    """Show current shift register data on the matrix."""
    sleep(SLEEP_S*2)
    GPIO.output(self.__latch_pin, GPIO.HIGH)
    sleep(SLEEP_S)
    GPIO.output(self.__latch_pin, GPIO.LOW)

  def display_frame(self, frame):
    """Display a whole 16x16 frame."""
    for val in self.__convert_frame(frame):
      self.write_bit(val)
    self.latch_data()

  def clear_screen(self):
    """Clear the matrix turning all leds off."""
    for _ in range(16 * 16):
      self.write_bit(0)
    self.latch_data()

  def show_led_order(self, delay_s=0.25):
    """Display a small animation showing the matrix led order."""
    for i in range(16 * 16):
      self.write_bit((not i))
      self.latch_data()
      sleep(delay_s)

  def set_brightness(self, brightness):
    """Adjust display brightness from 0 to 100."""
    if brightness not in range(101):
      raise ValueError("Brightness value must be between 0 and 100")
    self.__pwm.ChangeDutyCycle(100 - brightness)