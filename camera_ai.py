import machine
import sys
import uselect

class AI_CAMERA:
  
  def __init__(self, rx_pin=None, tx_pin=None):
    if rx_pin == None and tx_pin == None: # using ohstem app
      self._uart = None
    else:
      self._uart = machine.UART(2, baudrate=115200, rx=rx_pin, tx=tx_pin, timeout=10)
      self._uart.init(parity=None, stop=1, bits=8)

    self.current_classname = ''
    self.current_prediction = 0

  def update(self):
    # flush old data and get latest one
    data = ''
    if self._uart: # from camera AI
      while self._uart.any():
        data = self.uart.readline()
    else:
      data = self._read_repl()
    
    if data:
      try:
        if self._uart:
          # data is byte array
          self.current_classname, self.current_prediction = str(data[:-1].decode('utf-8')).split(";")
        else:
          # data from repl is string
          self.current_classname, self.current_prediction = str(data)[:-1].split(";")

        self.current_prediction = float(self.current_prediction)*100
      except Exception as error:
        #print('Error parsing AI result: ')
        #print(error)
        self.current_classname = ''
        self.current_prediction = 0
    else:
      self.current_classname = ''
      self.current_prediction = 0

  '''
    reversed: 
      If True, function will return True if AI result != class_name
      If False, function will return True if AI result == class_name
  '''
  def check(self, class_name, prediction=0, reversed=False):
    if not reversed:
        if self.current_prediction >= prediction and self.current_classname == class_name:
          return True
        else:
          return False
    else:
      if (self.current_classname != class_name or self.current_prediction < prediction) \
        and self.current_classname != '':
          return True
      else:
        return False

  def get_classname(self):
    return self.current_classname
  
  def get_prediction(self):
    return self.current_prediction
  
  def _read_repl(self):
    spoll=uselect.poll()        # Set up an input polling object.
    spoll.register(sys.stdin, uselect.POLLIN)    # Register polling object.

    input = ''
    if spoll.poll(0):
        input = sys.stdin.read(1)

        while spoll.poll(0):
            input = input + sys.stdin.read(1)

    spoll.unregister(sys.stdin)
    return input
