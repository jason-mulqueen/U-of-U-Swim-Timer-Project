def open_python_port():
    """Find connected Arduino and create serial object on connected port"""
    for port in list(serial.tools.list_ports.comports()):
        if 'Arduino' in port.description:
            return serial.Serial(port[0], 9600)

def wait_for_arduino_ready(arduino):
    """Wait for Arduino to be ready to go"""
    while arduino.inWaiting() <= 0:
        continue
    myData = bytes.decode(arduino.readline()) #Read Ready signal to clear it out