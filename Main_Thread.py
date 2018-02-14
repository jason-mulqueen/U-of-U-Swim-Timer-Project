#Import default libraries~ ~ ~ ~ ~ ~ ~
import serial
import serial.tools.list_ports
import sys
#- - - - - - - - - - - - - - - - - - - - - -
#Import custom libraries and classes - - - - -
from Main_GUI import Timing_GUI
#---------------------------------------------------------------------------------------


#Find connected Arduino and create serial object on connected port-------------
for port in list(serial.tools.list_ports.comports()):
    if 'Arduino' in port.description:
        arduino = serial.Serial(port[0], 9600)
        break #Once correct port is found, there is no need to scan the rest

#Wait for Arduino to be ready to go
while arduino.inWaiting() <= 0:
    continue
myData = bytes.decode(arduino.readline()) #Read Ready signal to clear it out

#Run GUI------------------------
app = qw.QApplication(sys.argv)
sudoku = Timing_GUI()
sys.exit(app.exec_())