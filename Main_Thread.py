#Import default libraries~ ~ ~ ~ ~ ~ ~
import serial
import serial.tools.list_ports
import sys
#- - - - - - - - - - - - - - - - - - - - - -
#Import custom libraries and classes - - - - -
from Main_GUI import Timing_GUI
import AuxFunctions as AF
#---------------------------------------------------------------------------------------

#Navigate to working directory, creating if necessary
AF.nav_to_directory(os.path.join("C:\\Users", os.getlogin(), "Documents", "Swim Manager"))

#Ready serial device
arduino = AF.open_python_port()
AF.wait_for_arduino_ready(arduino)


#Run GUI------------------------
app = qw.QApplication(sys.argv)
sudoku = Timing_GUI()
sys.exit(app.exec_())